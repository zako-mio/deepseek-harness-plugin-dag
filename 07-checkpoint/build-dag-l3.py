#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2 L3 DAG 建模脚本:
合并 webapp-dag.json (L1+L2, 134 节点) + L3 采集 (39 插件) → 更新 webapp-dag.json
- 保留 L1+L2 全部节点/边/组
- 追加 L3 节点/边/组 (G30-G37)
- 层次遍历重算拓扑层 (被依赖方先于依赖方)
- L2 环修复方法论: E3 过滤 + slot/协议注册方向修正 + dependents 不反推 + 双向耦合合并
- 无环校验
- 回填 L3 seam referred_by 到 external-seams.json
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-plugin-dag-rc8"
CHK = os.path.join(BASE, "07-checkpoint")
DAG = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
SEAMS = os.path.join(BASE, "01-dag-data", "external-seams.json")
INV = os.path.join(CHK, "stage-00-l3-inventory.json")

# ---- 1. 读取基线 DAG (L1+L2) ----
with open(DAG, "r", encoding="utf-8") as f:
    dag = json.load(f)

base_nodes = {n["id"]: n for n in dag["nodes"]}
base_edges = dag["edges"]
base_groups = {g["id"]: g for g in dag["groups"]}
print(f"[INFO] base: {len(base_nodes)} nodes, {len(base_edges)} edges, {len(base_groups)} groups")

