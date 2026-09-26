# -*- coding: utf-8 -*-
"""S2b: 查 23 个未覆盖插件的信息（名称/组/层/权重）"""
import json, os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
sys.stdout.reconfigure(encoding="utf-8")

with open(os.path.join(BASE, "01-dag-data", "webapp-dag.json"), encoding="utf-8") as f:
    dag = json.load(f)
with open(os.path.join(BASE, "07-checkpoint", "research", "aggregated.json"), encoding="utf-8") as f:
    agg = json.load(f)

covered = set(agg["plugins"].keys())
for n in dag["nodes"]:
    if n["id"] not in covered:
        print(f"{n['id']:<32} {n.get('group_name','?'):<12} 层:{n.get('layer',-1)}")
