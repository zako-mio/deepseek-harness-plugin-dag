#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2 L2 DAG 建模脚本:
合并 L1 core-dag.json (76 节点) + L2 采集 (58 节点) → webapp-dag.json
- 保留 L1 全部节点/边/组
- 追加 L2 节点/边/组 (G25-G29)
- 层次遍历重算拓扑层 (被依赖方先于依赖方)
- 无环校验
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-plugin-dag-rc8"
CHK = os.path.join(BASE, "07-checkpoint")
DAG1 = os.path.join(BASE, "01-dag-data", "core-dag.json")
OUT = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
INV = os.path.join(CHK, "stage-00-l2-inventory.json")
MAP = r"D:\Opencode_Download\Mission-file\2026-08\0814-deepseek-harness源码解析\07-checkpoint\PACKAGE-MAP.json"

# ---- 1. 读取 L1 DAG ----
with open(DAG1, "r", encoding="utf-8") as f:
    dag1 = json.load(f)

l1_nodes = {n["id"]: n for n in dag1["nodes"]}
l1_edges = dag1["edges"]
l1_groups = {g["id"]: g for g in dag1["groups"]}
print(f"[INFO] L1: {len(l1_nodes)} nodes, {len(l1_edges)} edges, {len(l1_groups)} groups")

# ---- 2. 读取 L2 采集 ----
routes = ["r1", "r2", "r3", "r4"]
l2_plugins = {}
for r in routes:
    fp = os.path.join(CHK, f"stage-01-l2-{r}.json")
    with open(fp, "r", encoding="utf-8") as f:
        data = json.load(f)
    for p in data["plugins"]:
        if p["id"] in l2_plugins:
            print(f"[WARN] duplicate L2 id: {p['id']}")
        l2_plugins[p["id"]] = p
print(f"[INFO] L2 plugins: {len(l2_plugins)}")

# ---- 3. 读取 L2 inventory 分组 + path ----
with open(INV, "r", encoding="utf-8") as f:
    inv = json.load(f)

l2_group_of = {}
l2_group_name = {}
l2_group_plugins = {}
for g in inv["groups"]:
    l2_group_plugins[g["id"]] = []
    l2_group_name[g["id"]] = g["name"]
    for p in g["plugins"]:
        l2_group_of[p["id"]] = g["id"]
        l2_group_plugins[g["id"]].append(p["id"])

# path 从 inventory 取
inv_path = {}
for g in inv["groups"]:
    for p in g["plugins"]:
        inv_path[p["id"]] = p["path"]

# ---- 4. PACKAGE-MAP 补 path ----
with open(MAP, "r", encoding="utf-8") as f:
    pkgmap = json.load(f)
pkg_by_name = {p["name"]: p for p in pkgmap["packages"]}

def path_of(pid):
    if pid in inv_path:
        return inv_path[pid]
    full = "@deepseek-ai/" + pid
    meta = pkg_by_name.get(full)
    if meta:
        return meta.get("path", "")
    return ""

# ---- 5. 归一化 plugin_id ----
def normalize_pid(x):
    if not x:
        return None
    x = x.strip()
    if x.startswith("@deepseek-ai/"):
        x = x[len("@deepseek-ai/"):]
    if "/" in x:
        x = x.split("/")[0]
    return x

# ---- 6. 构建全节点集 ----
# 全节点: L1 76 + L2 58
all_plugins = {}
for nid, n in l1_nodes.items():
    all_plugins[nid] = {
        "id": nid, "name": n["name"], "implementation": n["implementation"],
        "provides": n.get("provides", []), "path": n.get("path", ""),
        "layer": "L1"
    }
for pid, p in l2_plugins.items():
    all_plugins[pid] = {
        "id": pid, "name": p["name"], "implementation": p["implementation"],
        "provides": p.get("provides", []), "path": path_of(pid),
        "layer": "L2", "override_base": p.get("override_base")
    }
print(f"[INFO] merged plugin set: {len(all_plugins)}")

# ---- 7. 构建依赖边 ----
# 方向: edges (a -> b) 表示 a depends on b (b 先于 a)
edges = []  # (from, to, evidence, purpose, mechanism, layer)
all_ids = set(all_plugins.keys())
l2_ids = set(l2_plugins.keys())

