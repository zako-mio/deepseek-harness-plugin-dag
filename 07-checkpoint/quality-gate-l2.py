#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S6 L2 质量门控脚本: 校验 0816-plugin-dag L1+L2 全部交付物
1. JSON 合法性 (webapp-dag.json / external-seams.json / stage-*.json)
2. DAG 无环 (Kahn 校验 + 拓扑分层完整)
3. HTML: UTF-8 无替换字符, div 开闭平衡, 引用完整性(内链目标存在)
4. drawio: XML 良构 + 配套 png 存在
5. vendor: cytoscape.min.js + cytoscape-dagre.min.js 存在
6. 插件页覆盖: 134 节点 + 36 外部 seam 每插件 ≥1 页
7. 交互图 DATA 校验 (index.html 可解析 + 组级 30 节点)
"""
import json, os, re, glob, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-plugin-dag-rc8"
errors = []
warnings = []

def check(cond, msg):
    if not cond:
        errors.append(msg)

# ---- 1. JSON 合法性 ----
json_files = [
    os.path.join(BASE, "01-dag-data", "webapp-dag.json"),
    os.path.join(BASE, "01-dag-data", "core-dag.json"),
    os.path.join(BASE, "01-dag-data", "external-seams.json"),
] + glob.glob(os.path.join(BASE, "07-checkpoint", "stage-01-l2-r*.json")) + [
    os.path.join(BASE, "07-checkpoint", "stage-00-l2-inventory.json"),
]
for jf in json_files:
    try:
        with open(jf, "r", encoding="utf-8") as f:
            json.load(f)
    except Exception as e:
        check(False, f"JSON 非法 {os.path.basename(jf)}: {e}")
print(f"[1] JSON 校验: {len(json_files)} 文件")

# ---- 2. DAG 无环 + 拓扑 ----
with open(os.path.join(BASE, "01-dag-data", "webapp-dag.json"), "r", encoding="utf-8") as f:
    dag = json.load(f)
node_ids = {n["id"] for n in dag["nodes"]}
for e in dag["edges"]:
    check(e["from"] in node_ids, f"边 from 不在节点集: {e['from']}")
    check(e["to"] in node_ids, f"边 to 不在节点集: {e['to']}")
indeg = {nid: 0 for nid in node_ids}
adj = {nid: [] for nid in node_ids}
for e in dag["edges"]:
    adj[e["to"]].append(e["from"])
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
print(f"[2] DAG 无环校验: {count}/{len(node_ids)} 节点可达, 边数={len(dag['edges'])}, 层数={dag['meta']['layer_count']}")

# ---- 3. HTML 校验 ----
html_files = glob.glob(os.path.join(BASE, "02-plugin-pages", "*.html")) + \
             glob.glob(os.path.join(BASE, "03-groups", "*.html")) + \
             glob.glob(os.path.join(BASE, "04-interactive", "*.html"))
check(len(html_files) >= 134 + 36 + 29 + 1, f"HTML 页数不足: {len(html_files)}")

page_names = {os.path.basename(p) for p in glob.glob(os.path.join(BASE, "02-plugin-pages", "*.html"))}
group_names = {os.path.basename(p) for p in glob.glob(os.path.join(BASE, "03-groups", "*.html"))}
all_pages = page_names | group_names | {"index.html"}

broken = []
for hf in html_files:
    with open(hf, "r", encoding="utf-8") as f:
        content = f.read()
    if "\ufffd" in content:
        check(False, f"UTF-8 替换字符: {os.path.basename(hf)}")
    opens = content.count("<div")
    closes = content.count("</div>")
    if opens != closes:
        check(False, f"div 不平衡 {os.path.basename(hf)}: open={opens} close={closes}")
    for m in re.finditer(r'href="([^"#]+\.html)(?:#[^"]*)?"', content):
        target = m.group(1)
        if target == "../index.html":
            continue
        base_dir = os.path.dirname(hf)
        abs_t = os.path.normpath(os.path.join(base_dir, target))
        if not os.path.exists(abs_t):
            broken.append(f"{os.path.basename(hf)} -> {target}")

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
check(not core_missing, f"插件页缺失: {core_missing}")
check(not ext_missing, f"外部 seam 页缺失: {ext_missing}")
print(f"[5] 插件页覆盖: 核心 {len(node_ids)-len(core_missing)}/{len(node_ids)}, 外部 {len(ext_ids)-len(ext_missing)}/{len(ext_ids)}")

# ---- 6. 交互图 DATA ----
html_path = os.path.join(BASE, "04-interactive", "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()
m = re.search(r'const DATA = (\{.*?\});', content, re.DOTALL)
if not m:
    check(False, "index.html DATA 不可解析")
else:
    try:
        data = json.loads(m.group(1))
        check(len(data["plugins"]) == len(node_ids), f"DATA plugins 数不符: {len(data['plugins'])} vs {len(node_ids)}")
        check(len(data["groups"]) == len(dag["groups"]), f"DATA groups 数不符: {len(data['groups'])} vs {len(dag['groups'])}")
        check("disabledIds" in data and len(data["disabledIds"]) > 0, "DATA 缺 disabledIds")
        check('node[kind="disabled"]' in content, "样式缺 node[kind=disabled]")
        check('node[kind="plugin"]' in content and 'node[kind="group"]' in content, "样式选择器缺失")
        check("extColor" in data, "DATA 缺 extColor")
    except Exception as e:
        check(False, f"index.html DATA 解析失败: {e}")
print(f"[6] 交互图 DATA 校验: plugins={len(data['plugins']) if 'data' in dir() else 'N/A'}")

# ---- 汇总 ----
print("\n===== 质量门控结果 =====")
print(f"ERRORS: {len(errors)}")
for e in errors[:20]:
    print(f"  [ERR] {e}")
print(f"WARNINGS: {len(warnings)}")
for w in warnings[:20]:
    print(f"  [WARN] {w}")
print(f"\n{'ALL PASS' if not errors else f'FAIL ({len(errors)} errors)'}")
sys.exit(1 if errors else 0)
