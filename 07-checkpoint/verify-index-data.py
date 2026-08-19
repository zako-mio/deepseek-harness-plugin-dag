#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证注入后的 index.html: DATA 可解析 + 样式选择器存在 + div 平衡"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-plugin-dag-rc8"
HTML = os.path.join(BASE, "04-interactive", "index.html")

with open(HTML, "r", encoding="utf-8") as f:
    content = f.read()

# 1. 提取 DATA
m = re.search(r'const DATA = (\{.*?\});', content, re.DOTALL)
if not m:
    print("[ERR] DATA not found")
    raise SystemExit(1)
data = json.loads(m.group(1))
print(f"[OK] DATA parsed: plugins={len(data['plugins'])} seams={len(data['seams'])} edges={len(data['edges'])} groupEdges={len(data['groupEdges'])}")
print(f"[OK] groups keys: {len(data['groups'])}, groupColor keys: {len(data['groupColor'])}")
print(f"[OK] disabledIds: {len(data.get('disabledIds', []))}")
print(f"[OK] extColor: {data['extColor']}")

# 2. 检查样式选择器
for sel in ['node[kind="plugin"]', 'node[kind="seam"]', 'node[kind="stub"]', 'node[kind="disabled"]', 'node[kind="group"]', 'edge[kind="seam"]', 'edge[kind="group"]']:
    print(f"  selector {sel}: {'FOUND' if sel in content else 'MISSING'}")

# 3. div 平衡
opens = content.count("<div")
closes = content.count("</div>")
print(f"div balance: {opens} vs {closes} {'OK' if opens == closes else 'FAIL'}")

# 4. 替换字符
if "\ufffd" in content:
    print("[ERR] UTF-8 replacement char found")
else:
    print("[OK] no replacement chars")

# 5. 检查 DATA 里 plugins 的 kind 分布
from collections import Counter
kinds = Counter(p["data"]["kind"] for p in data["plugins"])
print(f"plugin kinds: {dict(kinds)}")

# 6. 组级视图节点数 (groups 24 L1 + 5 L2 + EXT)
print(f"组级视图节点 = {len(data['groups'])} 组 + 1 EXT = {len(data['groups'])+1}")
