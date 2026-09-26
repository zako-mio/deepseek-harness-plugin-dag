#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重新注入 DATA JSON 到 index.html (替换 __DATA__ 占位符)"""
import json, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
DAG = os.path.join(BASE, "01-dag-data", "core-dag.json")
EXT = os.path.join(BASE, "01-dag-data", "external-seams.json")
HTML = os.path.join(BASE, "04-interactive", "index.html")

with open(DAG, "r", encoding="utf-8") as f:
    dag = json.load(f)
with open(EXT, "r", encoding="utf-8") as f:
    ext = json.load(f)

nodes = {n["id"]: n for n in dag["nodes"]}
groups = {g["id"]: g for g in dag["groups"]}
edges = dag["edges"]
ext_map = {e["id"]: e for e in ext["seams"]}

GROUP_COLORS = {}
palette = ["#4f8cff","#7b61ff","#2fb98a","#e8933b","#e05563","#3b9fe0","#9a7bf0","#e0a03b",
           "#3bc4a0","#d0546b","#6c8df5","#b48a3c","#54a0e8","#8a5cf0","#3ab7c4","#e07b54",
           "#5f8de0","#9b6bd4","#4aa8a0","#d06a4a","#6b9bd4","#b07bd4","#4ac48e","#d48a5b"]
gids = sorted(groups.keys())
for i, gid in enumerate(gids):
    GROUP_COLORS[gid] = palette[i % len(palette)]

plugin_nodes = []
for nid, n in nodes.items():
    gid = n["group"]
    plugin_nodes.append({
        "data": {
            "id": nid, "label": nid, "kind": "plugin", "group": gid,
            "gname": n["group_name"], "layer": n["layer"], "url": f"../02-plugin-pages/{nid}.html"
        }
    })

ext_nodes = []
for sid, s in ext_map.items():
    ext_nodes.append({
        "data": {
            "id": sid, "label": sid, "kind": "seam", "group": "EXT",
            "gname": "外部基座seam", "layer": 0, "url": f"../02-plugin-pages/{sid}.html"
        }
    })

edge_list = []
for e in edges:
    edge_list.append({"data": {"id": f"{e['from']}->{e['to']}", "source": e["from"], "target": e["to"], "kind": "core"}})

for sid, s in ext_map.items():
    for dep in s.get("referred_by", []):
        if dep in nodes:
            edge_list.append({"data": {"id": f"{dep}->{sid}", "source": dep, "target": sid, "kind": "seam"}})

group_edges = []
for e in edges:
    gs = nodes[e["from"]]["group"]
    gt = nodes[e["to"]]["group"]
    if gs != gt:
        key = f"grp-{gs}->grp-{gt}"
        if not any(ge["data"]["id"] == key for ge in group_edges):
            group_edges.append({"data": {"id": key, "source": "grp-"+gs, "target": "grp-"+gt, "kind": "group"}})
for sid, s in ext_map.items():
    for dep in s.get("referred_by", []):
        if dep in nodes:
            gs = nodes[dep]["group"]
            key = f"grp-{gs}->grp-EXT"
            if not any(ge["data"]["id"] == key for ge in group_edges):
                group_edges.append({"data": {"id": key, "source": "grp-"+gs, "target": "grp-EXT", "kind": "group"}})

payload = {
    "plugins": plugin_nodes,
    "seams": ext_nodes,
    "edges": edge_list,
    "groupEdges": group_edges,
    "groups": {gid: {"name": g["name"], "color": GROUP_COLORS[gid]} for gid, g in groups.items()},
    "groupColor": GROUP_COLORS,
    "extColor": "#b48a3c"
}

data_json = json.dumps(payload, ensure_ascii=False)
with open(HTML, "r", encoding="utf-8") as f:
    content = f.read()

if "__DATA__" not in content:
    print("[ERR] __DATA__ placeholder not found")
    raise SystemExit(1)

content = content.replace("__DATA__", data_json)
with open(HTML, "w", encoding="utf-8") as f:
    f.write(content)

print(f"[OK] injected DATA: plugins={len(plugin_nodes)}, seams={len(ext_nodes)}, edges={len(edge_list)}, groupEdges={len(group_edges)}")
