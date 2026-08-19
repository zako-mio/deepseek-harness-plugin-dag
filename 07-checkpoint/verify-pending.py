#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 pending.json 合法性与计数"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

fp = r"D:\Opencode_Download\Reflection\pending.json"
with open(fp, "r", encoding="utf-8") as f:
    d = json.load(f)

print(f"meta: {d['meta']}")
statuses = {}
for c in d["cycles"]:
    statuses[c["status"]] = statuses.get(c["status"], 0) + 1
print(f"cycle statuses: {statuses}")
print(f"total cycles: {len(d['cycles'])}")
print("[OK] JSON valid")
