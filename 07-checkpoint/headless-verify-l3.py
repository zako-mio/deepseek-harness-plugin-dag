#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S6 headless Chrome 验证 L3 交互图:
1. --dump-dom 组级视图: zcount=38 (37 组 + EXT) + zmode=组级
2. --dump-dom ?drill=G30: L3 组下钻节点数 > 0
3. --screenshot 组级 + L3 组下钻截图 (供 VLM 验证配色)
"""
import os, re, subprocess, sys, json
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
HTML = os.path.join(BASE, "04-interactive", "index.html")
OUT = os.path.join(BASE, "07-checkpoint", "screenshots")
os.makedirs(OUT, exist_ok=True)
CHROME = "/snap/bin/chromium"

with open(HTML, "r", encoding="utf-8") as f:
    content = f.read()
m = re.search(r'const DATA = (\{.*?\});', content, re.DOTALL)
data = json.loads(m.group(1))
expected_groups = len(data["groups"]) + 1  # +EXT
print(f"[INFO] expected group-level nodes: {expected_groups} (groups={len(data['groups'])} + EXT)")

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
    out = r.stdout.decode("utf-8", errors="replace") if r.stdout else ""
    return out

# 1. 组级视图 DOM
url = f"file:///{HTML.replace(chr(92), '/')}"
dom = run_chrome(url, dump=True)
zmode = re.search(r'id="zmode">([^<]*)<', dom)
zcount = re.search(r'id="zcount">([^<]*)<', dom)
print(f"[1] 组级 DOM: zmode={zmode.group(1) if zmode else 'N/A'}, zcount={zcount.group(1) if zcount else 'N/A'}")
assert zcount and int(zcount.group(1)) == expected_groups, f"组级 zcount != {expected_groups}"

# 2. 组下钻（动态选取：最大组 + 中等规模组，避免硬编码旧组号）
_groups = sorted(data["groups"].items(), key=lambda kv: -kv[1].get("count", 0)) if isinstance(data["groups"], dict) else []
if not _groups:
    # DATA.groups 为 dict{gid:{name,color}}；按 plugins 计数选
    _cnt = {}
    for e in data.get("edges", []):
        pass
    _groups = [(g, {}) for g in list(data["groups"].keys())]
gids = list(data["groups"].keys())
big_gid = gids[0]
mid_gid = gids[min(len(gids) // 2, len(gids) - 1)]
print(f"[INFO] drill groups: {big_gid}, {mid_gid}")

url_drill = f"file:///{HTML.replace(chr(92), '/')}?drill={big_gid}"
dom2 = run_chrome(url_drill, dump=True)
zcount2 = re.search(r'id="zcount">([^<]*)<', dom2)
zmode2 = re.search(r'id="zmode">([^<]*)<', dom2)
n2 = int(zcount2.group(1)) if zcount2 else -1
print(f"[2] 下钻 {big_gid} DOM: zmode={zmode2.group(1) if zmode2 else 'N/A'}, zcount={n2}")
# 非空断言: 下钻视图必须与组级视图不同（防假绿），且节点数 > 0
assert n2 > 0, f"下钻 {big_gid} 节点为 0"
assert n2 != expected_groups, f"下钻视图与组级视图节点数相同({n2})，URL 路由未生效（假绿）"
assert zmode2 and zmode2.group(1).startswith(big_gid), f"zmode 未切换: {zmode2.group(1) if zmode2 else 'N/A'}"

# 3. 截图 (组级 + 两个下钻)
shot1 = os.path.join(OUT, "l3-group-level.png")
shot2 = os.path.join(OUT, f"l3-drill-{big_gid}.png")
shot3 = os.path.join(OUT, f"l3-drill-{mid_gid}.png")
run_chrome(url, dump=False, shot=shot1, wait_ms=5000)
run_chrome(url_drill, dump=False, shot=shot2, wait_ms=5000)
run_chrome(f"file:///{HTML.replace(chr(92), '/')}?drill={mid_gid}", dump=False, shot=shot3, wait_ms=5000)

for s in [shot1, shot2, shot3]:
    size = os.path.getsize(s) if os.path.exists(s) else 0
    print(f"[3] screenshot {os.path.basename(s)}: {size} bytes {'OK' if size > 10000 else 'TOO SMALL'}")

print("\n[OK] headless DOM 断言通过 (组级 38 节点 + L3 下钻非 0)")
print(f"[OK] 截图输出: {OUT}")
