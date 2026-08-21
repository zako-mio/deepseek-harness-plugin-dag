# -*- coding: utf-8 -*-
"""S2a: 聚合 6 路调研结果，验证覆盖度与完整性"""
import json, os, sys, glob

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0822-plugin-dag-v0.1.1-rc2"
RES = os.path.join(BASE, "07-checkpoint", "research")
sys.stdout.reconfigure(encoding="utf-8")

all_nodes = {}
for p in glob.glob(os.path.join(RES, "shard*.json")):
    with open(p, encoding="utf-8") as f:
        data = json.load(f)
    # 结构可能是 {items:[...]} 或 {plugins:[...]} 或 {shardX:[...]} 或直接数组
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for k in ("items", "plugins", "results", "nodes", "data"):
            if k in data and isinstance(data[k], list):
                items = data[k]
                break
        else:
            # 兜底：取所有值是 list 的键
            for k, v in data.items():
                if isinstance(v, list) and v and isinstance(v[0], dict) and "id" in v[0]:
                    items = v
                    break
    for it in items:
        if isinstance(it, dict) and "id" in it:
            all_nodes[it["id"]] = it

print(f"总覆盖插件: {len(all_nodes)}")
print(f"keys 样本: {list(all_nodes.values())[0].keys() if all_nodes else 'EMPTY'}")

# 检查 CORE 插件是否都有 why/history/sources
missing_why = [i for i, v in all_nodes.items() if not v.get("why") and not v.get("why_short")]
print(f"缺 why/why_short: {len(missing_why)} -> {missing_why[:10]}")

# 统计 why 完整 vs why_short
full = [i for i, v in all_nodes.items() if v.get("why")]
short = [i for i, v in all_nodes.items() if v.get("why_short") and not v.get("why")]
print(f"深度 why: {len(full)} / 简版 why_short: {len(short)} / 无: {len(missing_why)}")

# 保存聚合
with open(os.path.join(RES, "aggregated.json"), "w", encoding="utf-8") as f:
    json.dump({"meta": {"total": len(all_nodes), "full": len(full), "short": len(short), "missing": missing_why}, "plugins": all_nodes}, f, ensure_ascii=False, indent=2)
print("[OUT] aggregated.json")
