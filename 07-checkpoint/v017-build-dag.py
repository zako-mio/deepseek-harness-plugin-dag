#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v0.1.7-rc.2 数据层构建：
  - 合并 21 个分片 → 239 节点 + 边
  - 拓扑分层（最长路径；type-only 边不参与分层，仅展示）
  - 环检测与报告
  - 输出 webapp-dag.json / external-seams.json / core-dag.json
"""
import json, os, re, sys
from collections import defaultdict, Counter, deque
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
OUT = os.path.join(SCRIPT_DIR, "v017")
DATA = os.path.join(BASE, "01-dag-data")

cls = json.load(open(os.path.join(OUT, "classification.json"), encoding="utf-8"))
facts = json.load(open(os.path.join(OUT, "facts.json"), encoding="utf-8"))
inv = json.load(open(os.path.join(OUT, "inventory.json"), encoding="utf-8"))

EXCLUDE_TARGETS = {"dsh-base", "dsh-headless", "dsh-web-app", "dsh-acp-app", "dsh-sdk-app",
                   "dsh-sdk-minimal", "dsh-app-boot", "dsh-cmdline"}

# ---- 分片结果合并 ----
analysis = {}
for f in sorted(os.listdir(OUT)):
    if f.startswith("stage-01-shard-") and f.endswith(".json"):
        for x in json.load(open(os.path.join(OUT, f), encoding="utf-8")):
            analysis[x["id"]] = x

node_ids = set(cls["nodes"])
seam_ids = set(cls["seams"])
group_of, group_name = {}, {}
for g in cls["groups"]:
    for p in g["plugins"]:
        group_of[p] = g["id"]
        group_name[g["id"]] = g["name"]

# ---- type-only 判定（双通道：证据文本 + 确定性 import 行）----
RE_TYPE_IMPORT = re.compile(r"""^\s*(?:import|export)\s+type\b""")


def import_lines_type_only(a, b):
    """facts 中 a 对 b 的所有 import 行是否全为 type-only"""
    locs = [i["loc"] for i in facts.get(a, {}).get("imports", []) if i["dep"] == b]
    if not locs:
        return None
    all_type = True
    for loc in locs:
        f, _, ln = loc.rpartition(":")
        try:
            src = os.path.join(BASE, "05-source", "dsh-v0.1.7-rc.2",
                               "deepseek-harness-dsh-v0.1.7-rc.2", facts[a]["path"], f)
            with open(src, encoding="utf-8", errors="replace") as fh:
                lines = fh.readlines()
            txt = lines[int(ln) - 1]
        except Exception:
            return None
        if not RE_TYPE_IMPORT.match(txt):
            all_type = False
    return all_type


# ---- 组装边 ----
edges = []
seen = set()
for pid, x in analysis.items():
    for dp in x.get("depends_on", []):
        tgt = dp.get("plugin_id")
        if not tgt or tgt == pid or tgt in EXCLUDE_TARGETS:
            continue
        if tgt not in node_ids and tgt not in seam_ids:
            continue  # 非仓内包
        key = (pid, tgt)
        if key in seen:
            continue
        seen.add(key)
        ev = dp.get("evidence", "")
        mech = dp.get("mechanism", "E1")
        has_runtime = ("E2" in mech) or ("E3" in mech)
        to = False
        if not has_runtime:
            ti = import_lines_type_only(pid, tgt)
            if ti is None:
                to = bool(re.search(r"import type|type-only|纯类型|仅类型|type 导入", ev))
            else:
                to = ti
        edges.append({
            "from": pid, "to": tgt,
            "mechanism": mech,
            "evidence": ev, "purpose": dp.get("purpose", ""),
            "type_only": bool(to),
        })

print(f"[INFO] edges in DAG (node->node): {len(edges)}")
seam_edges = [e for e in edges if e["to"] in seam_ids]
node_edges = [e for e in edges if e["to"] in node_ids]
edges = node_edges          # schema 约定：edges 仅节点间边；seam 边经 external-seams.referred_by 表达
print(f"        → edges(节点间): {len(node_edges)}, seam_edges: {len(seam_edges)}")
print(f"        type_only: {sum(1 for e in edges if e['type_only'])}")

# ---- external-seams.json ----
seams_out = []
for sid in sorted(seam_ids):
    f = facts[sid]
    refs = sorted({e["from"] for e in seam_edges if e["to"] == sid})
    mechs = sorted({m for e in seam_edges if e["to"] == sid for m in e["mechanism"].split("+") if m.startswith("E")})
    seams_out.append({
        "id": sid,
        "name": f["name"],
        "path": f["path"],
        "ts_count": f.get("ts_count", 0),
        "description": "",
        "ref_count": len(refs),
        "referred_by": refs,
        "mechanisms": mechs,
    })
with open(os.path.join(DATA, "external-seams.json"), "w", encoding="utf-8") as fh:
    json.dump({"count": len(seams_out), "seams": seams_out}, fh, ensure_ascii=False, indent=2)
print(f"[INFO] external-seams.json: {len(seams_out)} seams")

# ---- 分层：最长路径（只用非 type-only 边） ----
# 环处理：DFS 找反馈边（back edge）→ 标记 soft，保留展示但不参与分层（零信息损失）
runtime_pairs = [(e["from"], e["to"]) for e in node_edges if not e["type_only"]]
radj = defaultdict(list)
for a, b in runtime_pairs:
    radj[b].append(a)          # b -> 其依赖方 a；拓扑分层按「被依赖方先」

color = {}
soft = set()
stack = []


def dfs_cycle(u):
    color[u] = 1
    stack.append(u)
    for v in radj[u]:
        if color.get(v, 0) == 0:
            dfs_cycle(v)
        elif color.get(v) == 1:
            soft.add((v, u))   # v 依赖 u，但 u 又（间接）依赖 v → 反馈边
    stack.pop()
    color[u] = 2


sys.setrecursionlimit(20000)
for n in sorted(node_ids):
    if color.get(n, 0) == 0:
        dfs_cycle(n)
print(f"[INFO] feedback(soft) edges: {len(soft)} -> {sorted(soft)}")

for e in edges:
    if e["type_only"]:
        continue
    if (e["from"], e["to"]) in soft:
        e["soft"] = True

runtime_edges = [(a, b) for a, b in runtime_pairs if (a, b) not in soft]
adj = defaultdict(list)   # u (被依赖) -> [v (依赖 u)]
indeg = {n: 0 for n in node_ids}
for a, b in runtime_edges:          # a depends on b  => b 先于 a
    adj[b].append(a)
    indeg[a] += 1

q = deque([n for n in node_ids if indeg[n] == 0])
level = {n: 0 for n in node_ids}
processed = 0
while q:
    u = q.popleft()
    processed += 1
    for v in adj[u]:
        level[v] = max(level[v], level[u] + 1)
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)

if processed != len(node_ids):
    cyc = sorted(n for n in node_ids if indeg[n] > 0)
    print(f"[ERROR] CYCLE remains: {len(cyc)} nodes")
    with open(os.path.join(OUT, "cycle-report.json"), "w", encoding="utf-8") as fh:
        json.dump({"cycle_nodes": cyc}, fh, ensure_ascii=False, indent=1)
else:
    print(f"[OK] acyclic after soft-edge removal; layer max = {max(level.values())}")

# type-only 参与的环（仅报告）
to_adj = defaultdict(list)
to_indeg = {n: 0 for n in node_ids}
for e in node_edges:
    to_adj[e["to"]].append(e["from"]); to_indeg[e["from"]] += 1
q2 = deque([n for n in node_ids if to_indeg[n] == 0]); p2 = 0
while q2:
    u = q2.popleft(); p2 += 1
    for v in to_adj[u]:
        to_indeg[v] -= 1
        if to_indeg[v] == 0:
            q2.append(v)
print(f"[INFO] 全边（含 type-only）可达: {p2}/{len(node_ids)} → 含 type 边的环节点 {len(node_ids)-p2}")

# ---- 节点 ----
def src_layer(pid):
    asm = facts[pid]["assembled_in"]
    if "base" in asm:
        return "L1"
    if "web-app" in asm:
        return "L2"
    return "L3"


nodes_out = []
for pid in sorted(node_ids):
    f = facts[pid]
    x = analysis.get(pid, {})
    gid = group_of.get(pid, "G99")
    nodes_out.append({
        "id": pid,
        "name": f["name"],
        "group": gid,
        "group_name": group_name.get(gid, "未分组"),
        "layer": level[pid],
        "implementation": x.get("implementation", ""),
        "provides": x.get("provides", []),
        "path": f["path"],
        "source_layer": src_layer(pid),
        "assembled_in": f["assembled_in"],
    })

result = {
    "meta": {
        "mission": "DeepSeek Harness 插件级 DAG 依赖链分析 — v0.1.7-rc.2 全量重建",
        "generated_at": "2026-09-27",
        "source": "官方 tarball dsh-v0.1.7-rc.2 (SHA256 761df167…) + 21 分片源码级三依据分析",
        "plugin_count": len(nodes_out),
        "edge_count": len(edges),
        "seam_edge_count": len(seam_edges),
        "layer_count": max(level.values()) + 1,
        "group_count": len(cls["groups"]),
        "seam_count": len(seams_out),
        "acyclic": processed == len(node_ids),
        "l1_plugins": sum(1 for n in nodes_out if n["source_layer"] == "L1"),
        "l2_plugins": sum(1 for n in nodes_out if n["source_layer"] == "L2"),
        "l3_plugins": sum(1 for n in nodes_out if n["source_layer"] == "L3"),
    },
    "groups": [{"id": g["id"], "name": g["name"], "plugins": g["plugins"]} for g in cls["groups"]],
    "layers": {str(i): sorted(p for p in node_ids if level[p] == i) for i in range(max(level.values()) + 1)},
    "nodes": sorted(nodes_out, key=lambda n: (n["layer"], n["id"])),
    "edges": sorted(edges, key=lambda e: (e["from"], e["to"])),
    "seam_edges": sorted(seam_edges, key=lambda e: (e["from"], e["to"])),
}
with open(os.path.join(DATA, "webapp-dag.json"), "w", encoding="utf-8") as fh:
    json.dump(result, fh, ensure_ascii=False, indent=2)
print(f"[OK] webapp-dag.json: {len(nodes_out)} nodes / {len(edges)} edges / {result['meta']['layer_count']} layers / {len(result['groups'])} groups")

# ---- core-dag.json = L1 子图 ----
l1 = {n["id"] for n in nodes_out if n["source_layer"] == "L1"}
core = {
    "meta": {**result["meta"], "mission": "DeepSeek Harness 插件级 DAG 依赖链分析 — L1 core (v0.1.7-rc.2)",
             "plugin_count": len(l1), "group_count": len({n["group"] for n in nodes_out if n["id"] in l1})},
    "groups": [{"id": g["id"], "name": g["name"], "plugins": [p for p in g["plugins"] if p in l1]}
               for g in result["groups"] if any(p in l1 for p in g["plugins"])],
    "layers": {k: [p for p in v if p in l1] for k, v in result["layers"].items()},
    "nodes": [n for n in result["nodes"] if n["id"] in l1],
    "edges": [e for e in edges if e["from"] in l1 and e["to"] in l1],
}
core["meta"]["edge_count"] = len(core["edges"])
core["meta"]["layer_count"] = len([k for k, v in core["layers"].items() if v])
with open(os.path.join(DATA, "core-dag.json"), "w", encoding="utf-8") as fh:
    json.dump(core, fh, ensure_ascii=False, indent=2)
print(f"[OK] core-dag.json: {len(core['nodes'])} nodes / {len(core['edges'])} edges")
