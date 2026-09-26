#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v0.1.7-rc.2 生成器输入准备：
  - v017/special-modules.json   （gen-html-l3.py 的 SPECIAL 输入，8 个特殊模块）
  - v017/disabled-rows.json     （inject-data-l3.py 的 disabled 输入）
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
OUT = os.path.join(SCRIPT_DIR, "v017")
SRC = os.path.join(BASE, "05-source", "dsh-v0.1.7-rc.2", "deepseek-harness-dsh-v0.1.7-rc.2")

inv = json.load(open(os.path.join(OUT, "inventory.json"), encoding="utf-8"))
facts = json.load(open(os.path.join(OUT, "facts.json"), encoding="utf-8"))
pkgs = inv["packages"]

BUNDLE_KIND = {
    "dsh-base": ("bundle", "所有 profile 的第一 patch 层，对空 profile 根做一次 insert"),
    "dsh-headless": ("bundle", "headless profile 的增量 patch 层（base 之上）"),
    "dsh-web-app": ("bundle", "web-app profile 的增量 patch 层（base 之上，含全部客户端 UI 包）"),
    "dsh-acp-app": ("bundle", "ACP profile 的增量 patch 层"),
    "dsh-sdk-app": ("bundle", "SDK profile 的增量 patch 层"),
    "dsh-sdk-minimal": ("bundle", "独立最小 SDK 应用：不叠 base，自身即完整 Cordis 树"),
    "dsh-app-boot": ("boot", "profile 引导与运行时镜像重建（app-boot）"),
    "dsh-cmdline": ("boot", "命令行入口与启动胶水（cmdline）"),
}


def to_id(nm):
    return nm.split("/")[1] if nm.startswith("@deepseek-ai/") else nm.split("/")[0]


special = []
for sid in sorted(inv["special"]):
    f = facts.get(sid, {})
    p = pkgs.get(sid, {})
    kind, desc = BUNDLE_KIND.get(sid, ("bundle", ""))
    deps = sorted({d for d in f.get("import_pkgs", [])})
    if sid.startswith("dsh-") and sid in ("dsh-base", "dsh-headless", "dsh-web-app", "dsh-acp-app", "dsh-sdk-app", "dsh-sdk-minimal"):
        short = sid[4:]  # base / headless / web-app / ...
        rows = inv["bundles"].get(short, {}).get("insert_rows", [])
        rows_txt = "、".join(f'{r["row_id"]}({to_id(r["name"]) if r.get("name") else "-"}{"，disabled" if r.get("disabled") else ""})'
                            for r in rows[:60])
        assembly = f'共 {len(rows)} 条 insert 行：{rows_txt}'
        deps = sorted({to_id(r["name"]) for r in rows if r.get("name")})
    else:
        assembly = desc
    files = p.get("ts_files", [])
    structure = (f'{len(files)} 个 TS 源文件：' + "、".join(files[:12]) + ("…" if len(files) > 12 else "")) if files else "无 TS 源码（bundle 元包）"
    special.append({
        "id": sid,
        "kind": kind,
        "assembly_summary": assembly,
        "structure_notes": structure,
        "dependencies": deps,
    })

with open(os.path.join(OUT, "special-modules.json"), "w", encoding="utf-8") as fh:
    json.dump({"special_modules": special}, fh, ensure_ascii=False, indent=1)
print(f"[OK] special-modules.json: {len(special)} modules -> {[s['id'] for s in special]}")

# ---- disabled rows ----
nodes = set(json.load(open(os.path.join(OUT, "classification.json"), encoding="utf-8"))["nodes"])
disabled = []
for b, bd in inv["bundles"].items():
    for r in bd["insert_rows"]:
        if not r.get("disabled"):
            continue
        nid = to_id(r["name"]) if r.get("name") else r["row_id"]
        disabled.append({"row_id": r["row_id"], "node": nid, "bundle": b,
                         "note": f'{b} bundle 中 disabled: {r["disabled"]}',
                         "in_nodes": nid in nodes})
with open(os.path.join(OUT, "disabled-rows.json"), "w", encoding="utf-8") as fh:
    json.dump({"disabled_base_rows": disabled}, fh, ensure_ascii=False, indent=1)
print(f"[OK] disabled-rows.json: {len(disabled)} rows, of which in DAG nodes: {sum(1 for d in disabled if d['in_nodes'])}")
for d in disabled[:12]:
    print(f"   {d['bundle']:12s} {d['row_id']:34s} -> {d['node']:38s} in_dag={d['in_nodes']}")
