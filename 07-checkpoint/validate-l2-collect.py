#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 4 路 L2 采集 JSON 合法性与 58 节点覆盖"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

CHK = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-plugin-dag-rc8\07-checkpoint"
INV = os.path.join(CHK, "stage-00-l2-inventory.json")

with open(INV, "r", encoding="utf-8") as f:
    inv = json.load(f)

# 期望的 58 节点 id
expected = set()
for g in inv["groups"]:
    for p in g["plugins"]:
        expected.add(p["id"])

all_plugins = {}
for r in ["r1", "r2", "r3", "r4"]:
    fp = os.path.join(CHK, f"stage-01-l2-{r}.json")
    with open(fp, "r", encoding="utf-8") as f:
        data = json.load(f)
    for p in data["plugins"]:
        if p["id"] in all_plugins:
            print(f"[WARN] duplicate: {p['id']}")
        all_plugins[p["id"]] = p
    print(f"[OK] {r}: {len(data['plugins'])} plugins")

print(f"\n[INFO] total unique: {len(all_plugins)}")
missing = expected - set(all_plugins.keys())
extra = set(all_plugins.keys()) - expected
print(f"[INFO] expected: {len(expected)}, missing: {len(missing)}, extra: {len(extra)}")
for m in sorted(missing):
    print(f"  [MISSING] {m}")
for e in sorted(extra):
    print(f"  [EXTRA] {e}")

# 检查每条依赖是否有 evidence
no_evidence = []
for pid, p in all_plugins.items():
    for dep in p.get("depends_on", []):
        if not dep.get("evidence"):
            no_evidence.append(f"{pid} -> {dep.get('plugin_id')}")
print(f"\n[INFO] depends_on entries missing evidence: {len(no_evidence)}")
for n in no_evidence[:10]:
    print(f"  {n}")

# 检查 mechanism 合法性
bad_mech = []
for pid, p in all_plugins.items():
    for dep in p.get("depends_on", []):
        if dep.get("mechanism") not in ("E1", "E2", "E3"):
            bad_mech.append(f"{pid} -> {dep.get('plugin_id')}: {dep.get('mechanism')}")
print(f"[INFO] bad mechanism: {len(bad_mech)}")

print("\n[OK] validation complete")
