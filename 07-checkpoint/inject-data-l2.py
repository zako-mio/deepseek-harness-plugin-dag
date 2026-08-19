#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S3 L2 交互图 DATA 注入:
读取 webapp-dag.json (134 节点) + external-seams.json (36 seam) + stage-00-l2-inventory.json (disabled 清单)
生成完整 DATA 注入 index.html (替换第 60 行 const DATA = {...};)
同时: 在样式数组插入 node[kind="disabled"] 数据属性选择器 (L155 与 L156 之间)
"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0819-plugin-dag-rc7"
DAG = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
EXT = os.path.join(BASE, "01-dag-data", "external-seams.json")
INV = os.path.join(BASE, "07-checkpoint", "stage-00-l2-inventory.json")
HTML = os.path.join(BASE, "04-interactive", "index.html")

with open(DAG, "r", encoding="utf-8") as f:
    dag = json.load(f)
with open(EXT, "r", encoding="utf-8") as f:
    ext = json.load(f)
with open(INV, "r", encoding="utf-8") as f:
    inv = json.load(f)

nodes = {n["id"]: n for n in dag["nodes"]}
groups = {g["id"]: g for g in dag["groups"]}
edges = dag["edges"]
ext_map = {e["id"]: e for e in ext["seams"]}

# disabled 清单: L1 节点中在 web patch 被 disabled 的
disabled_ids = set()
for d in inv["disabled_base_rows"]:
    if d.get("node") and d["node"] in nodes:
        disabled_ids.add(d["node"])
print(f"[INFO] disabled base rows: {len(disabled_ids)} -> {sorted(disabled_ids)}")

# 组配色 (29 组 + EXT; 5 个新组追加新色)
palette = ["#4f8cff","#7b61ff","#2fb98a","#e8933b","#e05563","#3b9fe0","#9a7bf0","#e0a03b",
           "#3bc4a0","#d0546b","#6c8df5","#b48a3c","#54a0e8","#8a5cf0","#3ab7c4","#e07b54",
           "#5f8de0","#9b6bd4","#4aa8a0","#d06a4a","#6b9bd4","#b07bd4","#4ac48e","#d48a5b",
           "#e8a13b","#6b8fe8","#3bc48a","#d07bd4","#4f8ce8"]
gids = sorted(groups.keys())
GROUP_COLORS = {}
for i, gid in enumerate(gids):
    GROUP_COLORS[gid] = palette[i % len(palette)]

# ---- 插件节点 (134, 含 L1 76 + L2 58) ----
plugin_nodes = []
for nid, n in nodes.items():
    if nid in disabled_ids:
        kind = "disabled"
    else:
        kind = "plugin"
    plugin_nodes.append({
        "data": {
            "id": nid, "label": nid, "kind": kind, "group": n["group"],
            "gname": n["group_name"], "layer": n["layer"],
            "url": f"../02-plugin-pages/{nid}.html"
        }
    })

# ---- 外部 seam 节点 (36) ----
ext_nodes = []
for sid, s in ext_map.items():
    ext_nodes.append({
        "data": {
            "id": sid, "label": sid, "kind": "seam", "group": "EXT",
            "gname": "外部基座seam", "layer": 0, "url": f"../02-plugin-pages/{sid}.html"
        }
    })

# ---- 依赖边 (核心 434) ----
edge_list = []
for e in edges:
    kind = "core"
    # disabled 插件参与的边标记 (disabled 插件是 web 变体禁用的, 边仍存在但弱化)
    edge_list.append({"data": {"id": f"{e['from']}->{e['to']}", "source": e["from"], "target": e["to"], "kind": kind}})

# ---- 外部 seam 边 (plugin -> seam) ----
for sid, s in ext_map.items():
    for dep in s.get("referred_by", []):
        if dep in nodes:
            edge_list.append({"data": {"id": f"{dep}->{sid}", "source": dep, "target": sid, "kind": "seam"}})

# ---- 组聚合边 (组级视图) ----
group_edges = []
def add_group_edge(gs, gt):
    key = f"grp-{gs}->grp-{gt}"
    if not any(ge["data"]["id"] == key for ge in group_edges):
        group_edges.append({"data": {"id": key, "source": "grp-"+gs, "target": "grp-"+gt, "kind": "group"}})

for e in edges:
    gs = nodes[e["from"]]["group"]
    gt = nodes[e["to"]]["group"]
    if gs != gt:
        add_group_edge(gs, gt)
for sid, s in ext_map.items():
    for dep in s.get("referred_by", []):
        if dep in nodes:
            add_group_edge(nodes[dep]["group"], "EXT")

# ---- 组节点总数 (组级视图) ----
print(f"[INFO] groups in DAG: {len(gids)} -> 组级视图节点 = {len(gids) + 1}(+EXT)")

payload = {
    "plugins": plugin_nodes,
    "seams": ext_nodes,
    "edges": edge_list,
    "groupEdges": group_edges,
    "groups": {gid: {"name": groups[gid]["name"], "color": GROUP_COLORS[gid]} for gid in gids},
    "groupColor": GROUP_COLORS,
    "extColor": "#b48a3c",
    "disabledIds": sorted(disabled_ids)
}

data_json = json.dumps(payload, ensure_ascii=False)

# ---- 替换第 60 行 ----
with open(HTML, "rb") as f:
    raw = f.read()

# 文件无 BOM, CRLF
content = raw.decode("utf-8")
lines = content.split("\r\n")

# 找到 const DATA = 行
data_line_idx = None
for i, l in enumerate(lines):
    if l.startswith("const DATA = "):
        data_line_idx = i
        break
if data_line_idx is None:
    print("[ERR] const DATA line not found")
    raise SystemExit(1)

print(f"[INFO] replacing line {data_line_idx+1} (len={len(lines[data_line_idx])})")
lines[data_line_idx] = "const DATA = " + data_json + ";"
content = "\r\n".join(lines)

# ---- 插入 disabled 样式 (在 node[kind="stub"] 之后 / node[kind="group"] 之前) ----
STYLE_INSERT = """{ selector:'node[kind="disabled"]', style:{
    'background-color':'#3a3f4a','border-width':1.5,'border-color':'#c0504d',
    'width':56,'height':30, shape:'round-rectangle', opacity:0.55, 'label': 'data(label)'
  }},"""

marker = '''{ selector:'node[kind="group"]','''
if marker in content and 'node[kind="disabled"]' not in content:
    content = content.replace(marker, STYLE_INSERT + "\r\n  " + marker, 1)
    print("[OK] inserted node[kind=disabled] style before node[kind=group]")
elif 'node[kind="disabled"]' in content:
    print("[SKIP] disabled style already present")
else:
    print("[WARN] marker not found for disabled style insert")

# ---- 写回 (UTF-8 无 BOM, CRLF) ----
with open(HTML, "w", encoding="utf-8", newline="") as f:
    f.write(content)

print(f"[OK] injected DATA: plugins={len(plugin_nodes)}, seams={len(ext_nodes)}, edges={len(edge_list)}, groupEdges={len(group_edges)}")
print(f"[OK] groups={len(gids)+1}(含EXT), disabled={len(disabled_ids)}")