# ---- 2. 读取 L3 采集 ----
routes = ["r1", "r2", "r3", "r4", "r5"]
l3_plugins = {}
special_modules = []
seam_referred = []
for r in routes:
    fp = os.path.join(CHK, f"stage-01-l3-{r}.json")
    with open(fp, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data if isinstance(data, list) else data.get("plugins", [])
    for p in items:
        if not isinstance(p, dict) or "id" not in p:
            continue
        pid = p["id"]
        if pid in l3_plugins:
            print(f"[WARN] duplicate L3 id: {pid} (r{r}) - keeping first, merging second dependents")
            # 去重: 合并 dependents(防止 native-command 重复), 保第一个主体
            l3_plugins[pid]["dependents"] = l3_plugins[pid].get("dependents", []) + p.get("dependents", [])
            continue
        l3_plugins[pid] = p
    if isinstance(data, dict):
        if data.get("special_modules"):
            special_modules.extend(data["special_modules"])
        # r4 是 dict 结构
    if r == "r2":
        # r2 末尾附 seam_referred_by (list 或 dict 内的字段)
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and "seam_referred_by" in item:
                    seam_referred.extend(item["seam_referred_by"])
        elif isinstance(data, dict) and data.get("seam_referred_by"):
            seam_referred.extend(data["seam_referred_by"])
print(f"[INFO] L3 plugins: {len(l3_plugins)}")
print(f"[INFO] special modules: {len(special_modules)}")
print(f"[INFO] seam_referred entries: {len(seam_referred)}")

# ---- 3. 读取 L3 inventory 分组 + path ----
with open(INV, "r", encoding="utf-8") as f:
    inv = json.load(f)

l3_group_of = {}
l3_group_name = {}
l3_group_plugins = {}
for g in inv["groups"]:
    l3_group_plugins[g["id"]] = []
    l3_group_name[g["id"]] = g["name"]
    for p in g["plugins"]:
        l3_group_of[p["id"]] = g["id"]
        l3_group_plugins[g["id"]].append(p["id"])

# path 从 inventory 取
inv_path = {}
for g in inv["groups"]:
    for p in g["plugins"]:
        inv_path[p["id"]] = p["path"]

# ---- 4. 归一化 plugin_id ----
def normalize_pid(x):
    if not x:
        return None
    x = x.strip()
    if x.startswith("@deepseek-ai/"):
        x = x[len("@deepseek-ai/"):]
    if "/" in x:
        x = x.split("/")[0]
    return x

# ---- 5. 构建全节点集 ----
# 全节点: 基线 (L1+L2) + L3 39
all_plugins = {}
for nid, n in base_nodes.items():
    all_plugins[nid] = {
        "id": nid, "name": n["name"], "implementation": n["implementation"],
        "provides": n.get("provides", []), "path": n.get("path", ""),
        "layer": n.get("source_layer", "L1")
    }
for pid, p in l3_plugins.items():
    all_plugins[pid] = {
        "id": pid, "name": p["name"], "implementation": p["implementation"],
        "provides": p.get("provides", []), "path": inv_path.get(pid, p.get("path", "")),
        "layer": "L3"
    }
print(f"[INFO] merged plugin set: {len(all_plugins)}")

# ---- 6. 构建依赖边 ----
# 方向: edges (a -> b) 表示 a depends on b (b 先于 a)
edges = []  # (from, to, evidence, purpose, mechanism, layer)
all_ids = set(all_plugins.keys())
l3_ids = set(l3_plugins.keys())

# L3 采集误报修正 (环根源, 参照 L2 方法论):
REMOVE_EDGES = {
    # native-command 是库, 不依赖 cordis/invariants (peerDep 纯声明, 采集端已标 E3)
    ("dsh-native-command", "dsh-invariants"),
    ("dsh-native-command", "cordis"),
    # 示例包对 seam 的 doc 引用 (E1 doc 契约, 非源码依赖) 已在采集端弱化, 保留若 id 存在
}

def is_assembly_meta(dep):
    """E3 装配元信息边: 指向 bundle 包 (dsh-base/dsh-headless) 的装配说明, 非真实依赖"""
    if dep.get("mechanism") != "E3":
        return False
    purpose = dep.get("purpose", "")
    pid = normalize_pid(dep.get("plugin_id", ""))
    # 特殊模块不进 DAG: 指向它们的边作 seam 处理, 过滤
    if pid in ("dsh-base", "dsh-headless"):
        return True
    if "装配顺序" in purpose or "先于" in purpose:
        return True
    return False

# 6a. 基线内部边 (L1+L2)
for e in base_edges:
    if e["from"] in all_ids and e["to"] in all_ids:
        edges.append((e["from"], e["to"], e.get("evidence",""), e.get("purpose",""), e.get("mechanism","E1"), e.get("source_layer","L1")))

# 6b. L3 采集依赖边 (过滤 self-loop + E3 装配元信息)
for pid, p in l3_plugins.items():
    for dep in p.get("depends_on", []):
        dep_id = normalize_pid(dep.get("plugin_id", ""))
        if not dep_id or dep_id == pid:
            continue  # self-loop
        if is_assembly_meta(dep):
            continue
        if (pid, dep_id) in REMOVE_EDGES:
            print(f"[INFO] removed false edge: {pid} -> {dep_id}")
            continue
        # L3 -> L1/L2/L3 都建边; seam 已在 external-seams, 非节点, 跳过
        if dep_id in all_ids:
            edges.append((pid, dep_id, dep.get("evidence",""), dep.get("purpose",""), dep.get("mechanism","E1"), "L3"))

# 6c. dependents 不反推边 (L2 方法论: 采集端 dependents 仅作展示, 不反向建边)

# 去重
seen = set()
uniq_edges = []
for e in edges:
    key = (e[0], e[1])
    if key not in seen:
        seen.add(key)
        uniq_edges.append(e)
edges = uniq_edges
print(f"[INFO] merged edges: {len(edges)}")

# ---- 7. 无环校验 + 拓扑分层 ----
indeg = {pid: 0 for pid in all_ids}
adj = {pid: [] for pid in all_ids}
for a, b, *_ in edges:
    adj[b].append(a)   # b 完成后 a 才能开始
    indeg[a] += 1

queue = [pid for pid in all_ids if indeg[pid] == 0]
levels = {}
layer = 0
processed = 0
while queue:
    nxt = []
    for pid in queue:
        levels[pid] = layer
        processed += 1
        for child in adj[pid]:
            indeg[child] -= 1
            if indeg[child] == 0:
                nxt.append(child)
    queue = nxt
    layer += 1

if processed != len(all_ids):
    cycle_nodes = [pid for pid in all_ids if indeg[pid] > 0]
    print(f"[ERROR] CYCLE DETECTED: {len(cycle_nodes)} nodes involved")
    for pid in cycle_nodes:
        deps = [b for a, b, *_ in edges if a == pid and b in cycle_nodes]
        print(f"  {pid} -> in-cycle deps: {deps}")
    sys.exit(1)

print(f"[INFO] acyclic OK; layers: {layer}, processed: {processed}")

# ---- 8. 构建输出 ----
# 分组: 基线组 + L3 8 组
all_groups = {}
for gid, g in base_groups.items():
    all_groups[gid] = {"id": gid, "name": g["name"], "plugins": list(g["plugins"])}
for gid, g in l3_group_plugins.items():
    all_groups[gid] = {"id": gid, "name": l3_group_name[gid], "plugins": g}

group_of = {}
for gid, g in all_groups.items():
    for pl in g["plugins"]:
        group_of[pl] = gid

# 检查 L3 插件是否都有分组
for pid in l3_ids:
    if pid not in group_of:
        print(f"[WARN] L3 plugin {pid} has no group, assigning G99")

nodes = []
for pid, p in all_plugins.items():
    gid = group_of.get(pid, "G99")
    nodes.append({
        "id": pid,
        "name": p["name"],
        "group": gid,
        "group_name": all_groups[gid]["name"],
        "layer": levels[pid],
        "implementation": p["implementation"],
        "provides": p.get("provides", []),
        "path": p.get("path", ""),
        "source_layer": p.get("layer", "L1"),
        **({"override_base": p["override_base"]} if p.get("override_base") else {})
    })

edges_out = []
for a, b, ev, pu, mech, src_layer in edges:
    edges_out.append({
        "from": a, "to": b, "mechanism": mech,
        "evidence": ev, "purpose": pu, "source_layer": src_layer
    })

result = {
    "meta": {
        "mission": "deepseek-harness 插件级 DAG 依赖链分析 - L1 核心集 + L2 web-app + L3 其余插件",
        "generated_at": "2026-08-17",
        "source": "webapp-dag.json (L1+L2) + stage-01-l3-r1~r5.json (5路 explore 三依据分析)",
        "plugin_count": len(nodes),
        "edge_count": len(edges_out),
        "layer_count": layer,
        "group_count": len(all_groups),
        "acyclic": True,
        "l1_plugins": len(base_nodes) - sum(1 for n in dag["nodes"] if n.get("source_layer") == "L2"),
        "l2_plugins": sum(1 for n in dag["nodes"] if n.get("source_layer") == "L2"),
        "l3_plugins": len(l3_plugins)
    },
    "groups": [all_groups[gid] for gid in sorted(all_groups.keys())],
    "layers": {
        str(i): [pid for pid in all_ids if levels[pid] == i]
        for i in range(layer)
    },
    "nodes": sorted(nodes, key=lambda n: (n["layer"], n["id"])),
    "edges": sorted(edges_out, key=lambda e: (e["from"], e["to"]))
}

os.makedirs(os.path.dirname(DAG), exist_ok=True)
with open(DAG, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# ---- 9. 回填 seam referred_by 到 external-seams.json ----
seam_changes = 0
with open(SEAMS, "r", encoding="utf-8") as f:
    seams_data = json.load(f)
seams_by_id = {s["id"]: s for s in seams_data["seams"]}

for sr in seam_referred:
    sid = sr.get("seam_id")
    if sid not in seams_by_id:
        print(f"[WARN] seam {sid} not in external-seams.json, skipping")
        continue
    seam = seams_by_id[sid]
    refs = sr.get("referred_by", [])
    mechs = sr.get("mechanisms", [])
    if refs:
        existing = set(seam.get("referred_by", []))
        merged = list(existing | set(refs))
        seam["referred_by"] = sorted(merged)
        seam["ref_count"] = len(merged)
        if mechs:
            existing_m = set(seam.get("mechanisms", []))
            seam["mechanisms"] = sorted(existing_m | set(mechs))
        seam_changes += 1
        print(f"[INFO] seam {sid}: referred_by += {refs} (total {len(merged)})")
    elif sr.get("note"):
        # 无引用的 seam 追加 note 说明
        seam["note_l3"] = sr["note"]
        seam_changes += 1

with open(SEAMS, "w", encoding="utf-8") as f:
    json.dump(seams_data, f, ensure_ascii=False, indent=2)
print(f"[INFO] seams updated: {seam_changes} entries")

# ---- 10. 打印分层摘要 ----
print("\n=== 拓扑分层摘要 (L3 标记) ===")
for i in range(layer):
    layer_ids = [pid for pid in all_ids if levels[pid] == i]
    l3_count = sum(1 for x in layer_ids if x in l3_ids)
    if l3_count > 0:
        print(f"Layer {i} ({len(layer_ids)}, L3={l3_count}): {', '.join(sorted(x for x in layer_ids if x in l3_ids))}")

print(f"\n[OK] wrote {DAG}")
print(f"[OK] plugins={len(nodes)}, edges={len(edges_out)}, layers={layer}, groups={len(all_groups)}")
