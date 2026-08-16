#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析 stage-01 数据中 appears in depends_on 但不在 76 集合内的外部 seam 包"""
import json, os, glob, collections

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag"
CHK = os.path.join(BASE, "07-checkpoint")

# 收集所有 depends_on 引用
refs = collections.Counter()
for fp in glob.glob(os.path.join(CHK, "stage-01-r*.json")):
    with open(fp, "r", encoding="utf-8") as f:
        data = json.load(f)
    for p in data["plugins"]:
        for d in p.get("depends_on", []):
            pid = d.get("plugin_id", "")
            if pid.startswith("@deepseek-ai/"):
                pid = pid[len("@deepseek-ai/"):]
            if "/" in pid:
                pid = pid.split("/")[0]
            if pid.startswith("dsh-") or pid.startswith("cordis-plugin-"):
                refs[pid] += 1

# 76 集合内 id
with open(os.path.join(BASE, "01-dag-data", "core-dag.json"), "r", encoding="utf-8") as f:
    dag = json.load(f)
node_ids = {n["id"] for n in dag["nodes"]}

print("出现在 depends_on 但不在 76 集合内的官方包 (外部 seam):")
external = sorted([k for k in refs if k not in node_ids], key=lambda x: (-refs[x], x))
for k in external:
    print(f"  {k} x{refs[k]}")
print(f"\n外部 seam 包数量: {len(external)}")
