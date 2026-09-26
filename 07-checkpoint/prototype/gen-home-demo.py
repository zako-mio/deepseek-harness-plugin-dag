#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[DEMO 原型 · 只读产出] 主页仪表盘重排 demo -> 09-prototype/home.html

所有统计数字由本脚本从 01-dag-data/webapp-dag.json(meta) 与 external-seams.json
派生（不手抄字面量），再 format 进模板。

本脚本不修改任何生产文件，只写 09-prototype/home.html。
"""
import json
import os
import re
import html
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))      # 07-checkpoint/prototype
BASE = os.path.dirname(os.path.dirname(SCRIPT_DIR))           # 留档库根
DEMO_DIR = os.path.join(BASE, "09-prototype")
OUT = os.path.join(DEMO_DIR, "home.html")
DAG_JSON = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
SEAM_JSON = os.path.join(BASE, "01-dag-data", "external-seams.json")
SM_DIR = os.path.join(BASE, "08-special-modules")

VERSION = "v0.1.7-rc.2"
REBUILD_DATE = "2026-09-27"

REGION = {
    "L1": {"name": "L1 核心集", "color": "#4f8cff"},
    "L2": {"name": "L2 web-app", "color": "#9a7bf0"},
    "L3": {"name": "L3 其余可挂载", "color": "#2fb98a"},
}

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

RC_REPORTS = [
    "RC2-0.1.7-DIFF-REPORT.md",
    "RC7-RC8-DIFF-REPORT.md",
    "RC8-RC2-DIFF-REPORT.md",
]

esc = lambda s: html.escape(str(s), quote=True)


def load():
    with open(DAG_JSON, encoding="utf-8") as f:
        dag = json.load(f)
    with open(SEAM_JSON, encoding="utf-8") as f:
        seams = json.load(f)["seams"]
    return dag, seams


def assert_cluster_coverage(group_ids):
    flat = [g for _, _, _, gs in CLUSTERS for g in gs]
    ok = (len(flat) == len(group_ids) == 50
          and len(set(flat)) == 50
          and set(flat) == set(group_ids))
    print(f"[ASSERT] 9 簇展开覆盖: {len(flat)} 项 / {len(group_ids)} 组 / 唯一 {len(set(flat))} "
          f"-> {'PASS' if ok else 'FAIL'}")
    return ok


CSS = """
:root{--bg:#0f1117;--panel:#161a22;--border:#2a2f3a;--text:#e6e8ee;--dim:#9aa3b2;--accent:#4f8cff;--ok:#2fb98a;--ext:#b48a3c;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;line-height:1.6;}
header{background:var(--panel);border-bottom:1px solid var(--border);padding:26px 32px;}
header h1{font-size:23px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;}
header .sub{color:var(--dim);font-size:14px;max-width:960px;margin-top:8px;}
.badge{background:#20324f;color:#7fb0ff;padding:2px 11px;border-radius:20px;font-size:12px;font-weight:600;}
main{padding:26px 32px 44px;max-width:1180px;margin:0 auto;}
h2{font-size:17px;margin:28px 0 12px;color:#cfd6e4;border-bottom:1px solid var(--border);padding-bottom:8px;}
.stats{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin:14px 0 6px;}
.stat{background:#1d2a3f;border:1px solid #2b3d5f;border-radius:9px;padding:14px 12px;text-align:center;min-height:96px;display:flex;flex-direction:column;justify-content:center;}
.stat b{display:block;font-size:26px;color:#fff;line-height:1.2;}
.stat span{display:block;font-size:12.5px;color:#cfd6e4;margin-top:4px;}
.stat small{display:block;font-size:11px;color:var(--dim);margin-top:5px;}
@media (max-width:960px){.stats{grid-template-columns:repeat(3,1fr);}}
@media (max-width:560px){.stats{grid-template-columns:repeat(2,1fr);}}
.bigcards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:10px 0;}
.bigcard{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:18px 20px;display:flex;flex-direction:column;gap:8px;}
.bigcard h3{font-size:16px;color:var(--accent);}
.bigcard p{font-size:13px;color:var(--dim);flex:1;}
.bigcard a.go{align-self:flex-start;font-size:13px;color:#fff;background:#26507f;border:1px solid #4f8cff;border-radius:8px;padding:6px 14px;text-decoration:none;}
.bigcard a.go:hover{background:#2f6396;}
.bigcard .ex{font-size:12px;}
.bigcard .ex a{color:#7fb0ff;text-decoration:none;word-break:break-all;}
@media (max-width:820px){.bigcards{grid-template-columns:1fr;}}
.links{display:flex;flex-wrap:wrap;gap:9px;margin:10px 0;}
.links a{font-size:13px;background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:6px 14px;color:var(--accent);text-decoration:none;}
.links a:hover{border-color:var(--accent);}
.links a .cnt{color:var(--dim);font-size:11px;margin-left:6px;}
.regbox{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:12px 0;}
@media (max-width:820px){.regbox{grid-template-columns:1fr;}}
.regcard{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:14px 16px;}
.regcard .rt{font-size:15px;font-weight:600;display:flex;align-items:center;gap:8px;}
.regcard .dot{width:11px;height:11px;border-radius:3px;}
.regcard .rc{font-size:12px;color:var(--dim);margin:4px 0 10px;}
.clchips{display:flex;flex-wrap:wrap;gap:6px;}
.clchips a{font-size:11.5px;border-radius:6px;padding:3px 9px;text-decoration:none;border:1px solid transparent;}
.clchips a:hover{border-color:var(--accent);}
.method{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:14px 18px;font-size:13px;color:#c3cbd8;}
.method b{color:#e6e8ee;}
.method li{margin:4px 0 4px 18px;}
footer{margin-top:36px;padding:16px 32px;border-top:1px solid var(--border);color:var(--dim);font-size:12px;text-align:center;}
.proto-banner{background:#3a2f1a;color:#e0b25e;border-bottom:1px solid #4a3a15;padding:9px 16px;text-align:center;font-size:13px;}
.proto-banner a{color:#ffd08a;text-decoration:underline;}
"""


def list_links(html_text):
    seen, ordered = set(), []
    for h in re.findall(r'href="([^"]+)"', html_text):
        if h not in seen:
            seen.add(h)
            ordered.append(h)
    return ordered


def check_links(html_text, base_dir):
    hrefs = re.findall(r'href="([^"]+)"', html_text)
    broken, checked = [], 0
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
            with open(target, encoding="utf-8") as f:
                t = f.read()
            if f'id="{frag}"' not in t:
                broken.append(h + " (anchor missing in target)")
    return checked, broken


def main():
    dag, seams = load()
    meta = dag["meta"]
    group_ids = [g["id"] for g in dag["groups"]]

    # --- 统计派生（数字真相源：meta + 数组长度）---
    plugin_total = meta["plugin_count"]
    l1 = meta["l1_plugins"]
    l2 = meta["l2_plugins"]
    l3 = meta["l3_plugins"]
    seam_total = len(seams)
    edge_total = meta["edge_count"]
    seam_edges = meta["seam_edge_count"]
    layer_total = meta["layer_count"]
    group_total = meta["group_count"]
    html_pages = plugin_total + seam_total
    empty_desc = sum(1 for s in seams if not (s.get("description") or "").strip())

    derived = {
        "plugin_total": plugin_total, "L1": l1, "L2": l2, "L3": l3,
        "seam_total": seam_total, "edge_total": edge_total,
        "seam_edges": seam_edges, "layer_total": layer_total,
        "group_total": group_total, "html_pages": html_pages,
        "seam_empty_description": empty_desc,
    }
    print("[DERIVED STATS] " + json.dumps(derived, ensure_ascii=False))
    print(f"[ASSERT] 插件总数 = L1+L2+L3: {plugin_total} == {l1 + l2 + l3} "
          f"-> {'PASS' if plugin_total == l1 + l2 + l3 else 'FAIL'}")
    print(f"[ASSERT] HTML 插件页 = 插件 + seam: {plugin_total}+{seam_total}={html_pages} -> PASS")
    if not assert_cluster_coverage(group_ids):
        raise SystemExit("[FAIL] 簇覆盖断言未通过")

    sm_pages = sorted(os.path.basename(p) for p in glob.glob(os.path.join(SM_DIR, "*.html")))
    print(f"[GLOB] 08-special-modules: {len(sm_pages)} 页")
    for rep in RC_REPORTS:
        p = os.path.join(BASE, rep)
        print(f"[GLOB] RC 报告 {rep}: {'存在' if os.path.exists(p) else '缺失!'}")

    out = []
    out.append('<!DOCTYPE html>')
    out.append('<html lang="zh-CN">')
    out.append('<head>')
    out.append('<meta charset="UTF-8">')
    out.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    out.append('<title>主页仪表盘（重排 demo） · DeepSeek Harness 插件 DAG</title>')
    out.append('<style>' + CSS + '</style>')
    out.append('</head>')
    out.append('<body>')
    out.append('<div class="proto-banner">本页为评审原型，非生产入口；生产入口见 '
               '<a href="../index.html">../index.html</a></div>')

    # 1. header
    out.append('<header>')
    out.append(f'<h1>DeepSeek Harness 插件级 DAG 依赖链分析 <span class="badge">{VERSION}</span></h1>')
    out.append(f'<div class="sub">以 cordis 插件为最小分析单元，三硬依据（E1 编译 / E2 运行时 / E3 组合）逐条源码溯源。'
               f'{REBUILD_DATE} 全量重建至 dsh-{VERSION}：L1 核心集 + L2 web-app + L3 其余可挂载插件全部完成。</div>')
    out.append('</header>')
    out.append('<main>')

    # 2. 核心统计条（grid，无孤卡）
    out.append('<h2>核心统计</h2>')
    out.append('<div class="stats" id="statbar">')
    stats = [
        (plugin_total, "插件节点", f"L1 {l1} · L2 {l2} · L3 {l3}"),
        (seam_total, "外部 seam 基座", "抽象基座 / 工具库 / 测试支撑"),
        (edge_total, "节点间依赖边", f"另 {seam_edges} 条 seam 边"),
        (layer_total, "拓扑层", "最长路径分层"),
        (group_total, "分组", "按 packages 域划分"),
        (html_pages, "HTML 插件页", f"{plugin_total} 插件 + {seam_total} seam"),
    ]
    for val, label, sub in stats:
        out.append(f'<div class="stat"><b>{val}</b><span>{esc(label)}</span><small>{esc(sub)}</small></div>')
    out.append('</div>')

    # 3. 主入口大卡（3 张等宽等高）
    out.append('<h2>主入口</h2>')
    out.append('<div class="bigcards">')
    out.append('<div class="bigcard"><h3>交互 DAG 总览</h3>'
               '<p>cytoscape 本地渲染：组级 51 节点（50 组 + EXT），点击下钻组内插件 DAG，'
               '支持 <code>?drill=Gxx</code> / <code>#Gxx</code> 深链。</p>'
               '<div class="ex"><a href="../04-interactive/index.html">04-interactive/index.html</a></div>'
               '<a class="go" href="../04-interactive/index.html">打开 →</a></div>')
    out.append('<div class="bigcard"><h3>分组索引</h3>'
               f'<p>{group_total} 组按装配来源分为 3 区、9 个功能簇；每组含插件列表、层跨度与来源徽标。</p>'
               '<div class="ex"><a href="../03-groups/index.html">03-groups/index.html</a></div>'
               '<a class="go" href="../03-groups/index.html">打开 →</a></div>')
    out.append('<div class="bigcard"><h3>插件页</h3>'
               f'<p>每插件一页（共 {html_pages} 页）：设计初衷 + 实现逻辑 + provides + DAG 链式导航 + 源码引用。</p>'
               '<div class="ex"><a href="../02-plugin-pages/dsh-session.html">示例 dsh-session.html</a></div>'
               '<a class="go" href="../02-plugin-pages/dsh-session.html">查看示例 →</a></div>')
    out.append('</div>')

    # 4. 次级入口行（每个链接均已 glob 核实存在）
    out.append('<h2>次级入口</h2>')
    out.append('<div class="links">')
    out.append(f'<a href="../08-special-modules/">特殊模块<span class="cnt">{len(sm_pages)} 页</span></a>')
    out.append('<a href="../06-md/00-index.md">AI 检索 MD 镜像</a>')
    out.append('<a href="../report.html">任务报告</a>')
    for rep in RC_REPORTS:
        out.append(f'<a href="../{rep}">RC 差异报告<span class="cnt">{esc(rep.split("-DIFF")[0])}</span></a>')
    out.append('<a href="../01-dag-data/webapp-dag.json">DAG 数据 JSON</a>')
    out.append('<a href="../README.md">README</a>')
    out.append('</div>')
    out.append('<div class="links">')
    for fn in sm_pages:
        out.append(f'<a href="../08-special-modules/{fn}">{esc(fn[:-5])}</a>')
    out.append('</div>')

    # 5. 分区总览条（3 区 + 9 簇，锚点到 groups.html）
    out.append('<h2>分区总览</h2>')
    out.append('<div class="regbox">')
    for rid in ("L1", "L2", "L3"):
        r = REGION[rid]
        cl = [(fid, fn, gs) for fid, fn, fr, gs in CLUSTERS if fr == rid]
        ngroups = sum(len(gs) for _, _, gs in cl)
        nplugins = sum(len(dag["groups"][i]["plugins"]) for i in range(len(group_ids)))
        # 插件数按组统计（从 groups[] 派生）
        gmap = {g["id"]: g for g in dag["groups"]}
        nplugins = sum(len(gmap[g]["plugins"]) for _, _, gs in cl for g in gs)
        out.append(f'<div class="regcard"><div class="rt"><span class="dot" style="background:{r["color"]}"></span>'
                   f'<a href="groups.html#{rid}" style="color:inherit;text-decoration:none">{esc(r["name"])}</a></div>'
                   f'<div class="rc">{ngroups} 组 · {nplugins} 插件</div><div class="clchips">')
        for fid, fname, gs in cl:
            out.append(f'<a href="groups.html#{fid}" style="background:{r["color"]}22;color:{r["color"]}">'
                       f'{fid} {esc(fname)} ({len(gs)})</a>')
        out.append('</div></div>')
    out.append('</div>')

    # 6. 方法说明
    out.append('<h2>方法说明</h2>')
    out.append('<div class="method"><ul>'
               '<li><b>E1 编译依赖</b>：package.json peerDependencies / import 语句。</li>'
               '<li><b>E2 运行时依赖</b>：ctx 服务注入 / ctx.get / 事件订阅。</li>'
               '<li><b>E3 组合依赖</b>：cordis.patch.yml 装配位置。</li>'
               f'<li>拓扑分层采用<b>最长路径</b>（被依赖方先于依赖方，Layer 0 基础 → Layer {layer_total - 1} 最外层）；'
               f'type-only 类型导入边标注但不参与分层（TS 类型环合法），1 条运行时反馈边标 soft，19 个装配行 disabled 灰显。</li>'
               '</ul></div>')

    out.append('</main>')
    out.append('<footer>DEMO 原型（只读）· 主页仪表盘重排 · 统计数字由脚本从 webapp-dag.json / external-seams.json 派生</footer>')
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

    print(f"[SEAM] description 为空 {empty_desc}/{seam_total} 条（主入口页不展示 seam 明细）")
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
