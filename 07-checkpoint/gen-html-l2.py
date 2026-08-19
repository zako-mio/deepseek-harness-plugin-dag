#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S4 L2 HTML 生成脚本 (复用 L1 gen-html.py 模板)
数据源: 01-dag-data/webapp-dag.json (134 节点) + external-seams.json (36 seam)
产物:
  02-plugin-pages/{id}.html    每插件一页 (DAG 链式双导航; L1 页重生成含 L2 下游)
  03-groups/G{nn}.html         组索引页 (24 L1 + 5 L2)
  03-groups/index.html         组目录
  04-interactive/index.html    由 inject-data-l2.py 注入 (此脚本不覆盖)
"""
import json, os, html, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0819-plugin-dag-rc7"
DAG = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
EXT = os.path.join(BASE, "01-dag-data", "external-seams.json")
PAGES = os.path.join(BASE, "02-plugin-pages")
GROUPS = os.path.join(BASE, "03-groups")

with open(DAG, "r", encoding="utf-8") as f:
    dag = json.load(f)
with open(EXT, "r", encoding="utf-8") as f:
    ext = json.load(f)

nodes = {n["id"]: n for n in dag["nodes"]}
groups = {g["id"]: g for g in dag["groups"]}
layers = dag["layers"]
edges = dag["edges"]
ext_map = {e["id"]: e for e in ext["seams"]}

# 边索引
out_edges = {}
in_edges = {}
for nid in nodes:
    out_edges[nid] = []
    in_edges[nid] = []
for e in edges:
    out_edges[e["from"]].append(e)
    in_edges[e["to"]].append(e)

ext_dependents = {}
for pid, e in ext_map.items():
    ext_dependents[pid] = e.get("referred_by", [])

def esc(s):
    return html.escape(str(s), quote=True)

def page_url(nid):
    if nid in nodes:
        return f"{nid}.html"
    return f"../02-plugin-pages/{nid}.html" if nid in ext_map else "#"

def link_plugin(nid, label=None):
    if nid in nodes:
        return f'<a href="{nid}.html">{esc(label or nid)}</a>'
    if nid in ext_map:
        return f'<a href="../02-plugin-pages/{nid}.html" class="ext">{esc(label or nid)}</a>'
    return f'<span class="missing">{esc(label or nid)}</span>'

CSS = """
:root{--bg:#0f1117;--panel:#161a22;--border:#2a2f3a;--text:#e6e8ee;--dim:#9aa3b2;--accent:#4f8cff;--ext:#b48a3c;--ok:#2fb98a;--dis:#c0504d;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;line-height:1.6;}
header{background:var(--panel);border-bottom:1px solid var(--border);padding:14px 24px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;}
header h1{font-size:17px;font-weight:600;}
header .crumb{color:var(--dim);font-size:13px;}
header .crumb a{color:var(--accent);text-decoration:none;}
.badge{background:#20324f;color:#7fb0ff;padding:2px 10px;border-radius:20px;font-size:12px;}
.badge.ext{background:#3a2f1a;color:#e0b25e;}
.badge.layer{background:#1d2a24;color:#5fc9a0;}
.badge.l2{background:#2f2440;color:#b48ae0;}
.badge.dis{background:#3a1d1d;color:#e08584;}
main{padding:24px;max-width:1200px;margin:0 auto;}
h2{font-size:18px;margin:26px 0 12px;color:#cfd6e4;border-bottom:1px solid var(--border);padding-bottom:8px;}
h3{font-size:15px;margin:18px 0 8px;color:#b8c2d4;}
p,li{font-size:14px;}
ul{padding-left:22px;}
.dep-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:10px;margin:10px 0;}
.dep-item{background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:10px 12px;}
.dep-item .name{font-weight:600;color:var(--accent);}
.dep-item .mech{display:inline-block;font-size:11px;background:#1d2a3f;color:#7fb0ff;border-radius:4px;padding:1px 6px;margin-left:6px;}
.dep-item .evi{font-size:12px;color:var(--dim);margin-top:4px;font-family:Consolas,monospace;word-break:break-all;}
.dep-item .purpose{font-size:13px;margin-top:4px;}
.ext .name{color:var(--ext);}
.dis .name{color:var(--dis);}
.provides li{font-size:13px;margin:3px 0;}
.evidence{background:#0d1117;border:1px solid var(--border);border-radius:6px;padding:8px 12px;font-family:Consolas,monospace;font-size:12px;color:#9fb0c3;margin:6px 0;word-break:break-all;}
.dagnav{background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:12px 16px;margin:14px 0;}
.dagnav .label{font-size:12px;color:var(--dim);margin-bottom:6px;}
.dagnav .chips{display:flex;flex-wrap:wrap;gap:6px;}
.chip{font-size:12px;background:#1d2a3f;border:1px solid #2b3d5f;border-radius:6px;padding:2px 8px;color:#7fb0ff;text-decoration:none;}
.chip:hover{background:#2b3d5f;}
.chip.ext{background:#3a2f1a;border-color:#5a4422;color:#e0b25e;}
.chip.dis{background:#3a1d1d;border-color:#6a3231;color:#e08584;}
.chip.self{background:#20324f;border-color:#4f8cff;color:#fff;cursor:default;}
.treenav{background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:12px 16px;margin:14px 0;display:flex;flex-wrap:wrap;gap:4px 14px;}
.treenav a{color:var(--dim);font-size:13px;text-decoration:none;}
.treenav a:hover{color:var(--accent);}
.treenav .sep{color:#3a3f4a;}
.layernav{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0;}
.layernav a{font-size:12px;background:#161d2c;border:1px solid var(--border);border-radius:6px;padding:2px 8px;color:var(--dim);text-decoration:none;}
.layernav a.cur{background:#20324f;color:#7fb0ff;border-color:#4f8cff;}
footer{margin-top:40px;padding:16px 24px;border-top:1px solid var(--border);color:var(--dim);font-size:12px;text-align:center;}
table{border-collapse:collapse;width:100%;margin:10px 0;}
th,td{border:1px solid var(--border);padding:6px 10px;font-size:13px;text-align:left;}
th{background:var(--panel);color:#b8c2d4;}
"""

def page_header(title, crumb, extra_badge=""):
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)} · DeepSeek Harness 插件 DAG</title>
<style>{CSS}</style>
</head>
<body>
<header>
  <span class="crumb"><a href="../index.html">DAG总览</a> / <a href="../03-groups/index.html">组目录</a> / {crumb}</span>
  <h1>{esc(title)}</h1>
  {extra_badge}
</header>
<main>
"""

def page_footer():
    return """
</main>
<footer>DeepSeek Harness 插件级 DAG 依赖链分析 · L1 核心集 + L2 web-app bundle · 源码三依据(E1编译/E2运行时/E3组合)逐条溯源</footer>
</body>
</html>
"""

def treenav(gid):
    parts = ['<div class="treenav"><span style="color:var(--dim);font-size:12px;">目录:</span>']
    for g in dag["groups"]:
        parts.append(f'<a href="../03-groups/{g["id"]}.html">{esc(g["name"])}</a>')
    parts.append('</div>')
    return "".join(parts)

def dagnav(nid, kind="plugin"):
    if kind == "plugin":
        ups = out_edges.get(nid, [])
        downs = in_edges.get(nid, [])
        up_ids = sorted(set(e["to"] for e in ups))
        down_ids = sorted(set(e["from"] for e in downs))
        layer_cur = nodes[nid]["layer"] if nid in nodes else None
        layer_ids = sorted(layers.get(str(layer_cur), [])) if layer_cur is not None else []
        html_parts = ['<div class="dagnav">']
        html_parts.append('<div class="label">依赖链 · 上游（该插件依赖的前驱）：</div><div class="chips">')
        if up_ids:
            for u in up_ids:
                cls = "chip dis" if u in ext_map else ("chip ext" if u in ext_map else "chip")
                if u in ext_map:
                    cls = "chip ext"
                html_parts.append(f'<a class="{cls}" href="{page_url(u)}">{esc(u)}</a>')
        else:
            html_parts.append('<span style="color:var(--dim);font-size:12px;">无依赖（基础插件）</span>')
        html_parts.append('</div>')
        html_parts.append('<div class="label" style="margin-top:8px;">依赖链 · 下游（依赖该插件的节点）：</div><div class="chips">')
        if down_ids:
            for d in down_ids:
                cls = "chip"
                if d in ext_map:
                    cls = "chip ext"
                elif d in nodes and nodes[d].get("source_layer") == "L2":
                    cls = "chip l2"
                html_parts.append(f'<a class="{cls}" href="{page_url(d)}">{esc(d)}</a>')
        else:
            html_parts.append('<span style="color:var(--dim);font-size:12px;">无下游（叶子/被消费端）</span>')
        html_parts.append('</div>')
        if layer_cur is not None:
            html_parts.append('<div class="label" style="margin-top:8px;">同一拓扑层（Layer %d，层次遍历层序）：</div><div class="chips">' % layer_cur)
            for s in layer_ids:
                cls = "chip self" if s == nid else "chip"
                html_parts.append(f'<a class="{cls}" href="{page_url(s)}">{esc(s)}</a>')
            html_parts.append('</div>')
        html_parts.append('</div>')
        return "".join(html_parts)
    deps = ext_dependents.get(nid, [])
    parts = ['<div class="dagnav"><div class="label">被核心/Web 集插件依赖（下游消费者）：</div><div class="chips">']
    if deps:
        for d in sorted(deps):
            cls = "chip ext" if d in ext_map else "chip"
            parts.append(f'<a class="{cls}" href="{page_url(d)}">{esc(d)}</a>')
    else:
        parts.append('<span style="color:var(--dim);font-size:12px;">无核心集消费者</span>')
    parts.append('</div></div>')
    return "".join(parts)

def layernav(nid):
    cur = nodes[nid]["layer"]
    prev_layer = str(cur - 1) if cur > 0 else None
    next_layer = str(cur + 1) if str(cur + 1) in layers else None
    parts = ['<div class="layernav">']
    if prev_layer is not None:
        prev_ids = sorted(layers[prev_layer])
        parts.append(f'<a href="{page_url(prev_ids[0])}">↑ Layer {prev_layer}（{len(prev_ids)} 插件）</a>')
    parts.append(f'<span class="chip self">Layer {cur}</span>')
    if next_layer is not None:
        next_ids = sorted(layers[next_layer])
        parts.append(f'<a href="{page_url(next_ids[0])}">↓ Layer {next_layer}（{len(next_ids)} 插件）</a>')
    parts.append('</div>')
    return "".join(parts)

# ---------- 1. 生成插件页 (134: 76 L1 + 58 L2) ----------
os.makedirs(PAGES, exist_ok=True)
count = 0
for nid, n in nodes.items():
    gid = n["group"]
    gname = n["group_name"]
    title = f'{nid} · {n["name"]}'
    badges = [f'<span class="badge">Layer {n["layer"]}</span>', f'<span class="badge">{esc(gid)}</span>']
    if n.get("source_layer") == "L2":
        badges.append('<span class="badge l2">L2 web-app</span>')
    if nid in {d["node"] for d in []} or False:
        pass
    out = [page_header(title, f'{esc(gid)} {esc(gname)}', "".join(badges))]
    out.append(treenav(gid))
    out.append(dagnav(nid))
    out.append(layernav(nid))
    # 元信息
    out.append('<h2>插件信息</h2>')
    src_path = n.get("path", "")
    extra_rows = ""
    if n.get("source_layer") == "L2":
        extra_rows += '<tr><th>来源层</th><td>L2 web-app bundle（base 之上装配）</td></tr>'
    if n.get("override_base"):
        extra_rows += f'<tr><th>覆盖 base 行</th><td>覆盖 <a href="dsh-api-gateway.html">dsh-api-gateway</a>（web patch 以 {esc(n["override_base"])} 取代）</td></tr>'
    out.append(f'<table><tr><th>包名</th><td>{esc(n["name"])}</td></tr><tr><th>分组</th><td>{esc(gid)} · {esc(gname)}</td></tr><tr><th>拓扑层</th><td>Layer {n["layer"]}（层次遍历：被依赖方先于依赖方）</td></tr><tr><th>源码路径</th><td><code>{esc(src_path)}</code></td></tr>{extra_rows}</table>')
    # 实现逻辑
    out.append('<h2>① 实现逻辑</h2>')
    out.append(f'<p>{esc(n["implementation"])}</p>')
    # 注册内容
    out.append('<h2>② 注册/提供（provides）</h2>')
    out.append('<ul class="provides">')
    for p in n.get("provides", []):
        out.append(f'<li>{esc(p)}</li>')
    out.append('</ul>')
    # 依赖(上游)
    out.append('<h2>③ 依赖（depends_on · 上游前驱）</h2>')
    ups = sorted(out_edges.get(nid, []), key=lambda e: e["to"])
    if ups:
        out.append('<div class="dep-list">')
        for e in ups:
            dep = e["to"]
            evi = e.get("evidence", "")
            mech = e.get("mechanism", "E1")
            purp = e.get("purpose", "")
            cls = "dep-item ext" if dep in ext_map else "dep-item"
            out.append(f'<div class="{cls}"><span class="name">{link_plugin(dep)}</span><span class="mech">{esc(mech)}</span>')
            if purp:
                out.append(f'<div class="purpose">{esc(purp)}</div>')
            if evi:
                out.append(f'<div class="evi">{esc(evi)}</div>')
            out.append('</div>')
        out.append('</div>')
    else:
        out.append('<p style="color:var(--dim);">无依赖（基础插件）</p>')
    # 被依赖(下游)
    out.append('<h2>④ 被依赖（dependents · 下游消费者）</h2>')
    downs = sorted(in_edges.get(nid, []), key=lambda e: e["from"])
    if downs:
        out.append('<div class="dep-list">')
        for e in downs:
            fr = e["from"]
            evi = e.get("evidence", "")
            purp = e.get("purpose", "")
            out.append(f'<div class="dep-item"><span class="name">{link_plugin(fr)}</span>')
            if purp:
                out.append(f'<div class="purpose">{esc(purp)}</div>')
            if evi:
                out.append(f'<div class="evi">{esc(evi)}</div>')
            out.append('</div>')
        out.append('</div>')
    else:
        out.append('<p style="color:var(--dim);">无下游（叶子/被消费端）</p>')
    out.append(page_footer())
    with open(os.path.join(PAGES, f"{nid}.html"), "w", encoding="utf-8") as f:
        f.write("".join(out))
    count += 1
print(f"[OK] plugin pages: {count}")

# ---------- 2. 外部 seam 参考页 ----------
for sid, s in ext_map.items():
    title = f'{sid} · {s["name"]}'
    out = [page_header(title, '外部基座 seam', '<span class="badge ext">外部 seam</span>')]
    out.append(treenav(None))
    out.append(dagnav(sid, kind="seam"))
    out.append('<h2>基座 seam 说明</h2>')
    out.append(f'<p>{esc(s.get("description") or "（抽象基座，被核心/Web 集插件依赖）")}</p>')
    out.append(f'<table><tr><th>包名</th><td>{esc(s["name"])}</td></tr><tr><th>源码路径</th><td><code>{esc(s.get("path") or "")}</code></td></tr><tr><th>被插件引用</th><td>{s.get("ref_count", 0)} 次</td></tr></table>')
    out.append('<h2>被依赖（下游）</h2>')
    deps = sorted(s.get("referred_by", []))
    if deps:
        out.append('<div class="dep-list">')
        for d in deps:
            out.append(f'<div class="dep-item"><span class="name">{link_plugin(d)}</span></div>')
        out.append('</div>')
    else:
        out.append('<p style="color:var(--dim);">无消费者</p>')
    out.append('<h2>依赖机制分布</h2>')
    out.append(f'<p>{"、".join(esc(m) for m in s.get("mechanisms", []))}</p>')
    out.append(page_footer())
    with open(os.path.join(PAGES, f"{sid}.html"), "w", encoding="utf-8") as f:
        f.write("".join(out))
print(f"[OK] ext seam pages: {len(ext_map)}")

# ---------- 3. 组索引页 (29) ----------
os.makedirs(GROUPS, exist_ok=True)
for gid, g in groups.items():
    gname = g["name"]
    plist = g["plugins"]
    out = [page_header(f'{gid} · {gname} 组', '组索引', f'<span class="badge">{len(plist)} 插件</span>')]
    out.append(treenav(gid))
    out.append('<h2>组内插件</h2>')
    out.append('<table><tr><th>插件</th><th>拓扑层</th><th>来源</th><th>核心功能</th></tr>')
    for pid in plist:
        if pid in nodes:
            n = nodes[pid]
            impl = n["implementation"][:60] + ("…" if len(n["implementation"]) > 60 else "")
            src = 'L2' if n.get("source_layer") == "L2" else 'L1'
            out.append(f'<tr><td><a href="../02-plugin-pages/{pid}.html">{esc(pid)}</a></td><td>L{n["layer"]}</td><td>{src}</td><td>{esc(impl)}</td></tr>')
    out.append('</table>')
    out.append(page_footer())
    with open(os.path.join(GROUPS, f"{gid}.html"), "w", encoding="utf-8") as f:
        f.write("".join(out))
print(f"[OK] group pages: {len(groups)}")

# 组目录
out = [page_header('插件分组目录', '目录')]
out.append('<div class="treenav">')
for gid, g in groups.items():
    out.append(f'<a href="{gid}.html">{esc(gid)} {esc(g["name"])}（{len(g["plugins"])}）</a>')
out.append('</div>')
out.append('<h2>外部 seam 基座</h2><ul>')
for sid, s in ext_map.items():
    out.append(f'<li><a href="../02-plugin-pages/{sid}.html">{esc(sid)}</a> · {esc(s.get("description","")[:60])}</li>')
out.append('</ul>')
out.append(page_footer())
with open(os.path.join(GROUPS, "index.html"), "w", encoding="utf-8") as f:
    f.write("".join(out))
print(f"[OK] groups/index.html written")

print(f"\n[SUMMARY] plugin pages={count} ({len(nodes)} nodes), ext={len(ext_map)}, groups={len(groups)}")
