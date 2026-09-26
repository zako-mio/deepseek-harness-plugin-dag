#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S4 L3 HTML 生成脚本 (复用 gen-html-l2.py 模板)

数据源: 01-dag-data/webapp-dag.json (239 节点 / 50 组) + external-seams.json (73 seam)
       + 07-checkpoint/v017/special-modules.json (8 特殊模块)

产物 (按 --only 分阶段):
  02-plugin-pages/{id}.html    每插件一页 + 外部 seam 参考页   (--only plugin-pages)
  03-groups/G{nn}.html         组索引页                        (--only groups-pages)
  03-groups/index.html         分组索引 (区 → 功能簇 → 组卡片) (--only groups-index)
  08-special-modules/          特殊模块页 (8)                  (--only special)

====================== ⚠️ 误跑保护 (根因修复) ======================
本脚本此前**没有 argparse**: 命令行上传 --help 或任何参数都会被静默忽略并
**直接全量执行**。2026-09-27 02:43 即因一次 `python3 gen-html-l3.py --help`
误跑，重写了 02-plugin-pages(239) + 03-groups(51) + 08-special-modules(8)，
把 gen-plugin-dyn.py 事后注入的「动态 DAG」区块冲掉 (每页约 -3982 字符)，
靠 git checkout 回滚。现已改为「默认 dry-run + 显式 --write」。
⛔ 不要再用试探性参数调用本脚本；确认要写盘时必须显式带 `--write`。

用法:
  python3 gen-html-l3.py                                  # dry-run 全量 (零写盘)
  python3 gen-html-l3.py --only groups-index              # dry-run 单阶段 (零写盘)
  python3 gen-html-l3.py --only groups-index --write      # 真正落盘
  python3 gen-html-l3.py --only all --write               # 全量落盘 (原行为)

================== ⚠️⚠️ 关键顺序约束 (事故机制) ==================
本脚本生成的插件页**不包含**「动态 DAG」区块 —— 该区块由 gen-plugin-dyn.py
在生成之后**事后注入**。因此:
  跑完 `--only plugin-pages --write` 或 `--only all --write` 之后，
  **必须补跑 `python3 gen-plugin-dyn.py`** 重新注入动态 DAG，
  否则插件页会丢失该区块 (每页约 -3982 字符)。
