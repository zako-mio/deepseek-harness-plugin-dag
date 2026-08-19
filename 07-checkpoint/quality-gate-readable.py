# -*- coding: utf-8 -*-
"""S5: 可读性质量门控（0817 经验迁移）
新增三检查：
A. 插件页区块模板：每插件页含「为什么需要它 + ①实现逻辑②provides③依赖④被依赖」五段
B. HTML 无 .md 链接（人类可读性）：全站 HTML href 不含 .md
C. index 统计一致性：index.html 统计数字与 webapp-dag.json 实测一致
"""
import json, os, sys, re, glob

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0819-plugin-dag-rc7"
DAG = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
EXT = os.path.join(BASE, "01-dag-data", "external-seams.json")
INDEX = os.path.join(BASE, "index.html")
PAGES = os.path.join(BASE, "02-plugin-pages")
sys.stdout.reconfigure(encoding="utf-8")

ok = True
fails = []
def check(cond, msg):
    global ok
    if cond:
        print(f"  [OK] {msg}")
    else:
        ok = False
        fails.append(msg)
        print(f"  [FAIL] {msg}")

with open(DAG, encoding="utf-8") as f:
    dag = json.load(f)
with open(EXT, encoding="utf-8") as f:
    ext = json.load(f)

nodes = dag["nodes"]
edges = dag["edges"]
seams = ext["seams"]
page_ids = {n["id"] for n in nodes} | {s["id"] for s in seams}

print("=== A. 插件页区块模板（五段） ===")
REQ_BLOCKS = ["为什么需要它", "① 实现逻辑", "② 注册/提供", "③ 依赖", "④ 被依赖"]
block_missing = []
# 只检查 DAG 插件页（173），不检查 seam 页（seam 是基座说明页，无四段结构）
dag_page_ids = {n["id"] for n in nodes}
for nid in dag_page_ids:
    p = os.path.join(PAGES, nid + ".html")
    if not os.path.exists(p):
        block_missing.append((nid, "NO_PAGE"))
        continue
    c = open(p, encoding="utf-8").read()
    for b in REQ_BLOCKS:
        if b not in c:
            block_missing.append((nid, b))
check(not block_missing, f"DAG 插件页五段区块缺失 {len(block_missing)} -> {block_missing[:5]}")

print("=== B. HTML 站内链接无 .md（人类可读性） ===")
md_links = []
all_html = [INDEX] + glob.glob(os.path.join(PAGES, "*.html")) + glob.glob(os.path.join(BASE, "03-groups", "*.html")) + glob.glob(os.path.join(BASE, "04-interactive", "*.html")) + glob.glob(os.path.join(BASE, "08-special-modules", "*.html"))
for p in all_html:
    c = open(p, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r'href="([^"]+\.md)"', c):
        href = m.group(1)
        # 只检查站内相对链接（不含 http/https），外部来源引用（GitHub README.md）是内容合理引用
        if not href.startswith(("http://", "https://")):
            md_links.append((os.path.relpath(p, BASE), href))
check(not md_links, f"HTML 站内指向 .md {len(md_links)} -> {md_links[:5]}")

print("=== C. index 统计一致性 ===")
idx = open(INDEX, encoding="utf-8").read()
real = {
    "节点": len(nodes),
    "seam": len(seams),
    "边": len(edges),
    "组": len(dag.get("groups", [])),
    "页": len(glob.glob(os.path.join(PAGES, "*.html")))
}
print(f"  实测: 节点{real['节点']} / seam{real['seam']} / 边{real['边']} / 组{real['组']} / 页{real['页']}")
# 从 index.html 提取统计数字（统计块内的 <b> 值）
stats_b = re.findall(r'<div class="stat"><b>(\d+)</b><span>([^<]+)</span>', idx)
print(f"  index.html 统计块: {stats_b}")
idx_stats = {}
for num, label in stats_b:
    idx_stats[label] = int(num)
# 匹配
consistency_ok = True
for label, val in [("插件节点", real["节点"]), ("外部 seam", real["seam"]), ("依赖边", real["边"]), ("分组", real["组"]), ("HTML 插件页", real["页"])]:
    if label in idx_stats and idx_stats[label] != val:
        consistency_ok = False
        print(f"  [FAIL] {label}: index={idx_stats[label]} 实测={val}")
if consistency_ok:
    check(True, f"index 统计与数据源一致 ({len(stats_b)} 项)")
else:
    check(False, "index 统计存在不一致")

print()
print(f"===== {'ALL PASS' if ok else f'HAS FAILURES ({len(fails)})'} =====")
for f in fails:
    print("  -", f)
sys.exit(0 if ok else 1)
