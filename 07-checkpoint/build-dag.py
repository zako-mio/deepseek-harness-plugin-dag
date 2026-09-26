#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2 DAG 建模脚本: 从 stage-01-r*.json 提取插件节点与依赖边,
执行层次遍历(拓扑分层) + 无环校验, 输出 core-dag.json。
"""
import json, sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
CHK = os.path.join(BASE, "07-checkpoint")
OUT = os.path.join(BASE, "01-dag-data")

# 1. 读取 6 路 stage-01 数据
routes = ["r1-core", "r2-execution", "r3-interaction", "r4-session", "r5-subagent", "r6-framework"]
plugins = {}
for r in routes:
    fp = os.path.join(CHK, f"stage-01-{r}.json")
    with open(fp, "r", encoding="utf-8") as f:
        data = json.load(f)
    for p in data["plugins"]:
        pid = p["id"]
        if pid in plugins:
            print(f"[WARN] duplicate plugin id: {pid}")
        plugins[pid] = p

print(f"[INFO] loaded {len(plugins)} plugins from 6 routes")

# 2. 读取分组清单 stage-00-inventory.json
with open(os.path.join(CHK, "stage-00-inventory.json"), "r", encoding="utf-8") as f:
    inv = json.load(f)

group_of = {}
group_name = {}
group_plugins = {}
for g in inv["groups"]:
    group_plugins[g["id"]] = []
    group_name[g["id"]] = g["name"]
    for pl in g["plugins"]:
        group_of[pl["id"]] = g["id"]
        group_plugins[g["id"]].append(pl["id"])

print(f"[INFO] groups: {len(group_plugins)}")

# 3. 归一化 plugin_id（处理 @deepseek-ai/dsh-xxx 前缀形式、vendor 前缀）
def normalize_pid(x):
    if not x:
        return None
    x = x.strip()
    if x.startswith("@deepseek-ai/"):
        x = x[len("@deepseek-ai/"):]
    # 处理子入口如 tool-subagent-control/list-agents -> 归并到主包
    if "/" in x:
        x = x.split("/")[0]
    return x

# 3.5 读取 PACKAGE-MAP 补充 path
MAP = r"D:\Opencode_Download\Mission-file\2026-08\0814-deepseek-harness源码解析\07-checkpoint\PACKAGE-MAP.json"
with open(MAP, "r", encoding="utf-8") as f:
    pkgmap = json.load(f)
pkg_by_name = {p["name"]: p for p in pkgmap["packages"]}
def path_of(pid):
    full = "@deepseek-ai/" + pid
    meta = pkg_by_name.get(full)
    if meta:
        return meta.get("path", "")
    return ""

# 4. 构建依赖边（规范化 plugin_id 到本集合内）
edges = []  # (from_id, to_id, evidence, purpose, mechanism)
all_ids = set(plugins.keys())

for pid, p in plugins.items():
    for dep in p.get("depends_on", []):
        dep_id = normalize_pid(dep.get("plugin_id", ""))
        if not dep_id:
            continue
        # 指向本集合内才建边; 外部 seam 包(如 dsh-fs/dsh-llm 基座)若在本集合则建
        if dep_id in all_ids:
            edges.append((pid, dep_id, dep.get("evidence", ""), dep.get("purpose", ""), dep.get("mechanism", "E1")))

print(f"[INFO] edges within set: {len(edges)}")

# 5. 无环校验 + 拓扑分层（层次遍历 BFS: 被依赖方先于依赖方）
# 先建反图: in_degree 表示该节点被多少本集合内前驱依赖? 我们求"依赖的插件必须先激活"
# 方向: edges (a -> b) 表示 a depends on b, 即 b 必须先于 a。
# 拓扑序: b 在 a 前。用 Kahn: 初始入度=依赖数(指向自己的边数)
indeg = {pid: 0 for pid in all_ids}
adj = {pid: [] for pid in all_ids}
for a, b, ev, pu, mech in edges:
    adj[b].append(a)   # b 完成后 a 才能开始 (a depends on b)
    indeg[a] += 1

# 分层 BFS: 层0 = 无依赖的叶子(被依赖方), 逐层剥离
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
    # 有环: 找出剩余节点
    cycle_nodes = [pid for pid in all_ids if indeg[pid] > 0]
    print(f"[ERROR] CYCLE DETECTED: {len(cycle_nodes)} nodes involved")
    print(f"[ERROR] nodes: {cycle_nodes}")
    # 输出环信息
    for pid in cycle_nodes:
        deps = [b for a, b, ev, pu, mech in edges if a == pid and b in cycle_nodes]
        print(f"  {pid} -> in-cycle deps: {deps}")
    sys.exit(1)

print(f"[INFO] acyclic OK; layers: {layer}")

# 6. 构建输出
nodes = []
for pid, p in plugins.items():
    gid = group_of.get(pid, "G99")
    nodes.append({
        "id": pid,
        "name": p["name"],
        "group": gid,
        "group_name": group_name.get(gid, "未分组"),
        "layer": levels[pid],
        "implementation": p["implementation"],
        "provides": p.get("provides", []),
        "path": path_of(pid)
    })

# 节点提供者关系(被谁依赖) - 从 edges 反推
dependents_map = {pid: [] for pid in all_ids}
for a, b, ev, pu, mech in edges:
    dependents_map[b].append({"plugin_id": a, "evidence": ev, "purpose": pu})

edges_out = []
for a, b, ev, pu, mech in edges:
    edges_out.append({
        "from": a,
        "to": b,
        "mechanism": mech,
        "evidence": ev,
        "purpose": pu
    })

result = {
    "meta": {
        "mission": "deepseek-harness 插件级 DAG 依赖链分析 - 第一层核心集",
        "generated_at": "2026-08-16",
        "source": "stage-01-r1~r6.json (6路 explore 源码级三依据分析)",
        "plugin_count": len(nodes),
        "edge_count": len(edges_out),
        "layer_count": layer,
        "group_count": len(group_plugins),
        "acyclic": True
    },
    "groups": [
        {"id": gid, "name": group_name[gid], "plugins": group_plugins[gid]}
        for gid in group_name
    ],
    "layers": {
        str(i): [pid for pid in all_ids if levels[pid] == i]
        for i in range(layer)
    },
    "nodes": sorted(nodes, key=lambda n: (n["layer"], n["id"])),
    "edges": sorted(edges_out, key=lambda e: (e["from"], e["to"]))
}

os.makedirs(OUT, exist_ok=True)
out_fp = os.path.join(OUT, "core-dag.json")
with open(out_fp, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# 7. 打印分层摘要
print("\n=== 拓扑分层摘要 ===")
for i in range(layer):
    layer_ids = [pid for pid in all_ids if levels[pid] == i]
    print(f"Layer {i} ({len(layer_ids)}): {', '.join(sorted(layer_ids))}")

print(f"\n[OK] wrote {out_fp}")
print(f"[OK] plugins={len(nodes)}, edges={len(edges_out)}, layers={layer}, groups={len(group_plugins)}")
