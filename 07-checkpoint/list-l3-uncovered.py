#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L3 S0: 比对 PACKAGE-MAP 219 包 vs 已分析 (L1 76 + L2 58 + seam 36) → 未覆盖包清单"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

MAP = r"D:\Opencode_Download\Mission-file\2026-08\0814-deepseek-harness源码解析\07-checkpoint\PACKAGE-MAP.json"
DAG = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-plugin-dag-rc8\01-dag-data\webapp-dag.json"
EXT = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-plugin-dag-rc8\01-dag-data\external-seams.json"

with open(MAP, "r", encoding="utf-8") as f:
    pkgmap = json.load(f)
with open(DAG, "r", encoding="utf-8") as f:
    dag = json.load(f)
with open(EXT, "r", encoding="utf-8") as f:
    ext = json.load(f)

all_pkgs = {p["name"]: p for p in pkgmap["packages"]}
analyzed_names = set()
for n in dag["nodes"]:
    analyzed_names.add(n["name"])
for s in ext["seams"]:
    analyzed_names.add(s["name"])

# 例外: cordis-plugin-timer/hmr 是 vendor 包, name 是 @deepseek-ai/cordis-plugin-timer
print(f"[INFO] PACKAGE-MAP: {len(all_pkgs)} 包, 已分析: {len(analyzed_names)}")

uncovered = []
for name, p in all_pkgs.items():
    if name not in analyzed_names:
        uncovered.append(p)

print(f"[INFO] 未覆盖包: {len(uncovered)}")
print(f"\n=== 未覆盖包按域分组 ===")
from collections import defaultdict
domains = defaultdict(list)
for p in uncovered:
    parts = p["path"].split("/")
    domain = parts[1] if len(parts) > 1 else "?"
    domains[domain].append((p["name"], p["path"], p.get("ts_count", 0)))

for dom in sorted(domains.keys()):
    items = domains[dom]
    print(f"\n[{dom}] {len(items)} 个")
    for name, path, ts in sorted(items, key=lambda x: x[0]):
        print(f"  {name}  @ {path} ({ts} ts)")
