#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RC8 -> RC2 数据层更新脚本
- 在 webapp-dag.json / external-seams.json 中应用 RC2 的依赖变化
- 不改动历史版本记录
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-plugin-dag-rc8"
DAG = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
SEAMS = os.path.join(BASE, "01-dag-data", "external-seams.json")

with open(DAG, "r", encoding="utf-8") as f:
    dag = json.load(f)
with open(SEAMS, "r", encoding="utf-8") as f:
    seams_data = json.load(f)

nodes = {n["id"]: n for n in dag["nodes"]}
seams = {s["id"]: s for s in seams_data["seams"]}
edges = dag["edges"]

# --- 1. 新增 seam: dsh-authorization ---
if "dsh-authorization" not in seams:
    seams["dsh-authorization"] = {
        "id": "dsh-authorization",
        "name": "@deepseek-ai/dsh-authorization",
        "path": "packages/credentials/authorization",
        "ts_count": 3,
        "description": "Authorization seam (ctx.authorization): plugin-owned flows that obtain a credential through a conversation with the human",
        "ref_count": 1,
        "referred_by": ["dsh-llm-pi-ai"],
        "mechanisms": ["E1"]
    }
    print("[INFO] added seam dsh-authorization")

# --- 2. 更新现有 seam referred_by ---
updates = {
    "dsh-atomic-write": ["dsh-llm-deepseek"],
    "dsh-brand": ["dsh-llm-deepseek"],
    "dsh-home-paths": ["dsh-llm-deepseek"],
}
for sid, refs in updates.items():
    if sid not in seams:
        print(f"[WARN] seam {sid} not found, skipping")
        continue
    s = seams[sid]
    existing = set(s.get("referred_by", []))
    added = []
    for r in refs:
        if r not in existing:
            existing.add(r)
            added.append(r)
    if added:
        s["referred_by"] = sorted(existing)
        s["ref_count"] = len(existing)
        s["mechanisms"] = sorted(set(s.get("mechanisms", [])) | {"E1"})
        print(f"[INFO] seam {sid}: +referred_by {added} -> {len(existing)}")

# --- 3. 检查 webapp-dag.json 边是否需要新增 ---
# dsh-llm-deepseek 新增到 seam 的依赖不入 webapp-dag.edges（纯 seam 边通过 external-seams 表达）
# dsh-llm-pi-ai -> dsh-authorization 也是 seam 边
# 因此 webapp-dag.json 节点/边数不变

# --- 4. 更新 meta 版本标注 ---
dag["meta"]["generated_at"] = "2026-08-21"
dag["meta"]["source"] = "webapp-dag.json (L1+L2+L3, RC8 baseline) + RC2 dependency diff update"
# 保持 plugin_count/edge_count/layer_count/group_count 不变

# --- 写回 ---
with open(DAG, "w", encoding="utf-8") as f:
    json.dump(dag, f, ensure_ascii=False, indent=2)

seams_data["count"] = len(seams)
seams_data["seams"] = sorted(seams.values(), key=lambda s: s["id"])
with open(SEAMS, "w", encoding="utf-8") as f:
    json.dump(seams_data, f, ensure_ascii=False, indent=2)

print(f"[INFO] webapp-dag.json: {len(nodes)} nodes, {len(edges)} edges")
print(f"[INFO] external-seams.json: {len(seams)} seams")
print("[INFO] done")
