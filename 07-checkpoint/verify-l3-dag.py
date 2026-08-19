#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S2 验证: webapp-dag.json + external-seams.json JSON 合法 + DAG 无环 + 39 L3 节点覆盖"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0819-plugin-dag-rc7"
DAG = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
SEAMS = os.path.join(BASE, "01-dag-data", "external-seams.json")

with open(DAG, "r", encoding="utf-8") as f:
    dag = json.load(f)
with open(SEAMS, "r", encoding="utf-8") as f:
    seams = json.load(f)

print(f"[OK] webapp-dag.json valid JSON: {len(dag['nodes'])} nodes, {len(dag['edges'])} edges, {len(dag['groups'])} groups, {len(dag['layers'])} layers")
print(f"[OK] external-seams.json valid JSON: {len(seams['seams'])} seams")

# L3 节点 (source_layer == L3)
l3_nodes = [n for n in dag["nodes"] if n.get("source_layer") == "L3"]
print(f"[OK] L3 nodes: {len(l3_nodes)}")
missing_l3 = set()
for n in l3_nodes:
    if n["group"] not in {g["id"] for g in dag["groups"]}:
        missing_l3.add(n["group"])
if missing_l3:
    print(f"[WARN] L3 nodes with unknown group: {missing_l3}")
else:
    print("[OK] all L3 nodes have valid group")

# 期望的 39 个 L3 插件 id
expected = {
    "dsh-fs-e2b","dsh-subprocess-e2b","dsh-terminal-bash","dsh-tool-terminal","dsh-tool-bash-persistent","dsh-schedule",
    "dsh-sdk-client","dsh-sdk-jsonrpc-server",
    "dsh-lsp-stdio","dsh-tool-lsp",
    "dsh-subagent-acp","dsh-subagent-claude-code","dsh-subagent-codex","dsh-subagent-dsh-sdk",
    "dsh-web-fetch-http","dsh-web-search-exa","dsh-web-search-perplexity","dsh-session-reference","dsh-time-context","dsh-tmux-context",
    "dsh-session-persistence-sqlite","dsh-storage-sqlite","dsh-session-title-all-prompts-llm","dsh-tool-session-query",
    "dsh-hooks-claude-code","dsh-hooks-codex","dsh-tool-cordis","dsh-tool-ask-user","dsh-persona","dsh-agent-tool-presentation",
    "dsh-acp-demo","dsh-agent-spine-demo","dsh-sdk-jsonrpc-demo","dsh-typert-generator","dsh-native-command",
    "dsh-host-frontend-static","dsh-host-directory-picker","dsh-host-directory-picker-browse","dsh-host-directory-picker-native",
}
node_ids = {n["id"] for n in dag["nodes"]}
miss = expected - node_ids
extra = node_ids - expected - {n["id"] for n in dag["nodes"] if n.get("source_layer") != "L3"}
if miss:
    print(f"[ERROR] missing expected L3: {sorted(miss)}")
else:
    print(f"[OK] all {len(expected)} expected L3 plugin ids present")

# 无环校验
indeg = {n["id"]: 0 for n in dag["nodes"]}
adj = {n["id"]: [] for n in dag["nodes"]}
for e in dag["edges"]:
    if e["to"] not in adj or e["from"] not in adj:
        print(f"[ERROR] edge refs unknown node: {e['from']}->{e['to']}")
        continue
    adj[e["to"]].append(e["from"])
    indeg[e["from"]] += 1
queue = [pid for pid in indeg if indeg[pid] == 0]
processed = 0
while queue:
    nxt = []
    for pid in queue:
        processed += 1
        for child in adj[pid]:
            indeg[child] -= 1
            if indeg[child] == 0:
                nxt.append(child)
    queue = nxt
if processed != len(indeg):
    print(f"[ERROR] CYCLE: {len(indeg)-processed} nodes in cycle")
else:
    print(f"[OK] DAG acyclic: {processed}/{len(indeg)} nodes processed")

# seam referred_by 非空统计
non_empty = sum(1 for s in seams["seams"] if s.get("referred_by"))
print(f"[OK] seams with referred_by: {non_empty}/{len(seams['seams'])}")

# 特殊模块 (不进 DAG, 单独节)
print("\n=== 特殊模块 (独立分析, 非 DAG 节点) ===")
import glob
for fp in glob.glob(os.path.join(BASE, "07-checkpoint", "stage-01-l3-r4.json")):
    with open(fp, "r", encoding="utf-8") as f:
        r4 = json.load(f)
    for sm in r4.get("special_modules", []):
        print(f"  {sm['id']} [{sm.get('kind','?')}]: {sm.get('assembly_summary','')[:60]}...")
