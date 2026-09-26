#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v0.1.7-rc.2 分片生成：把 239 个节点按组打包成 ~14 个/片的委派分片"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCRIPT_DIR, "v017")
SHARDS_DIR = os.path.join(OUT, "shards")
os.makedirs(SHARDS_DIR, exist_ok=True)

cls = json.load(open(os.path.join(OUT, "classification.json"), encoding="utf-8"))
facts = json.load(open(os.path.join(OUT, "facts.json"), encoding="utf-8"))
inv = json.load(open(os.path.join(OUT, "inventory.json"), encoding="utf-8"))
ts_files_map = {k: v.get("ts_files", []) for k, v in inv["packages"].items()}

PER_SHARD = 14

# 按组分片；大组内部再切
units = []
for g in cls["groups"]:
    pids = g["plugins"]
    for i in range(0, len(pids), PER_SHARD):
        chunk = pids[i:i + PER_SHARD]
        units.append({"group": g["id"], "group_name": g["name"], "plugins": chunk})

# 小组两两合并（<8 且同域邻接）
merged = []
buf = None
for u in units:
    if buf is None:
        buf = u
        continue
    if len(buf["plugins"]) < 8 and buf["group"] != u["group"]:
        buf = {"group": f"{buf['group']}+{u['group']}", "group_name": f"{buf['group_name']} / {u['group_name']}",
               "plugins": buf["plugins"] + u["plugins"]}
        if len(buf["plugins"]) >= PER_SHARD:
            merged.append(buf); buf = None
    else:
        merged.append(buf); buf = u
if buf:
    merged.append(buf)

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
                   "input": f"07-checkpoint/v017/shards/{sid}.json",
                   "output": f"07-checkpoint/v017/stage-01-{sid}.json"})

with open(os.path.join(OUT, "shards-index.json"), "w", encoding="utf-8") as fh:
    json.dump({"per_shard": PER_SHARD, "total_nodes": len(facts) and sum(s["count"] for s in shards), "shards": shards}, fh, ensure_ascii=False, indent=1)

print(f"shards: {len(shards)}, total plugins covered: {sum(s['count'] for s in shards)}")
for s in shards:
    print(f"  {s['shard']}  {s['group_name']:24s} n={s['count']:2d}  {', '.join(s['ids'][:4])}{' ...' if s['count']>4 else ''}")
print(f"\n[OK] shards written to {SHARDS_DIR}")
