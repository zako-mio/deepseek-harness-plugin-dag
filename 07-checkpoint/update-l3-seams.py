#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S2 补充: 从 L3 全部采集产物自动回填 external-seams.json 的 referred_by
扫描 stage-01-l3-r1~r5.json 中所有 depends_on.plugin_id,
凡命中 external-seams.json 中 seam id 的, 累计 referred_by (去重) 与 mechanisms。
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag"
CHK = os.path.join(BASE, "07-checkpoint")
SEAMS = os.path.join(BASE, "01-dag-data", "external-seams.json")

with open(SEAMS, "r", encoding="utf-8") as f:
    seams_data = json.load(f)
seams_by_id = {s["id"]: s for s in seams_data["seams"]}

# 收集所有 L3 插件 id -> depends_on 列表
plugin_deps = {}   # plugin_id -> [ (dep_id, mechanism) ]
for r in ["r1", "r2", "r3", "r4", "r5"]:
    fp = os.path.join(CHK, f"stage-01-l3-{r}.json")
    with open(fp, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data if isinstance(data, list) else data.get("plugins", [])
    for p in items:
        if not isinstance(p, dict) or "id" not in p:
            continue
        pid = p["id"]
        if pid not in plugin_deps:
            plugin_deps[pid] = []
        for dep in p.get("depends_on", []):
            dep_id = dep.get("plugin_id", "").strip()
            if not dep_id:
                continue
            if dep_id.startswith("@deepseek-ai/"):
                dep_id = dep_id[len("@deepseek-ai/"):]
            plugin_deps[pid].append((dep_id, dep.get("mechanism", "E1")))

# 回填: 凡 L3 插件 depends_on 命中 seam -> referred_by += plugin_id
updated = 0
for pid, deps in plugin_deps.items():
    for dep_id, mech in deps:
        if dep_id not in seams_by_id:
            continue
        seam = seams_by_id[dep_id]
        refs = set(seam.get("referred_by", []))
        mechs = set(seam.get("mechanisms", []))
        changed = False
        if pid not in refs:
            refs.add(pid)
            changed = True
        m = mech.replace("+", "/").split("/")[0].strip().upper()
        if m in ("E1", "E2", "E3") and m not in mechs:
            mechs.add(m)
            changed = True
        if changed:
            seam["referred_by"] = sorted(refs)
            seam["ref_count"] = len(refs)
            seam["mechanisms"] = sorted(mechs)
            updated += 1
            print(f"[INFO] seam {dep_id} <- {pid} (mech {mech}): refs={len(refs)}")

with open(SEAMS, "w", encoding="utf-8") as f:
    json.dump(seams_data, f, ensure_ascii=False, indent=2)

print(f"\n[OK] seams updated: {updated} entries touched")
print(f"[OK] total seams: {len(seams_data['seams'])}")
