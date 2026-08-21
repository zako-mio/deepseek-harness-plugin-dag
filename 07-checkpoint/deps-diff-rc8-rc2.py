#!/usr/bin/env python3
"""
RC8 vs RC2 package.json 依赖 diff（E1）
输出每个包的新增/删除依赖，只关注 workspace 包
"""
import json
from pathlib import Path

OLD = Path("05-source/dsh-rc8")
NEW = Path("05-source/dsh-v0.1.1-rc.2/deepseek-harness-dsh-v0.1.1-rc.2")

def pkg_map(root):
    m = {}
    for domain in (root / "packages").iterdir():
        if not domain.is_dir(): continue
        for p in domain.iterdir():
            pj = p / "package.json"
            if pj.exists():
                m[(domain.name, p.name)] = json.loads(pj.read_text(encoding="utf-8"))
    return m

def deps(pkg):
    d = {}
    for sec in ["dependencies", "peerDependencies", "devDependencies"]:
        d.update(pkg.get(sec, {}))
    return {k: v for k, v in d.items() if k.startswith("@deepseek-ai/") or k.startswith("@cordis")}

old = pkg_map(OLD)
new = pkg_map(NEW)

all_keys = sorted(set(old) | set(new))
changes = []
for key in all_keys:
    if key not in old:
        changes.append({"pkg": key, "status": "added", "deps": list(deps(new[key]).keys())})
        continue
    if key not in new:
        changes.append({"pkg": key, "status": "removed", "deps": []})
        continue
    od = deps(old[key])
    nd = deps(new[key])
    added = sorted(set(nd) - set(od))
    removed = sorted(set(od) - set(nd))
    if added or removed:
        changes.append({"pkg": key, "added": added, "removed": removed})

print(json.dumps(changes, ensure_ascii=False, indent=2))
print(f"\n共 {len(changes)} 个包依赖变化", file=__import__('sys').stderr)
