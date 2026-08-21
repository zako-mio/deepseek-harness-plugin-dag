# -*- coding: utf-8 -*-
"""S0: DAG 重要性权重计算
读 01-dag-data/webapp-dag.json，计算每个插件的：
- 被依赖数（下游消费者数，即作为 target 被多少边引用）
- 依赖数（上游数，即作为 source 的边数）
- 拓扑层
- 组
按权重分级：核心（深度why）/ 普通 / 轻量（简版why）
"""
import json, os, sys, collections

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0822-plugin-dag-v0.1.1-rc2"
DAG = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
OUT = os.path.join(BASE, "07-checkpoint", "plugin-weight.json")
sys.stdout.reconfigure(encoding="utf-8")

with open(DAG, encoding="utf-8") as f:
    d = json.load(f)

# 结构探查
nodes = d.get("nodes", d) if isinstance(d, dict) else d
edges = d.get("edges", []) if isinstance(d, dict) else []
print(f"nodes: {len(nodes)}, edges: {len(edges)}")
print("node sample:", json.dumps(nodes[0], ensure_ascii=False)[:200] if nodes else "EMPTY")
print("edge sample:", json.dumps(edges[0], ensure_ascii=False)[:200] if edges else "EMPTY")
