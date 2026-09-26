#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P2 回盘复验：21 个分片输出 vs 输入对账"""
import json, os, sys, glob, re
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCRIPT_DIR, "v017")
idx = json.load(open(os.path.join(OUT, "shards-index.json"), encoding="utf-8"))
cls = json.load(open(os.path.join(OUT, "classification.json"), encoding="utf-8"))
facts = json.load(open(os.path.join(OUT, "facts.json"), encoding="utf-8"))

expect = {s["shard"]: s for s in idx["shards"]}
EXCLUDE_TARGETS = {"dsh-base", "dsh-headless", "dsh-web-app", "dsh-acp-app", "dsh-sdk-app",
                   "dsh-sdk-minimal", "dsh-app-boot", "dsh-cmdline"}

errors, warns = [], []
all_out = {}
for sid, s in sorted(expect.items()):
    fp = os.path.join(OUT, f"stage-01-{sid}.json")
    if not os.path.isfile(fp):
        errors.append(f"MISSING {sid}")
        continue
    try:
        d = json.load(open(fp, encoding="utf-8"))
    except Exception as e:
        errors.append(f"INVALID JSON {sid}: {e}")
        continue
    if not isinstance(d, list):
        errors.append(f"NOT LIST {sid}")
        continue
    got = [x.get("id") for x in d]
    if len(got) != s["count"]:
        errors.append(f"COUNT {sid}: in={s['count']} out={len(got)}")
    missing = set(s["ids"]) - set(got)
    extra = set(got) - set(s["ids"])
    if missing:
        errors.append(f"IDS missing {sid}: {sorted(missing)}")
    if extra:
        errors.append(f"IDS extra {sid}: {sorted(extra)}")
    for x in d:
        all_out[x["id"]] = x

print(f"shards expected={len(expect)} got={len(glob.glob(os.path.join(OUT,'stage-01-shard-*.json')))}")
print(f"entries collected={len(all_out)} / nodes={len(cls['nodes'])}")

n_edges = 0
bad_ev, selfloop, ex_target = 0, 0, 0
unknown_targets = Counter()
type_only = 0
edge_set = set()
for pid, x in all_out.items():
    for dp in x.get("depends_on", []):
        tgt = dp.get("plugin_id")
        n_edges += 1
        if tgt == pid:
            selfloop += 1
        if tgt in EXCLUDE_TARGETS:
            ex_target += 1
        if tgt not in facts:
            unknown_targets[tgt] += 1
        ev = dp.get("evidence", "")
        if not re.search(r":\d+", ev):
            bad_ev += 1
        if "type-only" in ev.lower() or "import type" in ev:
            type_only += 1
        edge_set.add((pid, tgt))

print(f"\nedges raw={n_edges} unique_pairs={len(edge_set)}")
print(f"self-loops={selfloop}  assembly-framework targets={ex_target}  bad-evidence={bad_ev}  type-only-evidence={type_only}")
print(f"targets not in repo packages: {len(unknown_targets)}")
for t, n in unknown_targets.most_common(20):
    print(f"   {t} x{n}")

# 覆盖：节点中无 depends_on 的
no_dep = [p for p in cls["nodes"] if not all_out.get(p, {}).get("depends_on")]
print(f"\nnodes with 0 depends_on: {len(no_dep)}  {no_dep[:15]}")
# implementation 为空
empty_impl = [p for p, x in all_out.items() if not (x.get("implementation") or "").strip()]
print(f"empty implementation: {len(empty_impl)} {empty_impl[:10]}")

print("\n=== ERRORS ===")
for e in errors:
    print(" ", e)
if not errors:
    print("  none")
