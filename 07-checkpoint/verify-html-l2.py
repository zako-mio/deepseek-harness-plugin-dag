#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S4 验证: 插件页双向链 + disabled 标注 + div 平衡"""
import json, os, re, glob, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-plugin-dag-rc8"
PAGES = os.path.join(BASE, "02-plugin-pages")

with open(os.path.join(BASE, "01-dag-data", "webapp-dag.json"), "r", encoding="utf-8") as f:
    dag = json.load(f)
nodes = {n["id"]: n for n in dag["nodes"]}

# 1. 页数
pages = glob.glob(os.path.join(PAGES, "*.html"))
print(f"[INFO] plugin pages: {len(pages)}")

# 2. 抽检 L2 核心页
for pid in ["dsh-web-app", "dsh-client-runtime", "dsh-client-ui-conversation", "dsh-host-apiproxy", "dsh-client-web", "dsh-client-ui-tool"]:
    fp = os.path.join(PAGES, f"{pid}.html")
    if not os.path.exists(fp):
        print(f"  [MISSING] {pid}")
        continue
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()
    opens = c.count("<div")
    closes = c.count("</div>")
    l2_badge = 'L2 web-app' in c
    dep_count = c.count('class="dep-item"')
    print(f"  {pid}: div={opens}/{closes} {'OK' if opens==closes else 'FAIL'} L2badge={l2_badge} deps={dep_count}")

# 3. L1 页是否含 L2 下游 (dsh-session 应有 L2 下游)
with open(os.path.join(PAGES, "dsh-session.html"), "r", encoding="utf-8") as f:
    c = f.read()
has_l2_down = 'chip l2' in c or 'dsh-client-runtime' in c or 'dsh-host-apiproxy' in c
print(f"\n[INFO] dsh-session page L2 downstream present: {has_l2_down}")

# 4. disabled 标注 (dsh-tool-bash 在 web 下 disabled)
with open(os.path.join(PAGES, "dsh-tool-bash.html"), "r", encoding="utf-8") as f:
    c = f.read()
print(f"[INFO] dsh-tool-bash page exists, mentions disabled: {'disabled' in c.lower()}")

# 5. 全局 div 平衡统计
bad = 0
for fp in pages:
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()
    if c.count("<div") != c.count("</div>"):
        bad += 1
        print(f"  [DIV-FAIL] {os.path.basename(fp)}")
print(f"[INFO] div imbalance: {bad}/{len(pages)}")

# 6. UTF-8 替换字符
repl = 0
for fp in pages:
    with open(fp, "r", encoding="utf-8") as f:
        c = f.read()
    if "\ufffd" in c:
        repl += 1
        print(f"  [REPL] {os.path.basename(fp)}")
print(f"[INFO] replacement chars: {repl}/{len(pages)}")

# 7. 组页
gpages = glob.glob(os.path.join(BASE, "03-groups", "*.html"))
print(f"[INFO] group pages: {len(gpages)}")
