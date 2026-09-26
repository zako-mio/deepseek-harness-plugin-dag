#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RC2 → 0.1.7-rc.2 包级结构差异（从 05-source 两个树重算，供差异报告引用）"""
import os, sys, json, hashlib
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
OLD = os.path.join(BASE, "05-source", "dsh-v0.1.1-rc.2", "deepseek-harness-dsh-v0.1.1-rc.2")
NEW = os.path.join(BASE, "05-source", "dsh-v0.1.7-rc.2", "deepseek-harness-dsh-v0.1.7-rc.2")
SKIP = {"node_modules", "dist", "lib", "build", ".turbo", "coverage"}


def pkg_list(root):
    out = {}
    base = os.path.join(root, "packages")
    for d1 in sorted(os.listdir(base)):
        p1 = os.path.join(base, d1)
        if not os.path.isdir(p1):
            continue
        for d2 in sorted(os.listdir(p1)):
            p2 = os.path.join(p1, d2)
            if os.path.isdir(p2) and os.path.isfile(os.path.join(p2, "package.json")):
                out[f"{d1}/{d2}"] = p2
    return out


def hash_tree(pkg, sub):
    root = os.path.join(pkg, sub)
    out = {}
    if not os.path.isdir(root):
        return out
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in SKIP]
        for fn in fns:
            if fn.endswith((".ts", ".tsx", ".js", ".mjs", ".json")):
                fp = os.path.join(dp, fn)
                with open(fp, "rb") as f:
                    out[os.path.relpath(fp, pkg)] = hashlib.sha1(f.read()).hexdigest()
    return out


old, new = pkg_list(OLD), pkg_list(NEW)
common = sorted(set(old) & set(new))
added = sorted(set(new) - set(old))
removed = sorted(set(old) - set(new))
src_changed, tests_only, ver_only = [], [], []
for k in common:
    if hash_tree(old[k], "src") != hash_tree(new[k], "src"):
        src_changed.append(k)
    elif hash_tree(old[k], "tests") != hash_tree(new[k], "tests"):
        tests_only.append(k)
    else:
        ver_only.append(k)

res = {"packages_old": len(old), "packages_new": len(new),
       "added": added, "removed": removed,
       "src_changed_count": len(src_changed), "tests_only_count": len(tests_only),
       "version_only_count": len(ver_only),
       "added_by_domain": dict(Counter(a.split("/")[0] for a in added))}
with open(os.path.join(SCRIPT_DIR, "v017", "delta-rc2-017.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)

print(f"packages/: {len(old)} -> {len(new)}  (+{len(added)} / -{len(removed)} / common {len(common)})")
print(f"src changed: {len(src_changed)}   tests only: {len(tests_only)}   version only: {len(ver_only)}")
print("\n[removed]"); [print("  ", r) for r in removed]
print("\n[added by domain]", res["added_by_domain"])
print("\n[added]"); [print("  ", a) for a in added]
