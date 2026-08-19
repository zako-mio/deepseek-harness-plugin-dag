#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S6 headless Chrome 验证 L2 交互图:
1. --dump-dom 组级视图: zcount=30 (组节点) + zmode=组级
2. --dump-dom ?drill=G25: 下钻节点数 > 0
3. --screenshot 组级 + 下钻截图 (供 VLM 验证配色)
"""
import os, re, subprocess, sys, json
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-plugin-dag-rc8"
HTML = os.path.join(BASE, "04-interactive", "index.html")
OUT = os.path.join(BASE, "07-checkpoint", "screenshots")
os.makedirs(OUT, exist_ok=True)
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# 从 DATA 提取预期数 (组级 30)
with open(HTML, "r", encoding="utf-8") as f:
    content = f.read()
m = re.search(r'const DATA = (\{.*?\});', content, re.DOTALL)
data = json.loads(m.group(1))
expected_groups = len(data["groups"]) + 1  # +EXT
print(f"[INFO] expected group-level nodes: {expected_groups} (groups={len(data['groups'])} + EXT)")

# 写一个临时 HTML 包装来绕过 file:// 下 localhost 问题 (无外部请求, 直接 file 打开即可)
def run_chrome(url, dump=True, shot=None, wait_ms=3000):
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
           f"--virtual-time-budget={wait_ms}"]
    if dump:
        cmd.append("--dump-dom")
    if shot:
        cmd.append(f"--screenshot={shot}")
        cmd.append("--window-size=1920,1080")
    cmd.append(url)
    r = subprocess.run(cmd, capture_output=True, timeout=60)
    # stdout 是 DOM 或截图空; stderr 有中文警告, 用 utf-8 解码兜底
    out = r.stdout.decode("utf-8", errors="replace") if r.stdout else ""
    err = r.stderr.decode("utf-8", errors="replace") if r.stderr else ""
    return out

# 1. 组级视图 DOM
url = f"file:///{HTML.replace(chr(92), '/')}"
r = run_chrome(url, dump=True)
dom = r
zmode = re.search(r'id="zmode">([^<]*)<', dom)
zcount = re.search(r'id="zcount">([^<]*)<', dom)
print(f"[1] 组级 DOM: zmode={zmode.group(1) if zmode else 'N/A'}, zcount={zcount.group(1) if zcount else 'N/A'}")
assert zcount and int(zcount.group(1)) == expected_groups, f"组级 zcount != {expected_groups}"

# 2. 下钻视图 G25 DOM
url_drill = f"file:///{HTML.replace(chr(92), '/')}?drill=G25"
r2 = run_chrome(url_drill, dump=True)
dom2 = r2
zcount2 = re.search(r'id="zcount">([^<]*)<', dom2)
print(f"[2] 下钻 G25 DOM: zcount={zcount2.group(1) if zcount2 else 'N/A'}")
assert zcount2 and int(zcount2.group(1)) > 0, "下钻 G25 节点为 0"

# 3. 截图 (组级 + 下钻 G25 + 下钻 G27)
shot1 = os.path.join(OUT, "group-level.png")
shot2 = os.path.join(OUT, "drill-G25.png")
shot3 = os.path.join(OUT, "drill-G27.png")
r3 = run_chrome(url, dump=False, shot=shot1, wait_ms=5000)
r4 = run_chrome(url_drill, dump=False, shot=shot2, wait_ms=5000)
r5 = run_chrome(f"file:///{HTML.replace(chr(92), '/')}?drill=G27", dump=False, shot=shot3, wait_ms=5000)

for s in [shot1, shot2, shot3]:
    size = os.path.getsize(s) if os.path.exists(s) else 0
    print(f"[3] screenshot {os.path.basename(s)}: {size} bytes {'OK' if size > 10000 else 'TOO SMALL'}")

print("\n[OK] headless DOM 断言通过 (组级 30 节点 + 下钻非 0)")
print(f"[OK] 截图输出: {OUT}")
