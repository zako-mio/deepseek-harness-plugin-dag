# -*- coding: utf-8 -*-
"""S0b: 生成 6 路调研分片清单（按权重+组均衡分配）
输出每路的插件 id 列表，供委派子Agent 时引用
"""
import json, sys, collections

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0822-plugin-dag-v0.1.1-rc2"
sys.stdout.reconfigure(encoding="utf-8")

with open(BASE + r"\07-checkpoint\plugin-weight.json", encoding="utf-8") as f:
    w = json.load(f)

plugins = w["plugins"]
core = [p for p in plugins if p["weight"] == "core"]
normal = [p for p in plugins if p["weight"] == "normal"]
light = [p for p in plugins if p["weight"] == "light"]

# 6 路分片：每路先分 core（均衡），再补 normal/light
buckets = [[] for _ in range(6)]
# 按被依赖数降序轮询分配 core
core_sorted = sorted(core, key=lambda x: -x["depended_count"])
for i, p in enumerate(core_sorted):
    buckets[i % 6].append(p)

# normal 按组尽量同路（同组插件放一路减少重复调研），light 简单填充
# 简化：normal+light 按顺序轮询
rest = normal + light
for i, p in enumerate(rest):
    buckets[i % 6].append(p)

# 输出每路统计与清单
total_ids = set()
for i, b in enumerate(buckets):
    ids = [p["id"] for p in b]
    total_ids.update(ids)
    c = sum(1 for p in b if p["weight"] == "core")
    n = sum(1 for p in b if p["weight"] == "normal")
    l = sum(1 for p in b if p["weight"] == "light")
    print(f"路{i}: {len(b)} 插件 (core {c} / normal {n} / light {l})")
    print(f"  core: {', '.join(x['id'] for x in b if x['weight']=='core')}")

print(f"\n总覆盖: {len(total_ids)} / {len(plugins)}")
miss = [p["id"] for p in plugins if p["id"] not in total_ids]
print(f"遗漏: {miss if miss else '无'}")

# 保存分片
shards = {}
for i, b in enumerate(buckets):
    shards[f"shard{i}"] = [p["id"] for p in b]
with open(BASE + r"\07-checkpoint\shards.json", "w", encoding="utf-8") as f:
    json.dump(shards, f, ensure_ascii=False, indent=2)
print("[OUT] 已写入 shards.json")
