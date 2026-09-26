#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[DEMO 原型 · 只读产出] 分组索引重设计 demo -> 09-prototype/groups.html

数据源（全部只读）:
  01-dag-data/webapp-dag.json   -> groups[] / nodes[]（layer/source_layer/group）
  01-dag-data/external-seams.json -> seams[]（73 条，description 全空）
  08-special-modules/*.html     -> 特殊模块入口（glob 实际文件名）
  07-checkpoint/v017/special-modules.json -> assembly_summary

本脚本不修改任何生产文件，只写 09-prototype/groups.html。
"""
import json
import os
import re
import html
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))      # 07-checkpoint/prototype
BASE = os.path.dirname(os.path.dirname(SCRIPT_DIR))           # 留档库根
DEMO_DIR = os.path.join(BASE, "09-prototype")
OUT = os.path.join(DEMO_DIR, "groups.html")
DAG_JSON = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
SEAM_JSON = os.path.join(BASE, "01-dag-data", "external-seams.json")
SM_JSON = os.path.join(BASE, "07-checkpoint", "v017", "special-modules.json")
SM_DIR = os.path.join(BASE, "08-special-modules")

PALETTE = ["#4f8cff", "#7b61ff", "#2fb98a", "#e8933b", "#e05563", "#3b9fe0", "#9a7bf0", "#e0a03b",
           "#3bc4a0", "#d0546b", "#6c8df5", "#b48a3c", "#54a0e8", "#8a5cf0", "#3ab7c4", "#e07b54",
           "#5f8de0", "#9b6bd4", "#4aa8a0", "#d06a4a", "#6b9bd4", "#b07bd4", "#4ac48e", "#d48a5b"]

REGION = {
    "L1": {"name": "L1 核心集", "color": "#4f8cff", "desc": "bundle/base 装配的 90 个核心插件"},
    "L2": {"name": "L2 web-app", "color": "#9a7bf0", "desc": "bundle/web-app 装配的 82 个插件（含客户端 UI）"},
    "L3": {"name": "L3 其余可挂载", "color": "#2fb98a", "desc": "5 个 bundle 之外、独立可挂载的 67 个插件"},
}

# 固定二级功能簇表（主 Agent 裁定，禁改）
CLUSTERS = [
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

esc = lambda s: html.escape(str(s), quote=True)


def load_data():
    with open(DAG_JSON, encoding="utf-8") as f:
        dag = json.load(f)
    with open(SEAM_JSON, encoding="utf-8") as f:
        seams = json.load(f)["seams"]
    sm_by_id = {}
    if os.path.exists(SM_JSON):
        with open(SM_JSON, encoding="utf-8") as f:
            for m in json.load(f).get("special_modules", []):
                sm_by_id[m["id"]] = m
    return dag, seams, sm_by_id


def build_group_stats(dag):
    nodes = dag["nodes"]
    by_group = {}
    for n in nodes:
        by_group.setdefault(n["group"], []).append(n)
    order = {"L1": 0, "L2": 1, "L3": 2}
    stats = {}
    for g in dag["groups"]:
        gid = g["id"]
        ns = by_group.get(gid, [])
        cnt = {}
        for n in ns:
            cnt[n["source_layer"]] = cnt.get(n["source_layer"], 0) + 1
        layers = [n["layer"] for n in ns]
        top = max(cnt.values()) if cnt else 0
        maj = min([k for k, v in cnt.items() if v == top], key=lambda x: order[x]) if cnt else "?"
        stats[gid] = {
            "id": gid, "name": g["name"], "plugins": g["plugins"],
            "n": len(ns), "src": cnt, "maj": maj,
            "lmin": min(layers) if layers else None,
            "lmax": max(layers) if layers else None,
        }
    return stats


def assert_cluster_coverage(group_ids):
    flat = []
    for _, _, _, gs in CLUSTERS:
        flat.extend(gs)
    dup = sorted({g for g in flat if flat.count(g) > 1})
    missing = sorted(set(group_ids) - set(flat))
    extra = sorted(set(flat) - set(group_ids))
    ok = (len(flat) == len(group_ids) == 50 and not dup and not missing and not extra)
    print(f"[ASSERT] 9 簇展开覆盖: 展开 {len(flat)} / 实际组 {len(group_ids)} / 重复 {dup} / 遗漏 {missing} / 越界 {extra} -> {'PASS' if ok else 'FAIL'}")
    return ok


def src_badge(src):
    keys = [k for k in ("L1", "L2", "L3") if src.get(k)]
    if len(keys) == 1:
        return f"纯 {keys[0]}", "pure"
    return "混合 " + "+".join(keys), "mix"


def card_html(st, gcolor, maxn):
    badge, bcls = src_badge(st["src"])
    size_cls = "big" if st["n"] >= 20 else ("mid" if st["n"] >= 8 else "small")
    bar = max(6, round(100 * st["n"] / maxn))
    span = f'{st["lmin"]} – {st["lmax"]}'
    return (
        f'<div class="gcard {size_cls}" style="border-left-color:{gcolor}">'
        f'<div class="ghead"><span class="swatch" style="background:{gcolor}"></span>'
        f'<span class="gid">{st["id"]}</span>'
        f'<a class="gname" href="../03-groups/{st["id"]}.html">{esc(st["name"])}</a></div>'
        f'<div class="gmeta"><span class="tag n">{st["n"]} 插件</span>'
        f'<span class="tag">层 {span}</span>'
        f'<span class="tag {bcls}">{esc(badge)}</span></div>'
        f'<div class="gbar"><i style="width:{bar}%;background:{gcolor}"></i></div>'
        f'</div>'
    )


def seam_card_html(rank, s, maxref):
    ref = s.get("ref_count", 0)
    bar = max(2, round(100 * ref / maxref))
    return (
        f'<div class="scard">'
        f'<div class="shead"><span class="rank">#{rank}</span>'
        f'<a href="../02-plugin-pages/{s["id"]}.html">{esc(s["id"])}</a></div>'
        f'<div class="spath">{esc(s.get("path") or "—")}</div>'
        f'<div class="smeta"><span>{s.get("ts_count", 0)} TS 文件</span><span>被 {ref} 个插件引用</span></div>'
        f'<div class="sbar"><i style="width:{bar}%"></i></div>'
        f'</div>'
    )


CSS = """
:root{--bg:#0f1117;--panel:#161a22;--panel2:#1b202a;--border:#2a2f3a;--text:#e6e8ee;--dim:#9aa3b2;--accent:#4f8cff;--ok:#2fb98a;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;line-height:1.6;}
header{background:var(--panel);border-bottom:1px solid var(--border);padding:16px 28px;}
header .crumb{color:var(--dim);font-size:13px;}
header .crumb a{color:var(--accent);text-decoration:none;}
header .crumb a:hover{text-decoration:underline;}
header h1{font-size:19px;margin-top:6px;}
header .sub{color:var(--dim);font-size:13px;margin-top:4px;}
main{padding:22px 28px 40px;max-width:1180px;margin:0 auto;}
h2{font-size:17px;margin:26px 0 6px;color:#cfd6e4;padding-bottom:7px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;flex-wrap:wrap;}
h2 .dot{width:10px;height:10px;border-radius:3px;display:inline-block;}
h3{font-size:14px;margin:18px 0 8px;color:#b8c2d4;display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
h3 .fid{background:#20324f;color:#7fb0ff;border-radius:5px;padding:1px 8px;font-size:12px;}
h3 .fcount{color:var(--dim);font-size:12px;font-weight:400;}
.navbox{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:12px 16px;margin:14px 0;}
.navrow{display:flex;flex-wrap:wrap;align-items:center;gap:8px;padding:5px 0;}
.navrow .rlabel{font-size:13px;font-weight:600;min-width:104px;color:#cfd6e4;}
.navrow a.chip{font-size:12px;background:#1d2a3f;border:1px solid #2b3d5f;border-radius:20px;padding:2px 10px;color:#9fc0ff;text-decoration:none;}
.navrow a.chip:hover{background:#2b3d5f;color:#fff;}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin:10px 0 6px;}
.gcard{background:var(--panel);border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:9px;padding:11px 13px;}
.gcard.small .gname{font-size:14px;}
.gcard.mid{padding:13px 15px;}
.gcard.mid .gname{font-size:16px;}
.gcard.big{padding:16px 18px;background:linear-gradient(180deg,#1b2330,#161a22);}
.gcard.big .gname{font-size:19px;font-weight:600;}
.ghead{display:flex;align-items:center;gap:7px;flex-wrap:wrap;}
.swatch{width:12px;height:12px;border-radius:3px;flex:0 0 auto;}
.gid{font-family:Consolas,monospace;font-size:12px;color:var(--dim);}
.gname{color:var(--accent);text-decoration:none;}
.gname:hover{text-decoration:underline;}
.gmeta{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 8px;}
.tag{font-size:11px;background:#1d2a3f;color:#8fa8c8;border-radius:5px;padding:1px 7px;}
.tag.n{background:#20324f;color:#7fb0ff;}
.tag.pure{background:#1d2a24;color:#5fc9a0;}
.tag.mix{background:#3a2f1a;color:#e0b25e;}
.gbar,.sbar{height:5px;background:#0d1117;border-radius:3px;overflow:hidden;}
.gbar i,.sbar i{display:block;height:100%;border-radius:3px;}
.sgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;margin:12px 0;}
.scard{background:var(--panel);border:1px solid var(--border);border-radius:9px;padding:10px 12px;}
.shead{display:flex;align-items:center;gap:7px;}
.shead .rank{font-size:11px;color:var(--dim);font-family:Consolas,monospace;}
.shead a{color:#e0b25e;text-decoration:none;font-size:13px;word-break:break-all;}
.shead a:hover{text-decoration:underline;}
.spath{font-family:Consolas,monospace;font-size:11px;color:var(--dim);margin:5px 0;word-break:break-all;}
.smeta{display:flex;gap:10px;font-size:11px;color:#8fa8c8;margin-bottom:7px;}
.sbar i{background:#b48a3c;}
.note{background:#0d1a14;border:1px solid #2f5a4a;border-radius:8px;padding:9px 13px;font-size:12.5px;color:#a7cbbd;margin:10px 0;}
.smgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px;margin:10px 0;}
.smcard{background:var(--panel);border:1px solid var(--border);border-radius:9px;padding:11px 13px;}
.smcard a{color:var(--accent);text-decoration:none;font-size:13.5px;font-weight:600;}
.smcard a:hover{text-decoration:underline;}
.smcard p{font-size:12px;color:var(--dim);margin-top:5px;}
footer{margin-top:36px;padding:16px 28px;border-top:1px solid var(--border);color:var(--dim);font-size:12px;text-align:center;}
.proto-banner{background:#3a2f1a;color:#e0b25e;border-bottom:1px solid #4a3a15;padding:9px 16px;text-align:center;font-size:13px;}
.proto-banner a{color:#ffd08a;text-decoration:underline;}
"""


def list_links(html_text):
    hrefs = re.findall(r'href="([^"]+)"', html_text)
    seen, ordered = set(), []
    for h in hrefs:
        if h in seen:
            continue
        seen.add(h)
        ordered.append(h)
    return ordered


def check_links(html_text, base_dir):
    hrefs = re.findall(r'href="([^"]+)"', html_text)
    broken = []
    checked = 0
    for h in hrefs:
        if h.startswith(("http://", "https://", "mailto:", "javascript:")):
            continue
        checked += 1
        path, _, frag = h.partition("#")
        if path == "":
            if frag and f'id="{frag}"' not in html_text:
                broken.append(h + " (missing anchor in self)")
            continue
        target = os.path.normpath(os.path.join(base_dir, path))
        if not os.path.exists(target):
            broken.append(h + " (file missing)")
            continue
        if frag and target.endswith(".html") and os.path.isfile(target):
            try:
                with open(target, encoding="utf-8") as f:
                    t = f.read()
                if f'id="{frag}"' not in t:
                    broken.append(h + " (anchor missing in target)")
            except Exception as e:  # noqa
                broken.append(h + f" (read error {e})")
    return checked, broken


def main():
    dag, seams, sm_by_id = load_data()
    group_ids = [g["id"] for g in dag["groups"]]
    print(f"[DATA] groups={len(group_ids)} nodes={len(dag['nodes'])} seams={len(seams)}")
    if not assert_cluster_coverage(group_ids):
        raise SystemExit("[FAIL] 簇覆盖断言未通过")

    st = build_group_stats(dag)
    gids_sorted = sorted(st.keys())
    gcolor = {gid: PALETTE[i % len(PALETTE)] for i, gid in enumerate(gids_sorted)}
    maxn = max(v["n"] for v in st.values())

    out = []
    out.append('<!DOCTYPE html>')
    out.append('<html lang="zh-CN">')
    out.append('<head>')
    out.append('<meta charset="UTF-8">')
    out.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    out.append('<title>分组索引（重设计 demo） · DeepSeek Harness 插件 DAG</title>')
    out.append('<style>' + CSS + '</style>')
    out.append('</head>')
    out.append('<body>')
    out.append('<div class="proto-banner">本页为评审原型，非生产入口；生产入口见 '
               '<a href="../index.html">../index.html</a></div>')
    out.append('<header>')
    out.append('<div class="crumb"><a href="../04-interactive/index.html">DAG 总览</a> / <span>分组索引</span></div>')
    out.append('<h1>分组索引 · 按区 + 功能簇重排</h1>')
    out.append(f'<div class="sub">50 组按装配来源（L1/L2/L3）分为 3 区、9 个功能簇；组内多数 source_layer 决定归区。'
               f'组配色与生产页一致。</div>')
    out.append('</header>')
    out.append('<main>')

    # 顶部快速锚点导航（按区/簇分组，替代 chip 墙）
    out.append('<div class="navbox">')
    for rid in ("L1", "L2", "L3"):
        chips = []
        for fid, fname, fregion, _ in CLUSTERS:
            if fregion == rid:
                chips.append(f'<a class="chip" href="#{fid}">{fid} {esc(fname)}</a>')
        out.append('<div class="navrow">')
        out.append(f'<span class="rlabel" style="color:{REGION[rid]["color"]}">'
                   f'<a href="#{rid}" style="color:inherit;text-decoration:none">{esc(REGION[rid]["name"])}</a></span>')
        out.append("".join(chips))
        out.append('</div>')
    out.append('</div>')

    # 三个区
    for rid in ("L1", "L2", "L3"):
        r = REGION[rid]
        rgroups = [g for fid, fn, fr, gs in CLUSTERS if fr == rid for g in gs]
        rplugins = sum(len(st[g]["plugins"]) for g in rgroups)
        out.append(f'<h2 id="{rid}"><span class="dot" style="background:{r["color"]}"></span>'
                   f'{esc(r["name"])}'
                   f'<span class="fcount" style="font-size:12px;color:var(--dim);font-weight:400">'
                   f'· {len(rgroups)} 组 / {rplugins} 插件 · {esc(r["desc"])}</span></h2>')
        for fid, fname, fregion, gs in CLUSTERS:
            if fregion != rid:
                continue
            fp = sum(len(st[g]["plugins"]) for g in gs)
            out.append(f'<h3 id="{fid}"><span class="fid">{fid}</span>{esc(fname)}'
                       f'<span class="fcount">{len(gs)} 组 / {fp} 插件</span></h3>')
            out.append('<div class="grid">')
            for g in gs:
                out.append(card_html(st[g], gcolor[g], maxn))
            out.append('</div>')

    # 外部 seam 基座
    empty_desc = sum(1 for s in seams if not (s.get("description") or "").strip())
    maxref = max(s.get("ref_count", 0) for s in seams) or 1
    seams_sorted = sorted(seams, key=lambda x: (-x.get("ref_count", 0), -x.get("ts_count", 0), x["id"]))
    out.append(f'<h2 id="seams"><span class="dot" style="background:#b48a3c"></span>外部 seam 基座'
               f'<span style="font-size:12px;color:var(--dim);font-weight:400">· {len(seams)} 项 · 按被引用插件数降序</span></h2>')
    out.append(f'<div class="note">说明字段（<code>description</code>）当前为空 {empty_desc}/{len(seams)}，'
               f'此处展示等价的<b>包路径</b>与<b>引用计数</b>，不再渲染空分隔符。'
               f'总 TS 文件 {sum(s.get("ts_count", 0) for s in seams)} · 总引用 {sum(s.get("ref_count", 0) for s in seams)}。</div>')
    out.append('<div class="sgrid">')
    for i, s in enumerate(seams_sorted, 1):
        out.append(seam_card_html(i, s, maxref))
    out.append('</div>')

    # 特殊模块
    sm_files = sorted(os.path.basename(p) for p in glob.glob(os.path.join(SM_DIR, "*.html")))
    out.append(f'<h2 id="special"><span class="dot" style="background:#2fb98a"></span>特殊模块'
               f'<span style="font-size:12px;color:var(--dim);font-weight:400">· {len(sm_files)} 页 · 不进 DAG，独立成页</span></h2>')
    out.append('<div class="smgrid">')
    for fn in sm_files:
        sid = fn[:-5]
        m = sm_by_id.get(sid, {})
        summary = (m.get("assembly_summary") or "").strip()
        if len(summary) > 120:
            summary = summary[:120] + "…"
        desc = summary if summary else "（assembly_summary 缺失，仅列入口）"
        out.append(f'<div class="smcard"><a href="../08-special-modules/{fn}">{esc(sid)}</a>'
                   f'<p>{esc(desc)}</p></div>')
    out.append('</div>')

    out.append('</main>')
    out.append('<footer>DEMO 原型（只读）· 分组索引重设计 · 数据派生自 webapp-dag.json + external-seams.json</footer>')
    out.append('</body>')
    out.append('</html>')

    html_text = "\n".join(out)

    nopen = len(re.findall(r"<div\b", html_text))
    nclose = html_text.count("</div>")
    print(f"[CHECK] <div>={nopen}  </div>={nclose}  -> {'PASS' if nopen == nclose else 'FAIL'}")
    if "\ufffd" in html_text:
        raise SystemExit("[FAIL] 检出替换字符 U+FFFD")
    if nopen != nclose:
        raise SystemExit("[FAIL] div 开闭不平衡")

    os.makedirs(DEMO_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html_text)

    print(f"[SEAM] description 为空 {empty_desc}/{len(seams)} 条（页面以 path / ref_count 等价展示）")
    checked, broken = check_links(html_text, DEMO_DIR)
    print(f"[LINKS] 检查 {checked} 条内部链接，断链 {len(broken)}")
    print("[LINKS] 唯一内部链接清单:")
    for h in list_links(html_text):
        print("   -", h)
    for b in broken:
        print("   BROKEN:", b)
    print(f"[OUT] {OUT}  ({len(html_text)} bytes)")
    if broken:
        raise SystemExit("[FAIL] 存在断链")


if __name__ == "__main__":
    main()
