#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S2 质量检查: 验证 webapp-dag.json 拓扑合理性 + 关键节点依赖"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0819-plugin-dag-rc7"
DAG = os.path.join(BASE, "01-dag-data", "webapp-dag.json")

with open(DAG, "r", encoding="utf-8") as f:
    dag = json.load(f)

nodes = {n["id"]: n for n in dag["nodes"]}
edges = dag["edges"]
print(f"nodes={len(nodes)} edges={len(edges)} layers={dag['meta']['layer_count']} groups={len(dag['groups'])}")

# 检查关键节点的依赖完整性
key_checks = {
    "dsh-web-app": ["dsh-host-webserver", "dsh-system-prompt", "dsh-shell-env"],
    "dsh-client-connection": ["dsh-host-apiproxy", "dsh-host-webserver"],
    "dsh-client-runtime": ["dsh-client-connection", "dsh-api-remotes"],
    "dsh-client-web": ["dsh-client-modules", "dsh-client-runtime", "dsh-client-web-react"],
    "dsh-host-apiproxy": ["dsh-session", "dsh-agent", "dsh-llm"],
    "dsh-client-ui-conversation": ["dsh-client-runtime", "dsh-client-ui-layout", "dsh-client-locale"],
    "dsh-client-ui-tool": ["dsh-client-ui-conversation", "dsh-client-runtime"],
}

out_edges = {}
for e in edges:
    out_edges.setdefault(e["from"], []).append(e["to"])

print("\n=== 关键节点上游依赖 ===")
for nid, expected in key_checks.items():
    deps = set(out_edges.get(nid, []))
    missing = [d for d in expected if d not in deps]
    status = "OK" if not missing else f"MISSING: {missing}"
    print(f"  {nid}: deps={len(deps)} {status}")

# 检查节点层 vs 依赖层约束 (依赖层 < 依赖方层)
print("\n=== 拓扑一致性 (依赖方层 > 被依赖方层) ===")
violations = []
for e in edges:
    f, t = e["from"], e["to"]
    if f in nodes and t in nodes:
        if nodes[f]["layer"] <= nodes[t]["layer"]:
            violations.append((f, nodes[f]["layer"], t, nodes[t]["layer"]))
print(f"violations: {len(violations)}")
for v in violations[:10]:
    print(f"  {v[0]}(L{v[1]}) -> {v[2]}(L{v[3]})")

# L2 节点覆盖
l2_nodes = [n for n in dag["nodes"] if n.get("source_layer") == "L2"]
print(f"\nL2 nodes: {len(l2_nodes)}")

# 组分布
from collections import Counter
group_counts = Counter(n["group"] for n in dag["nodes"])
print("组分布:", dict(sorted(group_counts.items())))
