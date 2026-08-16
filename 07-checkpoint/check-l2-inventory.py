#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S0 核验: stage-00-l2-inventory.json 的 name/path 与 PACKAGE-MAP.json 交叉检查"""
import json, os

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag"
MAP = r"D:\Opencode_Download\Mission-file\2026-08\0814-deepseek-harness源码解析\07-checkpoint\PACKAGE-MAP.json"
INV = os.path.join(BASE, "07-checkpoint", "stage-00-l2-inventory.json")

with open(INV, "r", encoding="utf-8") as f:
    inv = json.load(f)
with open(MAP, "r", encoding="utf-8") as f:
    pkgmap = json.load(f)

pkg_by_name = {p["name"]: p for p in pkgmap["packages"]}
print(f"[INFO] PACKAGE-MAP packages: {len(pkgmap['packages'])}")

issues = []
missing = []
ok = 0
total = 0
for g in inv["groups"]:
    for p in g["plugins"]:
        total += 1
        full = p["name"]
        meta = pkg_by_name.get(full)
        if meta is None:
            missing.append(f"{full} (row={p.get('row_id')})")
            continue
        expected = "packages/" + full[len("@deepseek-ai/"):].replace("-", "/", 1) if False else None
        # 直接比较 path
        if meta["path"] != p["path"]:
            issues.append(f"PATH MISMATCH {full}: inv={p['path']} map={meta['path']}")
        ok += 1

print(f"[INFO] total={total} ok={ok} missing={len(missing)} path_mismatch={len(issues)}")
for m in missing:
    print(f"  [MISSING] {m}")
for i in issues:
    print(f"  [ISSUE] {i}")
