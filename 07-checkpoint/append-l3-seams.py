#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L3 S0: 追加 13 个 L3 seam 到 external-seams.json (schema 同现有 36 个)"""
import json, os, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
sys.stdout.reconfigure(encoding='utf-8')

EXT = os.path.join(BASE, '01-dag-data', 'external-seams.json')
MAP = r"D:\Opencode_Download\Mission-file\2026-08\0814-deepseek-harness源码解析\07-checkpoint\PACKAGE-MAP.json"
INV = os.path.join(BASE, '07-checkpoint', 'stage-00-l3-inventory.json')

with open(EXT, "r", encoding="utf-8") as f:
    ext = json.load(f)
with open(MAP, "r", encoding="utf-8") as f:
    pkgmap = json.load(f)
with open(INV, "r", encoding="utf-8") as f:
    inv = json.load(f)

pkg_by_name = {p["name"]: p for p in pkgmap["packages"]}
existing_ids = {s["id"] for s in ext["seams"]}

added = []
for s in inv["l3_seams"]:
    if s["id"] in existing_ids:
        print(f"[SKIP] {s['id']} already exists")
        continue
    meta = pkg_by_name.get(s["name"], {})
    desc = meta.get("description", "") or f"{s['note']} seam"
    # description 若为空用 note
    new_seam = {
        "id": s["id"],
        "name": s["name"],
        "path": s["path"],
        "ts_count": s["ts_count"],
        "description": desc,
        "ref_count": 0,
        "referred_by": [],
        "mechanisms": [],
        "l3_note": s["note"]
    }
    ext["seams"].append(new_seam)
    added.append(s["id"])

ext["count"] = len(ext["seams"])

with open(EXT, "w", encoding="utf-8") as f:
    json.dump(ext, f, ensure_ascii=False, indent=2)

print(f"[OK] added {len(added)} seams: {added}")
print(f"[OK] external-seams.json now: {ext['count']} seams")
