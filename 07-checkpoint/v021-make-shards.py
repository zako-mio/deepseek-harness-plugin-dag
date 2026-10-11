#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v0.2.1-alpha.2 分片生成（增量版）：**只对 redo 集合**分片，复用节点不进分片。

redo 来源：07-checkpoint/v021/reuse-map.json（v021-merge-reuse.py 产出）。
分片策略沿用 v017：按组切 ~PER_SHARD 个/片，小组同域邻接合并。
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCRIPT_DIR, "v021")
SHARDS_DIR = os.path.join(OUT, "shards")
os.makedirs(SHARDS_DIR, exist_ok=True)

cls = json.load(open(os.path.join(OUT, "classification.json"), encoding="utf-8"))
facts = json.load(open(os.path.join(OUT, "facts.json"), encoding="utf-8"))
inv = json.load(open(os.path.join(OUT, "inventory.json"), encoding="utf-8"))
rm = json.load(open(os.path.join(OUT, "reuse-map.json"), encoding="utf-8"))
ts_files_map = {k: v.get("ts_files", []) for k, v in inv["packages"].items()}

REDO = set(rm["redo"])
PER_SHARD = 14

units = []
for g in cls["groups"]:
    pids = [p for p in g["plugins"] if p in REDO]
    for i in range(0, len(pids), PER_SHARD):
        units.append({"group": g["id"], "group_name": g["name"], "plugins": pids[i:i + PER_SHARD]})

# 小组两两合并（<8 且跨组邻接）
merged, buf = [], None
for u in units:
    if buf is None:
        buf = u
        continue
    if len(buf["plugins"]) < 8 and buf["group"] != u["group"]:
        buf = {"group": f"{buf['group']}+{u['group']}",
               "group_name": f"{buf['group_name']} / {u['group_name']}",
               "plugins": buf["plugins"] + u["plugins"]}
        if len(buf["plugins"]) >= PER_SHARD:
            merged.append(buf); buf = None
    else:
        merged.append(buf); buf = u
if buf:
    merged.append(buf)

# 尾部碎片（<8）并入上一片，避免出现只有 1-2 个插件的分片浪费一次委派
if len(merged) >= 2 and len(merged[-1]["plugins"]) < 8:
    tail = merged.pop()
    merged[-1] = {"group": f"{merged[-1]['group']}+{tail['group']}",
                  "group_name": f"{merged[-1]['group_name']} / {tail['group_name']}",
                  "plugins": merged[-1]["plugins"] + tail["plugins"]}

shards = []
for i, u in enumerate(merged, 1):
    sid = f"shard-{i:02d}"
    items = []
    for pid in u["plugins"]:
        f = facts[pid]
        items.append({
            "id": pid, "name": f["name"], "path": f["path"], "domain": f["domain"],
            "ts_count": f["ts_count"], "ts_files": ts_files_map.get(pid, []),
            "assembled_in": f["assembled_in"],
            "declared": f["declared"],
            "imports": f["imports"],
            "injects": f["injects"],
            "ctx_services": f["ctx_services"],
            "events_on": f["events_on"],
            "events_emit": f["events_emit"],
            "provides_hints": f["provides_hints"],
        })
    payload = {"shard": sid, "group": u["group"], "group_name": u["group_name"], "plugins": items}
    with open(os.path.join(SHARDS_DIR, f"{sid}.json"), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
    shards.append({"shard": sid, "group": u["group"], "group_name": u["group_name"],
                   "count": len(items), "ids": [x["id"] for x in items],
                   "input": f"07-checkpoint/v021/shards/{sid}.json",
                   "output": f"07-checkpoint/v021/stage-01-{sid}.json"})

total = sum(s["count"] for s in shards)
with open(os.path.join(OUT, "shards-index.json"), "w", encoding="utf-8") as fh:
    json.dump({"per_shard": PER_SHARD, "total_nodes": total, "reused": len(rm["reused"]),
               "shards": shards}, fh, ensure_ascii=False, indent=1)

print(f"shards: {len(shards)}, redo plugins covered: {total} (reused elsewhere: {len(rm['reused'])})")
for s in shards:
    print(f"  {s['shard']}  {s['group_name']:28s} n={s['count']:2d}  {', '.join(s['ids'][:3])}{' ...' if s['count']>3 else ''}")
print(f"\n[OK] shards written to {SHARDS_DIR}")
