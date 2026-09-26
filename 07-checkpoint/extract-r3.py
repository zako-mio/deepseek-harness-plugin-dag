#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 task tool-output 文件提取 R3 JSON 数组 → stage-01-l2-r3.json"""
import json, os, re, sys
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
sys.stdout.reconfigure(encoding='utf-8')

SRC = r"C:\Users\15057\.local\share\opencode\tool-output\tool_00baa1011001Q4I4HIbEOtjPZy"
OUT = os.path.join(BASE, '07-checkpoint', 'stage-01-l2-r3.json')

with open(SRC, "r", encoding="utf-8") as f:
    content = f.read()

# 找 ```json ... ``` 块
m = re.search(r'```json\s*(\[.*?\])\s*```', content, re.DOTALL)
if not m:
    print("[ERR] JSON block not found")
    raise SystemExit(1)

data = json.loads(m.group(1))
print(f"[OK] R3 plugins: {len(data)}")
for p in data:
    print(f"  {p['id']}")

with open(OUT, "w", encoding="utf-8") as f:
    json.dump({"route": "R3-interaction-ui", "scope": "会话交互UI + UI底座 19 插件", "plugins": data}, f, ensure_ascii=False, indent=2)
print(f"[OK] wrote {OUT}")
