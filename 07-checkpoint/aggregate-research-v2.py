# -*- coding: utf-8 -*-
"""S2a: 聚合 6 路调研结果 v2（支持字典/数组混合结构）"""
import json, os, sys, glob

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-plugin-dag-rc8"
RES = os.path.join(BASE, "07-checkpoint", "research")
sys.stdout.reconfigure(encoding="utf-8")

def extract_items(obj):
    """递归提取所有 {'id': ...} 字典"""
    out = []
    if isinstance(obj, dict):
        if "id" in obj and isinstance(obj.get("id"), str):
            out.append(obj)
        for v in obj.values():
            out.extend(extract_items(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(extract_items(v))
    return out

all_nodes = {}
for p in glob.glob(os.path.join(RES, "shard*.json")):
    with open(p, encoding="utf-8") as f:
        data = json.load(f)
    for it in extract_items(data):
        if it.get("id"):
            all_nodes[it["id"]] = it

print(f"总覆盖插件: {len(all_nodes)}")
full = [i for i, v in all_nodes.items() if v.get("why")]
short = [i for i, v in all_nodes.items() if v.get("why_short") and not v.get("why")]
missing = [i for i, v in all_nodes.items() if not v.get("why") and not v.get("why_short")]
print(f"深度 why: {len(full)} / 简版 why_short: {len(short)} / 无: {len(missing)} -> {missing[:10]}")

# 与 webapp-dag.json 的 173 节点对比
with open(os.path.join(BASE, "01-dag-data", "webapp-dag.json"), encoding="utf-8") as f:
    dag = json.load(f)
dag_ids = {n["id"] for n in dag["nodes"]}
covered = set(all_nodes.keys())
not_covered = dag_ids - covered
extra = covered - dag_ids
print(f"DAG 节点: {len(dag_ids)} / 调研覆盖: {len(covered)} / 未覆盖: {len(not_covered)} -> {sorted(not_covered)[:10]}")
print(f"多余(不在DAG): {sorted(extra)}")

with open(os.path.join(RES, "aggregated.json"), "w", encoding="utf-8") as f:
    json.dump({"meta": {"total": len(all_nodes), "full": len(full), "short": len(short), "missing": missing, "not_covered": sorted(not_covered)}, "plugins": all_nodes}, f, ensure_ascii=False, indent=2)
print("[OUT] aggregated.json v2")
