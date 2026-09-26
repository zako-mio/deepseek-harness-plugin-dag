#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v0.1.7-rc.2 页面目录清理：删除不在新节点/ seam 集合内的陈旧生成物"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
DATA = os.path.join(BASE, "01-dag-data")

dag = json.load(open(os.path.join(DATA, "webapp-dag.json"), encoding="utf-8"))
ext = json.load(open(os.path.join(DATA, "external-seams.json"), encoding="utf-8"))
nodes = {n["id"] for n in dag["nodes"]}
seams = {s["id"] for s in ext["seams"]}
groups = {g["id"] for g in dag["groups"]}
special = {s["id"] for s in json.load(open(os.path.join(SCRIPT_DIR, "v017", "special-modules.json"), encoding="utf-8"))["special_modules"]}

# 保留白名单（非生成物的手工文件）
KEEP = {"index.html"}

targets = [
    (os.path.join(BASE, "02-plugin-pages"), nodes | seams, ".html"),
    (os.path.join(BASE, "03-groups"), groups, ".html"),
    (os.path.join(BASE, "06-md", "plugins"), nodes | seams, ".md"),
    (os.path.join(BASE, "08-special-modules"), special, ".html"),
]

total = 0
for d, keep_ids, ext_ in targets:
    if not os.path.isdir(d):
        print(f"[WARN] missing dir {d}")
        continue
    named = {f"{i}{ext_}" for i in keep_ids}
    removed = []
    for fn in sorted(os.listdir(d)):
        if fn in KEEP or fn.startswith("00-"):
            continue
        if not fn.endswith(ext_):
            continue
        if fn not in named:
            fp = os.path.join(d, fn)
            if os.path.isfile(fp) or os.path.islink(fp):
                os.remove(fp)
                removed.append(fn)
    total += len(removed)
    print(f"[OK] {os.path.relpath(d, BASE)}: removed {len(removed)} stale files (kept {len(keep_ids)} expected)")
    for r in removed[:8]:
        print("     -", r)
    if len(removed) > 8:
        print(f"     ... (+{len(removed)-8})")
print(f"\n[OK] total removed: {total}")
