#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 buildDrillElements 数据逻辑: 从 index.html 提取 DATA, 用 Node 跑组内下钻构建"""
import json, os, re

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-plugin-dag-rc8"
HTML = os.path.join(BASE, "04-interactive", "index.html")

with open(HTML, "r", encoding="utf-8") as f:
    content = f.read()

# 提取 const DATA = {...};
m = re.search(r'const DATA = (\{.*?\});\n\n// ---- 数据索引', content, re.DOTALL)
if not m:
    print("DATA not found")
    raise SystemExit(1)

data = json.loads(m.group(1))
print(f"DATA plugins={len(data['plugins'])} seams={len(data['seams'])} edges={len(data['edges'])} groupEdges={len(data['groupEdges'])}")

# 模拟 buildDrillElements('G03')
pluginById = {p["data"]["id"]: p for p in data["plugins"]}
seamById = {s["data"]["id"]: s for s in data["seams"]}
groupMeta = data["groups"]

g3_ids = [p["data"]["id"] for p in data["plugins"] if p["data"]["group"] == "G03"]
in_edges = [e for e in data["edges"] if e["data"]["source"] in g3_ids and e["data"]["target"] in g3_ids]
ext_refs = set()
for e in data["edges"]:
    f, t = e["data"]["source"], e["data"]["target"]
    if f in g3_ids and t not in g3_ids:
        ext_refs.add(t)
    if t in g3_ids and f not in g3_ids:
        ext_refs.add(f)

print(f"G03 插件数: {len(g3_ids)}")
print(f"G03 组内边: {len(in_edges)}")
print(f"G03 跨组外部引用: {len(ext_refs)}")
print(f"  外部引用: {sorted(ext_refs)[:15]}...")

# stub 节点可解析性
missing = [rid for rid in ext_refs if rid not in pluginById and rid not in seamById]
print(f"  stub 无法解析: {missing}")