==================================================================
"""
import json, os, html, sys, argparse, re
import glob as _glob

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
DAG = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
EXT = os.path.join(BASE, "01-dag-data", "external-seams.json")
SPECIAL = os.path.join(CHK := os.path.join(BASE, "07-checkpoint"), "v017", "special-modules.json")
PAGES = os.path.join(BASE, "02-plugin-pages")
GROUPS = os.path.join(BASE, "03-groups")
SPECIAL_OUT = os.path.join(BASE, "08-special-modules")

STAGES = ("all", "plugin-pages", "groups-pages", "groups-index", "special")

_ap = argparse.ArgumentParser(
    description="DeepSeek Harness 插件 DAG · HTML 生成器 (默认 dry-run，需显式 --write 才落盘)")
_ap.add_argument("--only", choices=STAGES, default="all",
                 help="只生成某一阶段；默认 all (需配合 --write 才真正写盘)")
_ap.add_argument("--write", action="store_true",
                 help="真正写入文件；缺省为 dry-run (只打印将写入的路径，零写盘)")
ARGS = _ap.parse_args()
ONLY = ARGS.only
WRITE = ARGS.write

_PENDING = []


def emit(path, text):
    """暂存待写入内容；是否落盘由 flush() 依据 --write 决定 (dry-run 零写盘)。"""
    _PENDING.append((path, text))


def flush():
    if WRITE:
        for p, t in _PENDING:
            d = os.path.dirname(p)
            if d:
                os.makedirs(d, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(t)
        print(f"\n[WRITE] 已写入 {len(_PENDING)} 个文件 (--only {ONLY} --write)")
    else:
        print(f"\n[DRY-RUN] --only {ONLY} · 将写入 {len(_PENDING)} 个文件 (零写盘；加 --write 才落盘):")
        for p, t in _PENDING:
            print(f"   - {os.path.relpath(p, BASE)}  ({len(t)} bytes)")
        print("[DRY-RUN] 未修改任何文件。")


with open(DAG, "r", encoding="utf-8") as f:
    dag = json.load(f)
with open(EXT, "r", encoding="utf-8") as f:
    ext = json.load(f)
with open(SPECIAL, "r", encoding="utf-8") as f:
    special_data = json.load(f)

nodes = {n["id"]: n for n in dag["nodes"]}
groups = {g["id"]: g for g in dag["groups"]}
layers = dag["layers"]
edges = dag["edges"]
ext_map = {e["id"]: e for e in ext["seams"]}
special_modules = special_data.get("special_modules", [])

# 边索引
out_edges = {}
in_edges = {}
for nid in nodes:
    out_edges[nid] = []
    in_edges[nid] = []
for e in edges:
    out_edges[e["from"]].append(e)
    in_edges[e["to"]].append(e)


def esc(s):
    return html.escape(str(s), quote=True)


def wbrify(s):
    """转义后仅在 - 与 / 之后插入 <wbr>，给长 id/路径提供软换行机会，避免硬断词。"""
    return re.sub(r"([-/])", r"\1<wbr>", esc(s))


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
.badge.l3{background:#1d3a30;color:#5fd0a8;}
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
.chip.l2{background:#2f2440;border-color:#4a3560;color:#b48ae0;}
.chip.l3{background:#1d3a30;border-color:#2f5a4a;color:#5fd0a8;}
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
.whybox{background:#0d1a14;border:1px solid #2f5a4a;border-radius:8px;padding:14px 18px;margin:10px 0;}
.whybox .tag{color:#5fc9a0;font-size:12px;font-weight:600;letter-spacing:1px;}
.whybox p{font-size:14px;color:#cfe8dd;margin:6px 0;}
.whybox .hist{font-size:13px;color:var(--dim);margin-top:8px;}
.whybox .src{font-size:11px;color:var(--dim);margin-top:8px;}
.whybox .src a{color:#7fb0ff;text-decoration:none;word-break:break-all;}
.whybox .src a:hover{text-decoration:underline;}
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


FOOTER = '<footer>DeepSeek Harness 插件级 DAG 依赖链分析 · L1 核心集 + L2 web-app + L3 其余插件 · 源码三依据(E1编译/E2运行时/E3组合)逐条溯源</footer>'


def page_footer():
    return "\n</main>\n" + FOOTER + "\n</body>\n</html>\n"


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
                cls = "chip ext" if u in ext_map else "chip"
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
                elif d in nodes and nodes[d].get("source_layer") == "L3":
                    cls = "chip l3"
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
    deps = ext_map.get(nid, {}).get("referred_by", [])
    parts = ['<div class="dagnav"><div class="label">被核心/Web/L3 集插件依赖（下游消费者）：</div><div class="chips">']
    if deps:
        for d in sorted(deps):
            cls = "chip ext" if d in ext_map else "chip"
            parts.append(f'<a class="{cls}" href="{page_url(d)}">{esc(d)}</a>')
    else:
        parts.append('<span style="color:var(--dim);font-size:12px;">无消费者</span>')
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


# =====================================================================
# 1. 插件页 (239) + 外部 seam 参考页 (73)
# =====================================================================
def gen_plugin_pages():
    count = 0
    for nid, n in nodes.items():
        gid = n["group"]
        gname = n["group_name"]
        title = f'{nid} · {n["name"]}'
        badges = [f'<span class="badge">Layer {n["layer"]}</span>', f'<span class="badge">{esc(gid)}</span>']
        src_layer = n.get("source_layer", "L1")
        if src_layer == "L2":
            badges.append('<span class="badge l2">L2 web-app</span>')
        elif src_layer == "L3":
            badges.append('<span class="badge l3">L3 其余</span>')
        out = [page_header(title, f'{esc(gid)} {esc(gname)}', "".join(badges))]
        out.append(treenav(gid))
        out.append(dagnav(nid))
        out.append(layernav(nid))
        # 元信息
        out.append('<h2>插件信息</h2>')
        src_path = n.get("path", "")
        extra_rows = ""
        if src_layer == "L2":
            extra_rows += '<tr><th>来源层</th><td>L2 web-app bundle（base 之上装配）</td></tr>'
        elif src_layer == "L3":
            extra_rows += '<tr><th>来源层</th><td>L3 其余插件（独立于 bundle 装配的扩展/变体/示例）</td></tr>'
        if n.get("override_base"):
            extra_rows += f'<tr><th>覆盖 base 行</th><td>覆盖 <a href="dsh-api-gateway.html">dsh-api-gateway</a>（web patch 以 {esc(n["override_base"])} 取代）</td></tr>'
        out.append(f'<table><tr><th>包名</th><td>{esc(n["name"])}</td></tr><tr><th>分组</th><td>{esc(gid)} · {esc(gname)}</td></tr><tr><th>拓扑层</th><td>Layer {n["layer"]}（层次遍历：被依赖方先于依赖方）</td></tr><tr><th>源码路径</th><td><code>{esc(src_path)}</code></td></tr>{extra_rows}</table>')
        # 为什么需要它（设计初衷）
        why_data = n.get("why", {})
        if why_data and why_data.get("text"):
            why_parts = ['<div class="whybox"><span class="tag">为什么需要它 · 设计初衷</span>']
            why_parts.append(f'<p>{esc(why_data["text"])}</p>')
            if why_data.get("history"):
                why_parts.append(f'<div class="hist">📜 {esc(why_data["history"])}</div>')
            srcs = why_data.get("sources", [])
            if srcs:
                src_links = "".join(f'<a href="{esc(u)}" target="_blank">{esc(u)}</a><br>' for u in srcs)
                why_parts.append(f'<div class="src">📚 来源：<br>{src_links}</div>')
            why_parts.append('</div>')
            out.append("".join(why_parts))
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
        # 双身份: 插件也是 seam 接口, 补充 seam 侧被依赖
        if nid in ext_map:
            s = ext_map[nid]
            seam_deps = sorted(s.get("referred_by", []))
            if seam_deps:
                out.append('<h2>⑤ 作为 seam 接口被依赖（seam referred_by）</h2>')
                out.append('<div class="dep-list">')
                for d in seam_deps:
                    if d != nid:
                        out.append(f'<div class="dep-item ext"><span class="name">{link_plugin(d)}</span></div>')
                out.append('</div>')
        out.append(page_footer())
        emit(os.path.join(PAGES, f"{nid}.html"), "".join(out))
        count += 1
    print(f"[GEN] plugin pages: {count}")

    # 外部 seam 参考页 (跳过 DAG 双身份节点, 由插件页承载)
    dual_ids = set(nodes.keys()) & set(ext_map.keys())
    print(f"[INFO] dual-identity ids (DAG节点+seam, 走插件页): {sorted(dual_ids)}")
    for sid, s in ext_map.items():
        if sid in dual_ids:
            print(f"[SKIP] seam page for {sid} (dual-identity, plugin page carries)")
            continue
        title = f'{sid} · {s["name"]}'
        out = [page_header(title, '外部基座 seam', '<span class="badge ext">外部 seam</span>')]
        out.append(treenav(None))
        out.append(dagnav(sid, kind="seam"))
        out.append('<h2>基座 seam 说明</h2>')
        out.append(f'<p>{esc(s.get("description") or "（抽象基座，被核心/Web/L3 集插件依赖）")}</p>')
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
        emit(os.path.join(PAGES, f"{sid}.html"), "".join(out))
    print(f"[GEN] ext seam pages: {len(ext_map)} (含 {len(dual_ids)} 个双身份跳过)")


# =====================================================================
# 2. 组索引页 (50)
# =====================================================================
def gen_group_pages():
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
                src = n.get("source_layer", "L1")
                src_lbl = {'L1': 'L1', 'L2': 'L2', 'L3': 'L3'}.get(src, src)
                out.append(f'<tr><td><a href="../02-plugin-pages/{pid}.html">{esc(pid)}</a></td><td>L{n["layer"]}</td><td>{src_lbl}</td><td>{esc(impl)}</td></tr>')
        out.append('</table>')
        out.append(page_footer())
        emit(os.path.join(GROUPS, f"{gid}.html"), "".join(out))
    print(f"[GEN] group pages: {len(groups)}")


# =====================================================================
# 3. 分组索引 (03-groups/index.html) — 区 → 功能簇 → 组卡片 (重设计)
# =====================================================================
PALETTE = ["#4f8cff", "#7b61ff", "#2fb98a", "#e8933b", "#e05563", "#3b9fe0", "#9a7bf0", "#e0a03b",
           "#3bc4a0", "#d0546b", "#6c8df5", "#b48a3c", "#54a0e8", "#8a5cf0", "#3ab7c4", "#e07b54",
           "#5f8de0", "#9b6bd4", "#4aa8a0", "#d06a4a", "#6b9bd4", "#b07bd4", "#4ac48e", "#d48a5b"]

# 固定二级功能簇表 (主 Agent 裁定, 禁改): (fid, 名称, 区, 组列表)
GROUP_CLUSTERS = [
    ("F1", "运行时基座", "L1", ["G04", "G09", "G45", "G42", "G22"]),
    ("F2", "会话与上下文", "L1", ["G33", "G34", "G07", "G17", "G44", "G15", "G21"]),
    ("F3", "智能与协议", "L1", ["G23", "G25", "G26"]),
    ("F4", "工具与执行面", "L1", ["G36", "G37", "G41", "G47", "G18", "G30", "G38", "G16", "G40", "G10", "G28"]),
    ("F5", "宿主与工作区", "L1", ["G03", "G35", "G49"]),
    ("F6", "客户端 UI", "L2", ["G06"]),
    ("F7", "客户端运行时与宿主接入", "L2", ["G05", "G02", "G08", "G11", "G12", "G14", "G20", "G31", "G50"]),
    ("F8", "协议与远程", "L3", ["G01", "G24", "G32", "G39", "G43"]),
    ("F9", "实验与扩展", "L3", ["G13", "G19", "G27", "G29", "G46", "G48"]),
]

REGION_NAME = {"L1": "L1 核心集", "L2": "L2 web-app", "L3": "L3 其余可挂载"}
REGION_COLOR = {"L1": "#4f8cff", "L2": "#9a7bf0", "L3": "#2fb98a"}
# 区描述: 90 / 82 / 67 由节点自身 source_layer 派生, 不硬编码
REGION_DESC = {
    "L1": "bundle/base 装配的核心插件",
    "L2": "bundle/web-app 装配、含客户端 UI 的插件",
    "L3": "5 个 bundle 之外、可独立挂载的插件",
}

GROUPS_INDEX_CSS = """
:root{--bg:#0f1117;--panel:#161a22;--border:#2a2f3a;--text:#e6e8ee;--dim:#9aa3b2;--accent:#4f8cff;--ext:#b48a3c;--ok:#2fb98a;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;line-height:1.6;}
header{background:var(--panel);border-bottom:1px solid var(--border);padding:16px 28px;}
header .crumb{color:var(--dim);font-size:13px;}
header .crumb a{color:var(--accent);text-decoration:none;}
header .crumb a:hover{text-decoration:underline;}
header h1{font-size:19px;margin-top:6px;}
header .sub{color:var(--dim);font-size:13px;margin-top:4px;}
main{padding:22px 28px 40px;max-width:1180px;margin:0 auto;}
h2{font-size:17px;margin:26px 0 6px;color:#cfd6e4;padding-bottom:7px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;flex-wrap:wrap;scroll-margin-top:12px;}
h2 .dot{width:10px;height:10px;border-radius:3px;display:inline-block;flex:0 0 auto;}
h2 .fcount,h3 .fcount{font-size:12px;color:var(--dim);font-weight:400;}
h3{font-size:14px;margin:18px 0 8px;color:#b8c2d4;display:flex;align-items:center;gap:8px;flex-wrap:wrap;scroll-margin-top:12px;}
h3 .fid{background:#20324f;color:#7fb0ff;border-radius:5px;padding:1px 8px;font-size:12px;font-weight:600;}
.navbox{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:10px 16px;margin:14px 0;}
.navrow{display:flex;flex-wrap:wrap;align-items:center;gap:8px;padding:5px 0;}
.navrow+.navrow{border-top:1px dashed #232a36;}
.navrow .rlabel{font-size:13px;font-weight:600;min-width:96px;color:#cfd6e4;}
.navrow a.chip{font-size:12px;background:#1d2a3f;border:1px solid #2b3d5f;border-radius:20px;padding:2px 10px;color:#9fc0ff;text-decoration:none;}
.navrow a.chip:hover{background:#2b3d5f;color:#fff;}
.navrow a.chip.znav{background:#20283a;border-color:#3a4a66;}
.caliber{background:#161d2c;border:1px solid #26314a;border-radius:8px;padding:8px 13px;font-size:12px;color:#9fb0c3;margin:8px 0 0;}
.caliber b{color:#cfd6e4;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin:10px 0 6px;}
.gcell{display:flex;min-width:0;}
a.gcard{display:block;flex:1 1 auto;width:100%;background:var(--panel);border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:9px;padding:11px 13px;text-decoration:none;color:inherit;transition:transform .12s ease,border-color .12s ease,box-shadow .12s ease,background .12s ease;}
a.gcard:hover{transform:translateY(-2px);border-color:#4f8cff;box-shadow:0 6px 18px rgba(0,0,0,.45);background:linear-gradient(180deg,#1d2533,#161a22);}
a.gcard:focus-visible{outline:2px solid #4f8cff;outline-offset:2px;}
a.gcard.small .gname{font-size:14px;}
a.gcard.mid{padding:13px 15px;}
a.gcard.mid .gname{font-size:16px;}
a.gcard.big{padding:16px 18px;background:linear-gradient(180deg,#1b2330,#161a22);border-left-width:6px;}
a.gcard.big .gname{font-size:19px;font-weight:600;}
.ghead{display:flex;align-items:center;gap:7px;flex-wrap:wrap;}
.swatch{width:12px;height:12px;border-radius:3px;flex:0 0 auto;}
.gid{font-family:Consolas,monospace;font-size:12px;color:var(--dim);}
.gname{color:var(--accent);}
a.gcard:hover .gname{text-decoration:underline;}
.gopen{margin-left:auto;color:var(--dim);font-size:14px;flex:0 0 auto;}
a.gcard:hover .gopen{color:#fff;}
.gmeta{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0;}
.tag{font-size:11px;background:#1d2a3f;color:#8fa8c8;border-radius:5px;padding:1px 7px;white-space:nowrap;}
.tag.n{background:#20324f;color:#7fb0ff;}
.tag.pure{background:#1d2a24;color:#5fc9a0;}
.tag.mix{background:#3a2f1a;color:#e0b25e;}
.gbar{height:5px;background:#0d1117;border-radius:3px;overflow:hidden;}
.gbar i{display:block;height:100%;border-radius:3px;}
details.fold{margin:22px 0 0;}
details.fold>summary{cursor:pointer;list-style:none;font-size:17px;color:#cfd6e4;padding:8px 0;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;flex-wrap:wrap;scroll-margin-top:12px;}
details.fold>summary::-webkit-details-marker{display:none;}
details.fold>summary::before{content:"\\25B8";color:var(--dim);font-size:13px;}
details.fold[open]>summary::before{content:"\\25BE";}
details.fold>summary:hover{color:#fff;}
.note{background:#0d1a14;border:1px solid #2f5a4a;border-radius:8px;padding:9px 13px;font-size:12.5px;color:#a7cbbd;margin:10px 0;}
.sgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:12px 0;}
.scard{background:var(--panel);border:1px solid var(--border);border-radius:9px;padding:9px 11px;min-width:0;}
.shead{display:flex;align-items:baseline;gap:6px;min-width:0;}
.shead .rank{font-size:11px;color:var(--dim);font-family:Consolas,monospace;flex:0 0 auto;}
.shead a{color:#e0b25e;text-decoration:none;font-size:12.5px;font-family:Consolas,monospace;word-break:normal;overflow-wrap:break-word;min-width:0;}
.shead a:hover{text-decoration:underline;}
.spath{font-family:Consolas,monospace;font-size:11px;color:var(--dim);margin:4px 0;word-break:normal;overflow-wrap:break-word;}
.smeta{display:flex;gap:10px;font-size:11px;color:#8fa8c8;margin-bottom:6px;flex-wrap:wrap;}
.sbar{height:4px;background:#0d1117;border-radius:3px;overflow:hidden;}
.sbar i{display:block;height:100%;border-radius:3px;background:#b48a3c;}
.smgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px;margin:10px 0;}
.smcard{background:var(--panel);border:1px solid var(--border);border-radius:9px;padding:11px 13px;}
.smcard a{color:var(--accent);text-decoration:none;font-size:13.5px;font-weight:600;}
.smcard a:hover{text-decoration:underline;}
.smcard p{font-size:12px;color:var(--dim);margin-top:5px;}
@media(max-width:900px){.sgrid{grid-template-columns:repeat(2,minmax(0,1fr));}}
@media(max-width:620px){.sgrid{grid-template-columns:minmax(0,1fr);}}
footer{margin-top:36px;padding:16px 28px;border-top:1px solid var(--border);color:var(--dim);font-size:12px;text-align:center;}
"""


def _assert_cluster_coverage(group_ids):
    flat = [g for _, _, _, gs in GROUP_CLUSTERS for g in gs]
    dup = sorted({g for g in flat if flat.count(g) > 1})
    missing = sorted(set(group_ids) - set(flat))
    extra = sorted(set(flat) - set(group_ids))
    ok = (len(flat) == len(group_ids) == 50 and not dup and not missing and not extra)
    print(f"[ASSERT] 功能簇表展开须恰好覆盖 50 组: 展开 {len(flat)} / 实际 {len(group_ids)}"
          f" / 重复 {dup} / 遗漏 {missing} / 越界 {extra} -> {'PASS' if ok else 'FAIL'}")
    if not ok:
        raise SystemExit("[FAIL] 9 簇展开未恰好覆盖 50 组 (无遗漏/无重复)")


def _group_stats():
    by_group = {}
    for n in dag["nodes"]:
        by_group.setdefault(n["group"], []).append(n)
    stats = {}
    for g in dag["groups"]:
        gid = g["id"]
        ns = by_group.get(gid, [])
        cnt = {}
        for n in ns:
            k = n.get("source_layer", "L1")
            cnt[k] = cnt.get(k, 0) + 1
        ls = [n["layer"] for n in ns]
        stats[gid] = {
            "id": gid, "name": g["name"], "plugins": g["plugins"],
            "n": len(ns), "src": cnt,
            "lmin": min(ls) if ls else None, "lmax": max(ls) if ls else None,
        }
    return stats


def _src_badge(src):
    keys = [k for k in ("L1", "L2", "L3") if src.get(k)]
    if len(keys) == 1:
        return f"纯 {keys[0]}", "pure"
    return "混合 " + "+".join(keys), "mix"


def _layer_span(st):
    if st["lmin"] is None:
        return "层 —"
    if st["lmin"] == st["lmax"]:
        return f'层 {st["lmin"]}'
    return f'层 {st["lmin"]}–{st["lmax"]}'


def _group_card(st, color, maxn):
    badge, bcls = _src_badge(st["src"])
    size_cls = "big" if st["n"] >= 20 else ("mid" if st["n"] >= 8 else "small")
    bar = max(6, round(100 * st["n"] / maxn))
    return (
        '<div class="gcell">'
        f'<a class="gcard {size_cls}" href="{st["id"]}.html" style="border-left-color:{color}">'
        '<div class="ghead">'
        f'<span class="swatch" style="background:{color}"></span>'
        f'<span class="gid">{st["id"]}</span>'
        f'<span class="gname">{esc(st["name"])}</span>'
        '<span class="gopen">›</span>'
        '</div>'
        f'<div class="gmeta"><span class="tag n">{st["n"]} 插件</span>'
        f'<span class="tag">{esc(_layer_span(st))}</span>'
        f'<span class="tag {bcls}">{esc(badge)}</span></div>'
        f'<div class="gbar"><i style="width:{bar}%;background:{color}"></i></div>'
        '</a></div>'
    )


def _seam_card(rank, s, maxref):
    ref = s.get("ref_count", 0)
    bar = max(2, round(100 * ref / maxref))
    return (
        '<div class="scard">'
        f'<div class="shead"><span class="rank">#{rank}</span>'
        f'<a href="../02-plugin-pages/{esc(s["id"])}.html">{wbrify(s["id"])}</a></div>'
        f'<div class="spath">{wbrify(s.get("path") or "—")}</div>'
        f'<div class="smeta"><span>{s.get("ts_count", 0)} TS 文件</span>'
        f'<span>被 {ref} 个插件引用</span></div>'
        f'<div class="sbar"><i style="width:{bar}%"></i></div>'
        '</div>'
    )


def gen_groups_index():
    group_ids = [g["id"] for g in dag["groups"]]
    _assert_cluster_coverage(group_ids)
    st = _group_stats()
    gcolor = {gid: PALETTE[i % len(PALETTE)] for i, gid in enumerate(sorted(st.keys()))}
    maxn = max(v["n"] for v in st.values())

    src_tot = {}
    for n in dag["nodes"]:
        k = n.get("source_layer", "L1")
        src_tot[k] = src_tot.get(k, 0) + 1

    o = []
    o.append('<!DOCTYPE html>')
    o.append('<html lang="zh-CN">')
    o.append('<head>')
    o.append('<meta charset="UTF-8">')
    o.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    o.append('<title>分组索引 · DeepSeek Harness 插件 DAG</title>')
    o.append('<style>' + GROUPS_INDEX_CSS + '</style>')
    o.append('</head>')
    o.append('<body>')
    o.append('<header>')
    out_nav = '<a href="../index.html">DAG 总览</a> / <span>分组索引</span>'
    o.append(f'<div class="crumb">{out_nav}</div>')
    o.append('<h1>分组索引 · 按区 + 功能簇重排</h1>')
    o.append('<div class="sub">50 组按装配来源（L1/L2/L3）划分为 3 区、9 个功能簇；'
             '组内多数 source_layer 决定归区（并列按 L1&gt;L2&gt;L3）。点击任意组卡片进入组页。</div>')
    o.append('</header>')
    o.append('<main>')

    # 顶部锚点导航: 3 区 + 9 簇
    o.append('<div class="navbox">')
    o.append('<div class="navrow"><span class="rlabel">区（3）</span>')
    for rid in ("L1", "L2", "L3"):
        ng = sum(1 for _, _, r, _ in GROUP_CLUSTERS if r == rid)
        o.append(f'<a class="chip znav" href="#{rid}">{esc(REGION_NAME[rid])} · {ng} 组</a>')
    o.append('</div>')
    o.append('<div class="navrow"><span class="rlabel">功能簇（9）</span>')
    for fid, fname, rid, _ in GROUP_CLUSTERS:
        o.append(f'<a class="chip" href="#{fid}" style="border-color:{REGION_COLOR[rid]}">'
                 f'{fid} {esc(fname)}</a>')
    o.append('</div>')
    o.append('</div>')

    o.append('<div class="caliber">'
             '<b>口径说明（两个数字不可混用）：</b>'
             '<b>组内成员合计</b>＝把该区/簇下所有组的 plugins 列表长度相加（每个插件只归属一个组，故不重复）；'
             '<b>插件自身 source_layer</b>＝按每个插件自身的 source_layer 归属统计。'
             '前者描述「分组规模」，后者描述「插件装配来源」。</div>')

    # 三区 → 簇 → 组卡片
    for rid in ("L1", "L2", "L3"):
        rgroups = [g for _, _, r, gs in GROUP_CLUSTERS if r == rid for g in gs]
        rmember = sum(st[g]["n"] for g in rgroups)
        desc = REGION_DESC[rid]
        o.append(f'<h2 id="{rid}"><span class="dot" style="background:{REGION_COLOR[rid]}"></span>'
                 f'{esc(REGION_NAME[rid])}'
                 f'<span class="fcount">· {len(rgroups)} 组 / {rmember} 插件（组内成员合计）'
                 f'· {src_tot.get(rid, 0)} 插件（{esc(desc)}；按插件自身 source_layer 计数）</span></h2>')
        for fid, fname, fregion, gs in GROUP_CLUSTERS:
            if fregion != rid:
                continue
            fmember = sum(st[g]["n"] for g in gs)
            o.append(f'<h3 id="{fid}"><span class="fid">{fid}</span>{esc(fname)}'
                     f'<span class="fcount">· {len(gs)} 组 / {fmember} 插件（组内成员合计）</span></h3>')
            o.append('<div class="grid">')
            for g in gs:
                o.append(_group_card(st[g], gcolor[g], maxn))
            o.append('</div>')

    # 外部 seam 基座 (折叠; description 73/73 为空)
    seams = ext["seams"]
    empty_desc = sum(1 for s in seams if not (s.get("description") or "").strip())
    maxref = max(s.get("ref_count", 0) for s in seams) or 1
    seams_sorted = sorted(seams, key=lambda x: (-x.get("ref_count", 0), -x.get("ts_count", 0), x["id"]))
    tot_ts = sum(s.get("ts_count", 0) for s in seams)
    tot_ref = sum(s.get("ref_count", 0) for s in seams)
    o.append('<details class="fold" id="seams">')
    o.append(f'<summary><span class="dot" style="background:#b48a3c"></span>外部 seam 基座'
             f'<span class="fcount">· {len(seams)} 项 · 按被引用插件数降序 · '
             f'总 TS 文件 {tot_ts} · 总引用 {tot_ref} · 点击展开/折叠</span></summary>')
    o.append(f'<div class="note">说明字段（<code>description</code>）当前为空 {empty_desc}/{len(seams)}'
             f'（100%），此处展示等价字段：<b>包路径（path）</b>与<b>引用计数（ref_count）</b>，'
             f'不再渲染空分隔符。</div>')
    o.append('<div class="sgrid">')
    for i, s in enumerate(seams_sorted, 1):
        o.append(_seam_card(i, s, maxref))
    o.append('</div>')
    o.append('</details>')

    # 特殊模块 (真实文件名 glob; 说明取 assembly_summary)
    sm_files = sorted(os.path.basename(p) for p in _glob.glob(os.path.join(SPECIAL_OUT, "*.html")))
    sm_by_id = {m["id"]: m for m in special_modules}
    o.append(f'<h2 id="special"><span class="dot" style="background:#2fb98a"></span>特殊模块'
             f'<span class="fcount">· {len(sm_files)} 页 · 不进 DAG，独立成页</span></h2>')
    o.append('<div class="smgrid">')
    for fn in sm_files:
        sid = fn[:-5]
        m = sm_by_id.get(sid, {})
        summary = (m.get("assembly_summary") or "").strip()
        if len(summary) > 120:
            summary = summary[:120] + "…"
        desc2 = summary if summary else "（assembly_summary 缺失，仅列入口）"
        o.append(f'<div class="smcard"><a href="../08-special-modules/{fn}">{esc(sid)}</a>'
                 f'<p>{esc(desc2)}</p></div>')
    o.append('</div>')

    o.append('</main>')
    o.append(FOOTER)
    o.append('</body>')
    o.append('</html>')

    text = "\n".join(o)

    nopen = len(re.findall(r"<div\b", text))
    nclose = text.count("</div>")
    print(f"[CHECK] groups-index: <div>={nopen}  </div>={nclose} -> {'PASS' if nopen == nclose else 'FAIL'}")
    if "\ufffd" in text:
        raise SystemExit("[FAIL] groups-index 检出替换字符 U+FFFD")
    if nopen != nclose:
        raise SystemExit("[FAIL] groups-index div 开闭不平衡")

    emit(os.path.join(GROUPS, "index.html"), text)
    print("[GEN] groups/index.html (重设计: 区→簇→组卡片, 整卡可点击, seam 折叠)")


# =====================================================================
# 4. 特殊模块页 (08-special-modules)
# =====================================================================
def gen_special_pages():
    for sm in special_modules:
        sid = sm["id"]
        title = f'{sid} · 特殊模块'
        out = [page_header(title, '特殊模块（bundle/boot 层）', '<span class="badge">非 DAG 节点</span>')]
        out.append(treenav(None))
        out.append('<h2>模块说明</h2>')
        out.append(f'<table><tr><th>模块</th><td>{esc(sm["id"])}</td></tr><tr><th>类型</th><td>{esc(sm.get("kind",""))}</td></tr><tr><th>装配摘要</th><td>{esc(sm.get("assembly_summary",""))}</td></tr><tr><th>结构说明</th><td>{esc(sm.get("structure_notes",""))}</td></tr></table>')
        out.append('<h2>依赖的 L1/L2 插件</h2>')
        deps = sm.get("dependencies", [])
        if deps:
            out.append('<ul>')
            for d in deps:
                # 特殊模块页在 08-special-modules/, 插件页在 ../02-plugin-pages/
                if d in nodes:
                    out.append(f'<li><a href="../02-plugin-pages/{d}.html">{esc(d)}</a></li>')
                elif d in ext_map:
                    out.append(f'<li><a href="../02-plugin-pages/{d}.html" class="ext">{esc(d)}</a></li>')
                else:
                    out.append(f'<li>{esc(d)}</li>')
            out.append('</ul>')
        else:
            out.append('<p style="color:var(--dim);">无（独立）</p>')
        out.append(page_footer())
        emit(os.path.join(SPECIAL_OUT, f"{sid}.html"), "".join(out))
    print(f"[GEN] special module pages: {len(special_modules)}")


# =====================================================================
# 分阶段执行 (默认 dry-run, 零写盘)
# =====================================================================
if ONLY in ("all", "plugin-pages"):
    gen_plugin_pages()
if ONLY in ("all", "groups-pages"):
    gen_group_pages()
if ONLY in ("all", "groups-index"):
    gen_groups_index()
if ONLY in ("all", "special"):
    gen_special_pages()

flush()

print(f"[SUMMARY] --only {ONLY} | write={WRITE} | plugin nodes={len(nodes)}, ext={len(ext_map)}, "
      f"groups={len(groups)}, special={len(special_modules)}")
if WRITE and ONLY in ("all", "plugin-pages"):
    print("[REMINDER] 已重生成插件页 —— 必须补跑 `python3 gen-plugin-dyn.py` 重新注入动态 DAG 区块！")
