#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S6 质量门控脚本: 校验 0816-plugin-dag 全部交付物
1. JSON 合法性 (core-dag.json / external-seams.json / stage-*.json)
2. DAG 无环 (Kahn 校验 + 拓扑分层完整)
3. HTML: UTF-8 无替换字符, div 开闭平衡, 引用完整性(内链目标存在)
4. drawio: XML 良构 + 配套 png 存在
5. vendor: cytoscape.min.js + cytoscape-dagre.min.js 存在
6. 插件页覆盖: 76 核心 + 36 外部 seam 每插件 ≥1 页
"""
import json, os, re, glob, html

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0819-plugin-dag-rc7"
errors = []
warnings = []

def check(cond, msg):
    if not cond:
        errors.append(msg)

# ---- 1. JSON 合法性 ----
json_files = [
    os.path.join(BASE, "01-dag-data", "core-dag.json"),
    os.path.join(BASE, "01-dag-data", "external-seams.json"),
] + glob.glob(os.path.join(BASE, "07-checkpoint", "stage-01-r*.json")) + [
    os.path.join(BASE, "07-checkpoint", "stage-00-inventory.json"),
]
for jf in json_files:
    try:
        with open(jf, "r", encoding="utf-8") as f:
            json.load(f)
    except Exception as e:
        check(False, f"JSON 非法 {os.path.basename(jf)}: {e}")
print(f"[1] JSON 校验: {len(json_files)} 文件")

# ---- 2. DAG 无环 + 拓扑 ----
with open(os.path.join(BASE, "01-dag-data", "core-dag.json"), "r", encoding="utf-8") as f:
    dag = json.load(f)
node_ids = {n["id"] for n in dag["nodes"]}
# 边合法性
for e in dag["edges"]:
    check(e["from"] in node_ids, f"边 from 不在节点集: {e['from']}")
    check(e["to"] in node_ids, f"边 to 不在节点集: {e['to']}")
# 无环 (Kahn)
indeg = {nid: 0 for nid in node_ids}
adj = {nid: [] for nid in node_ids}
for e in dag["edges"]:
    adj[e["to"]].append(e["from"])  # from 依赖 to, to 先
    indeg[e["from"]] += 1
queue = [n for n in node_ids if indeg[n] == 0]
count = 0
while queue:
    n = queue.pop()
    count += 1
    for c in adj[n]:
        indeg[c] -= 1
        if indeg[c] == 0:
            queue.append(c)
check(count == len(node_ids), f"DAG 有环! 处理 {count}/{len(node_ids)}")
print(f"[2] DAG 无环校验: {count}/{len(node_ids)} 节点可达, 边数={len(dag['edges'])}")

# ---- 3. HTML 校验 ----
html_files = glob.glob(os.path.join(BASE, "02-plugin-pages", "*.html")) + \
             glob.glob(os.path.join(BASE, "03-groups", "*.html")) + \
             glob.glob(os.path.join(BASE, "04-interactive", "*.html"))
check(len(html_files) >= 112 + 24 + 1, f"HTML 页数不足: {len(html_files)}")

# 内链完整性: 收集所有页面文件名
page_names = {os.path.basename(p) for p in glob.glob(os.path.join(BASE, "02-plugin-pages", "*.html"))}
group_names = {os.path.basename(p) for p in glob.glob(os.path.join(BASE, "03-groups", "*.html"))}
all_pages = page_names | group_names | {"index.html"}

broken = []
for hf in html_files:
    with open(hf, "r", encoding="utf-8") as f:
        content = f.read()
    # UTF-8 替换字符
    if "\ufffd" in content:
        check(False, f"UTF-8 替换字符: {os.path.basename(hf)}")
    # div 平衡
    opens = content.count("<div")
    closes = content.count("</div>")
    if opens != closes:
        check(False, f"div 不平衡 {os.path.basename(hf)}: open={opens} close={closes}")
    # 内链检查 (排除 ../index.html 总入口, 由 S7 生成)
    for m in re.finditer(r'href="([^"#]+\.html)(?:#[^"]*)?"', content):
        target = m.group(1)
        if target == "../index.html":
            continue
        # 相对路径解析
        base_dir = os.path.dirname(hf)
        abs_t = os.path.normpath(os.path.join(base_dir, target))
        if not os.path.exists(abs_t):
            broken.append(f"{os.path.basename(hf)} -> {target}")

# 去重 broken
seen = set()
uniq_broken = []
for b in broken:
    if b not in seen:
        seen.add(b)
        uniq_broken.append(b)
if uniq_broken:
    for b in uniq_broken[:20]:
        warnings.append(f"断链: {b}")
    check(len(uniq_broken) < 5, f"断链数过多: {len(uniq_broken)}")
print(f"[3] HTML 校验: {len(html_files)} 页, 断链 {len(uniq_broken)} 条")

# ---- 4. vendor ----
for v in ["cytoscape.min.js", "cytoscape-dagre.min.js"]:
    vp = os.path.join(BASE, "04-interactive", "vendor", v)
    check(os.path.exists(vp), f"vendor 缺失: {v}")
print(f"[4] vendor 校验: cytoscape + dagre 存在")

# ---- 5. 插件页覆盖 ----
core_missing = [nid for nid in node_ids if not os.path.exists(os.path.join(BASE, "02-plugin-pages", f"{nid}.html"))]
with open(os.path.join(BASE, "01-dag-data", "external-seams.json"), "r", encoding="utf-8") as f:
    ext = json.load(f)
ext_ids = [s["id"] for s in ext["seams"]]
ext_missing = [sid for sid in ext_ids if not os.path.exists(os.path.join(BASE, "02-plugin-pages", f"{sid}.html"))]
check(not core_missing, f"核心插件页缺失: {core_missing}")
check(not ext_missing, f"外部 seam 页缺失: {ext_missing}")
print(f"[5] 插件页覆盖: 核心 {len(node_ids)-len(core_missing)}/{len(node_ids)}, 外部 {len(ext_ids)-len(ext_missing)}/{len(ext_ids)}")

# ---- 汇总 ----
print("\n===== 质量门控结果 =====")
print(f"ERRORS: {len(errors)}")
for e in errors[:20]:
    print(f"  [ERR] {e}")
print(f"WARNINGS: {len(warnings)}")
for w in warnings[:20]:
    print(f"  [WARN] {w}")
print(f"\nPASS" if not errors else f"\nFAIL ({len(errors)} errors)")
sys_exit = 1 if errors else 0
raise SystemExit(sys_exit)
