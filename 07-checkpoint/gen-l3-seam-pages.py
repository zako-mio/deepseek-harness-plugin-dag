#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L3 S0: 为 13 个新 seam 生成占位参考页 (schema 同现有 seam 页, 待 S1 采集回填 referred_by)"""
import json, os, html, sys
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
EXT = os.path.join(BASE, "01-dag-data", "external-seams.json")
PAGES = os.path.join(BASE, "02-plugin-pages")

with open(EXT, "r", encoding="utf-8") as f:
    ext = json.load(f)

def esc(s):
    return html.escape(str(s), quote=True)

CSS = """
:root{--bg:#0f1117;--panel:#161a22;--border:#2a2f3a;--text:#e6e8ee;--dim:#9aa3b2;--accent:#4f8cff;--ext:#b48a3c;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;line-height:1.6;}
header{background:var(--panel);border-bottom:1px solid var(--border);padding:14px 24px;display:flex;align-items:center;gap:12px;}
header h1{font-size:17px;font-weight:600;}
header .crumb{color:var(--dim);font-size:13px;}
header .crumb a{color:var(--accent);text-decoration:none;}
.badge{background:#3a2f1a;color:#e0b25e;padding:2px 10px;border-radius:20px;font-size:12px;}
main{padding:24px;max-width:1000px;margin:0 auto;}
h2{font-size:18px;margin:26px 0 12px;color:#cfd6e4;border-bottom:1px solid var(--border);padding-bottom:8px;}
p,li{font-size:14px;}
table{border-collapse:collapse;width:100%;margin:10px 0;}
th,td{border:1px solid var(--border);padding:6px 10px;font-size:13px;text-align:left;}
th{background:var(--panel);color:#b8c2d4;}
.pending{background:#2a2410;border:1px solid #5a4a20;border-radius:8px;padding:12px 16px;color:#d4b35e;font-size:13px;}
footer{margin-top:40px;padding:16px 24px;border-top:1px solid var(--border);color:var(--dim);font-size:12px;text-align:center;}
"""

for s in ext["seams"]:
    # 只处理有 l3_note 的新 seam (L3 追加的)
    if "l3_note" not in s:
        continue
    sid = s["id"]
    title = f'{sid} · {s["name"]}'
    out = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} · DeepSeek Harness 插件 DAG</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <span class="crumb"><a href="../index.html">DAG总览</a> / <a href="../03-groups/index.html">组目录</a> / 外部 seam</span>
  <h1>{esc(title)}</h1>
  <span class="badge">外部 seam · L3</span>
</header>
<main>
<div class="pending">⚠️ L3 新 seam（{esc(s.get("l3_note",""))}）。S1 采集后将回填被依赖方（referred_by）与机制分布。</div>
<h2>基座 seam 说明</h2>
<p>{esc(s["description"])}</p>
<table>
<tr><th>包名</th><td>{esc(s["name"])}</td></tr>
<tr><th>源码路径</th><td><code>{esc(s["path"])}</code></td></tr>
<tr><th>TS 文件数</th><td>{s["ts_count"]}</td></tr>
<tr><th>被插件引用</th><td>{s["ref_count"]} 次（待 S1 回填）</td></tr>
<tr><th>来源</th><td>{esc(s["l3_note"])}</td></tr>
</table>
<h2>被依赖（下游）</h2>
<p style="color:var(--dim);">待 L3 采集后回填</p>
</main>
<footer>DeepSeek Harness 插件级 DAG 依赖链分析 · L3 seam 占位页</footer>
</body>
</html>
"""
    with open(os.path.join(PAGES, f"{sid}.html"), "w", encoding="utf-8") as f:
        f.write(out)
    print(f"[OK] {sid}.html")

print(f"\n[OK] wrote {sum(1 for s in ext['seams'] if 'l3_note' in s)} L3 seam placeholder pages")
