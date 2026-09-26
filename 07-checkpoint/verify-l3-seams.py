#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 external-seams.json 追加后合法 + 不破坏既有校验"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
EXT = os.path.join(BASE, "01-dag-data", "external-seams.json")
INV = os.path.join(BASE, "07-checkpoint", "stage-00-l3-inventory.json")

with open(EXT, "r", encoding="utf-8") as f:
    ext = json.load(f)
with open(INV, "r", encoding="utf-8") as f:
    inv = json.load(f)

print(f"[OK] seams: {ext['count']}, actual: {len(ext['seams'])}")

# 校验 id 唯一
ids = [s["id"] for s in ext["seams"]]
dup = len(ids) - len(set(ids))
print(f"[OK] id unique: {len(set(ids))}, dup: {dup}")

# 校验 schema 字段齐全
missing = []
for s in ext["seams"]:
    for field in ["id", "name", "path", "ts_count", "description", "ref_count", "referred_by", "mechanisms"]:
        if field not in s:
            missing.append(f"{s['id']}.{field}")
print(f"[OK] schema missing: {len(missing)} {missing[:5]}")

# 校验 L3 新 seam 存在
l3_ids = [s["id"] for s in inv["l3_seams"]]
missing_l3 = [x for x in l3_ids if x not in ids]
print(f"[OK] L3 seams present: {len(l3_ids) - len(missing_l3)}/{len(l3_ids)}, missing: {missing_l3}")

print("\n[OK] external-seams.json valid")
