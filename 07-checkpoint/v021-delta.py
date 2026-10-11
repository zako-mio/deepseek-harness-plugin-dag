#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v0.1.7-rc.2 → v0.2.1-alpha.2 包级结构差异（供差异报告与增量复用判定引用）。

关键设计：**以包 id（= 去 @deepseek-ai/ 前缀的包名）为键**，而非目录路径。
原因：本轮存在大量「同 id 换目录」的搬迁（如 packages/webhook/webhook →
packages/experimental/webhook，id 仍为 dsh-webhook）。以路径为键会把搬迁
误判成「删除 + 新增」，从而白白重做分析。

分类（按 id 对齐后）：
  added / removed / src_changed / tests_changed / version_only / identical
另记录 path_moved（同 id 但目录变了），供报告说明。
"""
import os, sys, json, hashlib
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
OUT = os.path.join(SCRIPT_DIR, "v021")
OLD = os.path.join(BASE, "05-source", "dsh-v0.1.7-rc.2", "deepseek-harness-dsh-v0.1.7-rc.2")
NEW = os.path.join(BASE, "05-source", "dsh-v0.2.1-alpha.2", "deepseek-harness-dsh-v0.2.1-alpha.2")
SKIP = {"node_modules", "dist", "lib", "build", ".turbo", "coverage", "__pycache__"}


def to_id(name):
    """'@deepseek-ai/dsh-x/tools' -> 'dsh-x'"""
    if not name:
        return name
    n = name.strip()
    if n.startswith("@"):
        n = "/".join(n.split("/")[:2])
    else:
        n = n.split("/")[0]
    return n[len("@deepseek-ai/"):] if n.startswith("@deepseek-ai/") else n


def pkg_list(root):
    """{id: {'path':..., 'dir':...}} for packages/<dom>/<pkg> and vendor/<pkg>"""
    out = {}
    pk = os.path.join(root, "packages")
    if os.path.isdir(pk):
        for d1 in sorted(os.listdir(pk)):
            p1 = os.path.join(pk, d1)
            if not os.path.isdir(p1):
                continue
            for d2 in sorted(os.listdir(p1)):
                p2 = os.path.join(p1, d2)
                pj = os.path.join(p2, "package.json")
                if not (os.path.isdir(p2) and os.path.isfile(pj)):
                    continue
                try:
                    nm = json.load(open(pj, encoding="utf-8")).get("name")
                except Exception:
                    continue
                if nm:
                    out[to_id(nm)] = {"path": f"packages/{d1}/{d2}", "dir": p2, "name": nm}
    vr = os.path.join(root, "vendor")
    if os.path.isdir(vr):
        for d in sorted(os.listdir(vr)):
            p = os.path.join(vr, d)
            pj = os.path.join(p, "package.json")
            if not (os.path.isdir(p) and os.path.isfile(pj)):
                continue
            try:
                nm = json.load(open(pj, encoding="utf-8")).get("name")
            except Exception:
                continue
            if nm:
                out[to_id(nm)] = {"path": f"vendor/{d}", "dir": p, "name": nm}
    return out


def hash_tree(pkg_dir, sub=None, exclude=()):
    """sha256 over sorted (relpath, bytes). sub=None → whole pkg minus SKIP/exclude."""
    base = os.path.join(pkg_dir, sub) if sub else pkg_dir
    if not os.path.isdir(base):
        return None
    h = hashlib.sha256()
    files = []
    for dp, dns, fns in os.walk(base):
        dns[:] = [d for d in dns if d not in SKIP and d not in exclude]
        for fn in sorted(fns):
            fp = os.path.join(dp, fn)
            files.append(os.path.relpath(fp, base))
    for rel in sorted(files):
        h.update(rel.encode())
        with open(os.path.join(base, rel), "rb") as f:
            h.update(f.read())
    return h.hexdigest()


def pkg_version(d):
    pj = os.path.join(d, "package.json")
    try:
        return json.load(open(pj, encoding="utf-8")).get("version")
    except Exception:
        return None


old, new = pkg_list(OLD), pkg_list(NEW)
old_ids, new_ids = set(old), set(new)
added = sorted(new_ids - old_ids)
removed = sorted(old_ids - new_ids)
common = sorted(old_ids & new_ids)

cat, detail, moved = {}, {}, {}
for pid in common:
    o, n = old[pid]["dir"], new[pid]["dir"]
    same_src = hash_tree(o, "src") == hash_tree(n, "src")
    same_tst = hash_tree(o, "tests") == hash_tree(n, "tests")
    same_rest = hash_tree(o, None, exclude=("src", "tests")) == hash_tree(n, None, exclude=("src", "tests"))
    if not same_src:
        k = "src_changed"
    elif not same_tst:
        k = "tests_changed"
    elif not same_rest:
        k = "version_only"
    else:
        k = "identical"
    cat[pid] = k
    if old[pid]["path"] != new[pid]["path"]:
        moved[pid] = {"from": old[pid]["path"], "to": new[pid]["path"]}
    detail[pid] = {"path_old": old[pid]["path"], "path_new": new[pid]["path"],
                   "version_old": pkg_version(o), "version_new": pkg_version(n)}

res = {
    "meta": {
        "from_version": "0.1.7-rc.2",
        "to_version": "0.2.1-alpha.2",
        "keyed_by": "package id (name minus @deepseek-ai/)",
        "old_root": OLD, "new_root": NEW,
    },
    "counts": {
        "old_total": len(old), "new_total": len(new),
        "added": len(added), "removed": len(removed), "common": len(common),
        "src_changed": sum(1 for v in cat.values() if v == "src_changed"),
        "tests_changed": sum(1 for v in cat.values() if v == "tests_changed"),
        "version_only": sum(1 for v in cat.values() if v == "version_only"),
        "identical": sum(1 for v in cat.values() if v == "identical"),
        "path_moved": len(moved),
    },
    "added": added, "removed": removed,
    "category": cat, "detail": detail, "path_moved": moved,
    "added_by_domain": dict(Counter(new[a]["path"].split("/")[1] for a in added)),
    "removed_by_domain": dict(Counter(old[r]["path"].split("/")[1] for r in removed)),
}
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "delta-017-021.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)

c = res["counts"]
print(f"packages (by id): {c['old_total']} -> {c['new_total']}   (+{c['added']} / -{c['removed']} / common {c['common']})")
print(f"  src_changed   : {c['src_changed']}")
print(f"  tests_changed : {c['tests_changed']}")
print(f"  version_only  : {c['version_only']}")
print(f"  identical     : {c['identical']}")
print(f"  path_moved    : {c['path_moved']}")
print(f"\nadded by domain  : {res['added_by_domain']}")
print(f"removed by domain: {res['removed_by_domain']}")
print(f"\n[added] {len(added)}"); [print("   ", a) for a in added]
print(f"\n[removed] {len(removed)}"); [print("   ", r) for r in removed]
print(f"\n[path_moved] {len(moved)}")
for k, v in sorted(moved.items()):
    print(f"    {k}: {v['from']} -> {v['to']}")
print(f"\n[OK] wrote {os.path.join(OUT, 'delta-017-021.json')}")
