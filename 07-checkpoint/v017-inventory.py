#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v0.1.7-rc.2 库存采集（确定性，可复现）
输出 07-checkpoint/v017/inventory.json:
  - bundles: 各 bundle cordis.patch.yml 的插入行/补丁行
  - packages: packages/*/* + vendor/* 全量包（id/name/path/domain/ts 文件）
  - nodes:   被装配的插件（排除特殊模块：bundle/boot）
  - seams:   未被装配但被节点依赖的包（抽象基座/测试支撑等）
  - uncovered: 既未装配也未被引用的包
"""
import json, os, re, sys
from collections import defaultdict
import yaml

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
SRC_NAME = "deepseek-harness-dsh-v0.1.7-rc.2"
SRC = os.path.join(BASE, "05-source", "dsh-v0.1.7-rc.2", SRC_NAME)
OUT_DIR = os.path.join(SCRIPT_DIR, "v017")
os.makedirs(OUT_DIR, exist_ok=True)

BUNDLES = ["base", "headless", "web-app", "acp-app", "sdk-app", "sdk-minimal"]
# 特殊模块：装配框架/启动胶水，不进主 DAG
SPECIAL_NAMES = {
    "@deepseek-ai/dsh-base", "@deepseek-ai/dsh-headless",
    "@deepseek-ai/dsh-app-boot", "@deepseek-ai/dsh-cmdline",
    "@deepseek-ai/dsh-web-app", "@deepseek-ai/dsh-acp-app",
    "@deepseek-ai/dsh-sdk-app", "@deepseek-ai/dsh-sdk-minimal",
}


class DshLoader(yaml.SafeLoader):
    """cordis patch 含 !!js 自定义标签（JS 表达式），保留原文即可"""


def _unknown(loader, tag_suffix, node):
    if isinstance(node, yaml.ScalarNode):
        return f"<{tag_suffix}>{loader.construct_scalar(node)}"
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    return loader.construct_mapping(node)


DshLoader.add_multi_constructor("tag:yaml.org,2002:js", _unknown)
DshLoader.add_multi_constructor("!", _unknown)
yaml.add_multi_constructor("tag:yaml.org,2002:js", _unknown, Loader=yaml.SafeLoader)


def base_name(n):
    """'@deepseek-ai/dsh-x/tools' -> '@deepseek-ai/dsh-x'"""
    if not n:
        return n
    n = n.strip()
    if n.startswith("@"):
        parts = n.split("/")
        return "/".join(parts[:2])
    return n.split("/")[0]


def to_id(name):
    n = base_name(name)
    return n[len("@deepseek-ai/"):] if n.startswith("@deepseek-ai/") else n


# ---- 1. 解析 bundle patch ----
bundles = {}
for b in BUNDLES:
    fp = os.path.join(SRC, "packages", "bundle", b, "cordis.patch.yml")
    if not os.path.isfile(fp):
        print(f"[WARN] bundle patch missing: {fp}")
        continue
    with open(fp, "r", encoding="utf-8") as f:
        doc = yaml.load(f, Loader=DshLoader)
    rows, patches = [], []
    for item in (doc or []):
        if not isinstance(item, dict):
            continue
        if "insert" in item:
            for r in item["insert"] or []:
                rows.append({
                    "row_id": r.get("id"),
                    "name": r.get("name"),
                    "disabled": r.get("disabled"),
                    "src": f"packages/bundle/{b}/cordis.patch.yml",
                })
        else:
            for k, v in item.items():
                if k == "id":
                    continue
                patches.append({"row_id": k, "value": v.get("disabled") if isinstance(v, dict) else v,
                                "src": f"packages/bundle/{b}/cordis.patch.yml"})
            if "id" in item:
                patches.append({"row_id": item["id"], "value": item.get("disabled"),
                                "src": f"packages/bundle/{b}/cordis.patch.yml"})
    bundles[b] = {"insert_rows": rows, "patches": patches}
    print(f"[INFO] bundle {b}: insert_rows={len(rows)} patches={len(patches)}")

# ---- 2. 枚举包 ----
packages = {}


def add_pkg(root_rel, pdir, domain):
    pj = os.path.join(pdir, "package.json")
    try:
        with open(pj, "r", encoding="utf-8") as f:
            meta = json.load(f)
    except Exception:
        return
    name = meta.get("name")
    if not name:
        return
    pid = to_id(name)
    src_dir = os.path.join(pdir, "src")
    ts_files = []
    if os.path.isdir(src_dir):
        for dp, dns, fns in os.walk(src_dir):
            dns[:] = [d for d in dns if d not in {"node_modules", "__tests__", "__snapshots__"}]
            for fn in fns:
                if fn.endswith((".ts", ".tsx", ".mts")):
                    ts_files.append(os.path.relpath(os.path.join(dp, fn), pdir))
    packages[pid] = {
        "id": pid,
        "name": name,
        "path": root_rel,
        "domain": domain,
        "ts_count": len(ts_files),
        "ts_files": sorted(ts_files),
        "has_src": os.path.isdir(src_dir),
        "version": meta.get("version"),
        "deps": {
            "peer": list((meta.get("peerDependencies") or {}).keys()),
            "deps": list((meta.get("dependencies") or {}).keys()),
            "dev": list((meta.get("devDependencies") or {}).keys()),
        },
    }


pk_root = os.path.join(SRC, "packages")
for d1 in sorted(os.listdir(pk_root)):
    p1 = os.path.join(pk_root, d1)
    if not os.path.isdir(p1):
        continue
    for d2 in sorted(os.listdir(p1)):
        p2 = os.path.join(p1, d2)
        if os.path.isdir(p2) and os.path.isfile(os.path.join(p2, "package.json")):
            add_pkg(f"packages/{d1}/{d2}", p2, d1)

v_root = os.path.join(SRC, "vendor")
if os.path.isdir(v_root):
    for d in sorted(os.listdir(v_root)):
        p = os.path.join(v_root, d)
        if os.path.isdir(p) and os.path.isfile(os.path.join(p, "package.json")):
            add_pkg(f"vendor/{d}", p, "vendor")

print(f"[INFO] packages enumerated: {len(packages)}")

# ---- 3. 装配判定 ----
assembled = {}   # id -> [bundle...]
for b, bd in bundles.items():
    for r in bd["insert_rows"]:
        nm = base_name(r.get("name"))
        if not nm:
            continue
        pid = to_id(nm)
        assembled.setdefault(pid, []).append(b)

special = {pid for pid in assembled if packages.get(pid, {}).get("name") in SPECIAL_NAMES}
# 特殊模块若不在 packages 里也按名字过滤
for pid, p in packages.items():
    if p["name"] in SPECIAL_NAMES:
        special.add(pid)

nodes = {}
for pid in assembled:
    if pid in special:
        continue
    p = packages.get(pid)
    if not p:
        continue
    if p["ts_count"] == 0:
        continue
    nodes[pid] = p

print(f"[INFO] assembled ids: {len(assembled)}; special: {len(special)}; nodes(with src): {len(nodes)}")

# ---- 4. 依赖引用（E1 声明）→ 区分 seam / uncovered ----
def dep_ids(p):
    out = set()
    for k in ("peer", "deps"):
        for d in p["deps"][k]:
            dn = base_name(d)
            if dn.startswith("@deepseek-ai/"):
                out.add(to_id(dn))
    return out


referenced = set()
for pid, p in nodes.items():
    referenced |= dep_ids(p)

seams, uncovered = {}, {}
for pid, p in packages.items():
    if pid in nodes or pid in special:
        continue
    if pid in referenced:
        seams[pid] = p
    else:
        uncovered[pid] = p

print(f"[INFO] seams: {len(seams)}; uncovered: {len(uncovered)}")

result = {
    "meta": {
        "version": "0.1.7-rc.2",
        "source_dir": SRC,
        "bundles": BUNDLES,
    },
    "bundles": bundles,
    "packages": packages,
    "assembled": {k: v for k, v in assembled.items()},
    "special": sorted(special),
    "nodes": sorted(nodes.keys()),
    "seams": sorted(seams.keys()),
    "uncovered": sorted(uncovered.keys()),
}
with open(os.path.join(OUT_DIR, "inventory.json"), "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("\n[special]", sorted(special))
print("\n[uncovered]", sorted(uncovered.keys()))
print(f"\n[OK] wrote {os.path.join(OUT_DIR, 'inventory.json')}")
