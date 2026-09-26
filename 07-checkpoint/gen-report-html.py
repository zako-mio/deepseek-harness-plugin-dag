#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""report.md → report.html（自包含暗色主题，轻量 Markdown 子集渲染）
支持: 标题 / 表格 / 无序+有序列表 / 引用块 / 代码块 / 行内 code / 粗体 / 分隔线
"""
import os, re, sys, html
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
SRC = os.path.join(BASE, "report.md")
OUT = os.path.join(BASE, "report.html")

CSS = """
:root{--bg:#0f1117;--panel:#161a22;--border:#2a2f3a;--text:#e6e8ee;--dim:#9aa3b2;--accent:#4f8cff;--ext:#b48a3c;--ok:#2fb98a;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;line-height:1.75;}
header{background:var(--panel);border-bottom:1px solid var(--border);padding:20px 32px;display:flex;align-items:center;gap:14px;flex-wrap:wrap;}
header h1{font-size:18px;font-weight:600;}
header a{color:var(--accent);text-decoration:none;font-size:13px;}
main{padding:26px 32px;max-width:980px;margin:0 auto;}
h1{font-size:22px;margin:8px 0 16px;}
h2{font-size:18px;margin:28px 0 12px;color:#cfd6e4;border-bottom:1px solid var(--border);padding-bottom:8px;}
h3{font-size:15px;margin:20px 0 10px;color:#b8c2d4;}
p,li{font-size:14px;}
ul,ol{padding-left:24px;margin:10px 0;}
li{margin:4px 0;}
blockquote{border-left:3px solid var(--accent);background:#141822;padding:10px 16px;margin:12px 0;color:var(--dim);font-size:13px;}
code{background:#1b2130;border:1px solid #2a3346;border-radius:4px;padding:1px 6px;font-family:Consolas,Monaco,monospace;font-size:12.5px;color:#9fc4ff;}
pre{background:#131822;border:1px solid var(--border);border-radius:8px;padding:14px 16px;overflow:auto;margin:12px 0;}
pre code{background:none;border:none;color:#c8d4e8;font-size:12.5px;}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:13.5px;}
th,td{border:1px solid var(--border);padding:8px 12px;text-align:left;vertical-align:top;}
th{background:#1a2030;color:#cfd6e4;font-weight:600;}
tr:nth-child(even) td{background:#141922;}
td code,th code{font-size:12px;}
hr{border:none;border-top:1px solid var(--border);margin:22px 0;}
a{color:var(--accent);}
"""


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", t)
    return t


def render(md):
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            buf = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(html.escape(lines[i])); i += 1
            i += 1
            out.append("<pre><code>" + "\n".join(buf) + "</code></pre>")
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:
            lv = len(m.group(1)); out.append(f"<h{lv}>{inline(m.group(2))}</h{lv}>"); i += 1; continue
        if re.match(r"^\s*(-{3,}|\*{3,})\s*$", ln):
            out.append("<hr>"); i += 1; continue
        if ln.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip(">").strip()); i += 1
            out.append("<blockquote>" + inline(" ".join(buf)) + "</blockquote>")
            continue
        if ln.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            head = [c.strip() for c in ln.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            t = ["<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"]
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t)); continue
        m = re.match(r"^\s*[-*]\s+(.*)$", ln)
        if m:
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.match(r"^\s*[-*]\s+(.*)$", lines[i]).group(1)); i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>"); continue
        m = re.match(r"^\s*\d+\.\s+(.*)$", ln)
        if m:
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.match(r"^\s*\d+\.\s+(.*)$", lines[i]).group(1)); i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>"); continue
        if ln.strip():
            out.append(f"<p>{inline(ln)}</p>")
        i += 1
    return "\n".join(out)


md = open(SRC, encoding="utf-8").read()
body = render(md)
page = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>任务完成报告 · dsh 插件级 DAG 知识库 0.1.7-rc.2</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <h1>任务完成报告</h1>
  <a href="index.html">← 返回任务目录</a>
  <a href="04-interactive/index.html">交互 DAG 总览</a>
  <a href="README.md">README</a>
  <a href="RC2-0.1.7-DIFF-REPORT.md">差异分析报告</a>
</header>
<main>
{body}
</main>
</body>
</html>
"""
with open(OUT, "w", encoding="utf-8") as f:
    f.write(page)
print(f"[OK] {OUT} ({len(page)} bytes)")