# 采集误报修正: 源码自述"零依赖/不直接依赖"却建边的伪依赖 (环根源)
REMOVE_EDGES = {
    ("dsh-client-ui-slots", "dsh-client-runtime"),      # ui-slots 是纯类型包, 被 runtime 实现而非依赖 runtime
    ("dsh-client-web-react", "dsh-cordis-host-runner"), # evidence 自述 "不直接依赖 Loader"
    ("dsh-api-remotes", "dsh-host-apiproxy"),           # E3 装配顺序说明, 非依赖; host-apiproxy type-only import 才是真实方向
    ("dsh-host-webserver", "dsh-web-app"),              # 装配元信息误报: webserver 是独立 node:http 服务, web-app 才依赖 webserver
    # UI 包间 slot 注册反向边: conversation 声明 slot, 子 UI 包注册进它的 slot → 子包依赖 conversation, 反向不成立
    ("dsh-client-ui-conversation", "dsh-client-ui-tool"),
    ("dsh-client-ui-conversation", "dsh-client-ui-workflow-run"),
    ("dsh-client-ui-conversation", "dsh-client-ui-deliverables"),
    ("dsh-client-ui-conversation", "dsh-client-ui-workspace"),
    ("dsh-client-ui-conversation", "dsh-client-ui-jobs"),
    ("dsh-client-ui-conversation", "dsh-client-ui-goal"),
    ("dsh-client-ui-conversation", "dsh-client-ui-trajectory"),
    ("dsh-client-ui-conversation", "dsh-client-ui-user-questions"),
    ("dsh-client-ui-conversation", "dsh-client-ui-message-feedback"),
    # input-trigger 不依赖 skill (skill 注册 '/' source 进 input-trigger; 方向反了)
    ("dsh-client-ui-input-trigger", "dsh-client-ui-skill"),
}
# 手动补真实运行时依赖 (L1 采集时 code-runtime 不在集内)
ADD_EDGES = [
    ("dsh-tools", "dsh-code-runtime-worker-thread", "packages/core/tools/src/index.ts:1020-1022", "Code Mode 工具经 ctx.get('codeRuntime') 解析运行时, 缺失 loud 报错", "E2"),
]

def is_assembly_meta(dep):
    """E3 装配元信息边: 指向 dsh-web-app 的 'insert 行装配' 或 '装配顺序' 说明, 非真实依赖"""
    if dep.get("mechanism") != "E3":
        return False
    purpose = dep.get("purpose", "")
    pid = normalize_pid(dep.get("plugin_id", ""))
    # 真实注入关系保留: inject: [webStartup]/[webRuntime] 是装配层显式服务注入
    if pid == "dsh-web-app" and "inject" in purpose:
        return False
    if pid == "dsh-web-app":
        return True
    if "装配顺序" in purpose or "先于" in purpose:
        return True
    return False

# 7a. L1 内部边
for e in l1_edges:
    if e["from"] in all_ids and e["to"] in all_ids:
        edges.append((e["from"], e["to"], e.get("evidence",""), e.get("purpose",""), e.get("mechanism","E1"), "L1"))

# 7b. L2 采集依赖边 (过滤 self-loop + E3 装配元信息)
for pid, p in l2_plugins.items():
    for dep in p.get("depends_on", []):
        dep_id = normalize_pid(dep.get("plugin_id", ""))
        if not dep_id or dep_id == pid:
            continue  # self-loop
        if is_assembly_meta(dep):
            continue
        # 采集误报修正
        if (pid, dep_id) in REMOVE_EDGES:
            print(f"[INFO] removed false edge: {pid} -> {dep_id}")
            continue
        # L2 -> L2 或 L2 -> L1 都建边; 外部 seam 指向 L1 seam 节点也建
        if dep_id in all_ids:
            edges.append((pid, dep_id, dep.get("evidence",""), dep.get("purpose",""), dep.get("mechanism","E1"), "L2"))

# 7c. 手动补边
for a, b, ev, pu, mech in ADD_EDGES:
    if a in all_ids and b in all_ids:
        edges.append((a, b, ev, pu, mech, "L1"))

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

# ---- 8. 无环校验 + 拓扑分层 ----
# 组合引用拆分: evidence/purpose 中 "a / b" 已在采集端拆开, 但保险起见按 plugin_id 已归一
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

# ---- 9. 构建输出 ----
# 分组: L1 24 组 + L2 5 组
all_groups = {}
for gid, g in l1_groups.items():
    all_groups[gid] = {"id": gid, "name": g["name"], "plugins": list(g["plugins"])}
for gid, g in l2_group_plugins.items():
    all_groups[gid] = {"id": gid, "name": l2_group_name[gid], "plugins": g}

group_of = {}
for gid, g in all_groups.items():
    for pl in g["plugins"]:
        group_of[pl] = gid

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
        "mission": "deepseek-harness 插件级 DAG 依赖链分析 - L1 核心集 + L2 web-app bundle",
        "generated_at": "2026-08-17",
        "source": "core-dag.json (L1) + stage-01-l2-r1~r4.json (4路 explore 三依据分析)",
        "plugin_count": len(nodes),
        "edge_count": len(edges_out),
        "layer_count": layer,
        "group_count": len(all_groups),
        "acyclic": True,
        "l1_plugins": len(l1_nodes),
        "l2_plugins": len(l2_plugins)
    },
    "groups": [all_groups[gid] for gid in sorted(all_groups.keys())],
    "layers": {
        str(i): [pid for pid in all_ids if levels[pid] == i]
        for i in range(layer)
    },
    "nodes": sorted(nodes, key=lambda n: (n["layer"], n["id"])),
    "edges": sorted(edges_out, key=lambda e: (e["from"], e["to"]))
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# ---- 10. 打印分层摘要 ----
print("\n=== 拓扑分层摘要 ===")
for i in range(layer):
    layer_ids = [pid for pid in all_ids if levels[pid] == i]
    l2_count = sum(1 for x in layer_ids if x in l2_ids)
    print(f"Layer {i} ({len(layer_ids)}, L2={l2_count}): {', '.join(sorted(layer_ids))}")

print(f"\n[OK] wrote {OUT}")
print(f"[OK] plugins={len(nodes)}, edges={len(edges_out)}, layers={layer}, groups={len(all_groups)}")
