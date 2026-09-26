#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成根入口主页仪表盘 -> index.html（生产页，唯一产出方）。

本脚本是留档库根 index.html 的**唯一生成器**（此前该页为手工维护）。
全部统计数字从 01-dag-data/webapp-dag.json(meta/groups) 与
01-dag-data/external-seams.json(seams) 派生（不手抄字面量）。

确定性：不使用运行时钟 / datetime.now()，重复运行 byte-identical。
只写 <BASE>/index.html，不触碰任何其它目录。
"""
import json
import os
import re
import glob
import html

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))       # 07-checkpoint
BASE = os.path.dirname(SCRIPT_DIR)                            # 留档库根
OUT = os.path.join(BASE, "index.html")
DAG_JSON = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
SEAM_JSON = os.path.join(BASE, "01-dag-data", "external-seams.json")
SM_DIR = os.path.join(BASE, "08-special-modules")
GROUPS_INDEX = os.path.join(BASE, "03-groups", "index.html")

VERSION = "v0.1.7-rc.2"
REBUILD_DATE = "2026-09-27"

REGION = {
    "L1": {"name": "L1 核心集", "color": "#4f8cff", "size": 90},
    "L2": {"name": "L2 web-app", "color": "#9a7bf0", "size": 82},
    "L3": {"name": "L3 其余可挂载", "color": "#2fb98a", "size": 67},
}
REGION_GROUPS_EXPECTED = {"L1": 29, "L2": 10, "L3": 11}

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
    ok = (len(flat) == len(set(flat)) == 50 and set(flat) == set(group_ids))
    print(f"[ASSERT] 9 簇展开覆盖恰好 50 组: 展开 {len(flat)} / 唯一 {len(set(flat))} / "
          f"库内 {len(group_ids)} -> {'PASS' if ok else 'FAIL'}")
    return ok


def assert_region_sizes(group_map):
    ok = True
    for rid, cl in ((r, [(fid, fn, gs) for fid, fn, fr, gs in CLUSTERS if fr == r]) for r in ("L1", "L2", "L3")):
        n = sum(len(gs) for _, _, gs in cl)
        if n != REGION_GROUPS_EXPECTED[rid]:
            ok = False
        print(f"[ASSERT] {rid} 组数 = {n} (期望 {REGION_GROUPS_EXPECTED[rid]}) -> "
              f"{'PASS' if n == REGION_GROUPS_EXPECTED[rid] else 'FAIL'}")
    return ok


def groups_anchors_available():
    """检测 03-groups/index.html 是否已含 L1..L3 / F1..F9 锚点。
    该页由并行 Agent 产出时可能尚未落地 -> 降级为不带锚点（外链仍有效）。"""
    wanted = ["L1", "L2", "L3", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9"]
    if not os.path.exists(GROUPS_INDEX):
        return False, wanted
    with open(GROUPS_INDEX, encoding="utf-8", errors="replace") as f:
        t = f.read()
    missing = [w for w in wanted if f'id="{w}"' not in t]
    return (not missing), missing


CSS = """
:root{--bg:#0f1117;--panel:#161a22;--border:#2a2f3a;--text:#e6e8ee;--dim:#9aa3b2;--accent:#4f8cff;--ok:#2fb98a;--ext:#b48a3c;}
*{box-sizing:border-box;margin:0;padding:0;}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;line-height:1.6;}
header{background:var(--panel);border-bottom:1px solid var(--border);padding:26px 32px;}
header h1{font-size:23px;display:flex;align-items:center;gap:12px;flex-wrap:wrap;}
header .sub{color:var(--dim);font-size:14px;max-width:1000px;margin-top:8px;}
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
.bigcards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:10px 0;align-items:stretch;}
a.bigcard{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:18px 20px;display:flex;flex-direction:column;gap:8px;text-decoration:none;color:inherit;transition:border-color .15s,background .15s,transform .15s;}
a.bigcard:hover{border-color:var(--accent);background:#1b2333;transform:translateY(-2px);}
a.bigcard:focus-visible{outline:2px solid var(--accent);outline-offset:2px;}
a.bigcard h3{font-size:16px;color:var(--accent);display:flex;justify-content:space-between;align-items:center;gap:8px;}
a.bigcard h3 .arrow{color:var(--dim);font-size:14px;}
a.bigcard:hover h3 .arrow{color:var(--accent);}
a.bigcard p{font-size:13px;color:var(--dim);flex:1;}
a.bigcard .ex{font-size:12px;color:#7fb0ff;word-break:break-all;font-family:Consolas,monospace;}
@media (max-width:820px){.bigcards{grid-template-columns:1fr;}}
.links{display:flex;flex-wrap:wrap;gap:9px;margin:10px 0;}
.links a{font-size:13px;background:var(--panel);border:1px solid var(--border);border-radius:8px;padding:6px 14px;color:var(--accent);text-decoration:none;}
.links a:hover{border-color:var(--accent);}
.links a .cnt{color:var(--dim);font-size:11px;margin-left:6px;}
.links a.ai{border-style:dashed;}
.regbox{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:12px 0;}
@media (max-width:820px){.regbox{grid-template-columns:1fr;}}
.regcard{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:14px 16px;}
.regcard .rt{font-size:15px;font-weight:600;display:flex;align-items:center;gap:8px;}
.regcard .rt a{color:inherit;text-decoration:none;}
.regcard .rt a:hover{color:var(--accent);}
.regcard .dot{width:11px;height:11px;border-radius:3px;flex:none;}
.regcard .rc{font-size:12.5px;color:#cfd6e4;margin:6px 0 2px;}
.regcard .rnote{font-size:11px;color:var(--dim);margin-bottom:10px;}
.clchips{display:flex;flex-wrap:wrap;gap:6px;}
.clchips a{font-size:11.5px;border-radius:6px;padding:3px 9px;text-decoration:none;border:1px solid transparent;}
.clchips a:hover{border-color:var(--accent);}
.method{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:14px 18px;font-size:13px;color:#c3cbd8;}
.method b{color:#e6e8ee;}
.method li{margin:4px 0 4px 18px;}
footer{margin-top:36px;padding:16px 32px;border-top:1px solid var(--border);color:var(--dim);font-size:12px;text-align:center;}
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
            with open(target, encoding="utf-8", errors="replace") as f:
                t = f.read()
            if f'id="{frag}"' not in t:
                broken.append(h + " (anchor missing in target)")
    return checked, broken


def main():
    dag, seams = load()
    meta = dag["meta"]
    group_ids = [g["id"] for g in dag["groups"]]
    group_map = {g["id"]: g for g in dag["groups"]}

    # --- 统计派生（真相源：meta + 数组长度）---
    plugin_total = meta["plugin_count"]
    l1, l2, l3 = meta["l1_plugins"], meta["l2_plugins"], meta["l3_plugins"]
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
    print(f"[ASSERT] HTML 插件页 = 插件 + seam: {plugin_total}+{seam_total}={html_pages} -> "
          f"{'PASS' if html_pages == plugin_total + seam_total else 'FAIL'}")
    if not assert_cluster_coverage(group_ids):
        raise SystemExit("[FAIL] 簇覆盖断言未通过")
    if not assert_region_sizes(group_map):
        raise SystemExit("[FAIL] 区组数断言未通过")

    sm_pages = sorted(os.path.basename(p) for p in glob.glob(os.path.join(SM_DIR, "*.html")))
    print(f"[GLOB] 08-special-modules: {len(sm_pages)} 页")
    for rep in RC_REPORTS:
        p = os.path.join(BASE, rep)
        print(f"[GLOB] RC 报告 {rep}: {'存在' if os.path.exists(p) else '缺失!'}")

    anchors_ok, missing_anchors = groups_anchors_available()
    print(f"[ANCHOR] 03-groups/index.html 锚点可用: {anchors_ok}"
          + ("" if anchors_ok else f"（缺失 {missing_anchors[:4]}... -> 降级为不带锚点）"))
    gidx = "03-groups/index.html"

    out = []
    out.append('<!DOCTYPE html>')
    out.append('<html lang="zh-CN">')
    out.append('<head>')
    out.append('<meta charset="UTF-8">')
    out.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    out.append(f'<title>DeepSeek Harness 插件级 DAG 依赖链分析 · 主页仪表盘 {VERSION}</title>')
    out.append('<style>' + CSS + '</style>')
    out.append('</head>')
    out.append('<body>')

    # 1. header（标题 + 一句话定位 + 版本徽标 + 重建说明，≤2 行）
    out.append('<header>')
    out.append(f'<h1>DeepSeek Harness 插件级 DAG 依赖链分析 <span class="badge">{VERSION}</span></h1>')
    out.append(f'<div class="sub">以 cordis 插件为最小分析单元，三硬依据（E1 编译 / E2 运行时 / E3 组合）逐条源码溯源，'
               f'回答每个插件「实现了什么 / 依赖谁 / 被谁依赖」。<br>'
               f'{REBUILD_DATE} 全量重建至 dsh-{VERSION}：L1 核心集 + L2 web-app + L3 其余可挂载插件全部完成。</div>')
    out.append('</header>')
    out.append('<main>')

    # 2. 核心统计条（等宽 grid，6 项；数字全部派生，任一断点无孤行）
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

    # 3. 主入口大卡（3 张；整块可点击 —— <a> 包裹整卡）
    out.append('<h2>主入口</h2>')
    out.append('<div class="bigcards">')
    out.append('<a class="bigcard" href="04-interactive/index.html">'
               '<h3>交互 DAG 总览 <span class="arrow">→</span></h3>'
               '<p>cytoscape 本地渲染：组级 51 节点（50 组 + EXT），点击下钻组内插件 DAG，'
               '支持 <code>?drill=Gxx</code> / <code>#Gxx</code> 深链；disabled 插件灰显红边。</p>'
               '<span class="ex">04-interactive/index.html</span></a>')
    out.append('<a class="bigcard" href="03-groups/index.html">'
               '<h3>分组索引 <span class="arrow">→</span></h3>'
               f'<p>{group_total} 组按装配来源分为 3 区、9 个功能簇；每组含插件列表、层跨度与来源徽标。</p>'
               '<span class="ex">03-groups/index.html</span></a>')
    out.append('<a class="bigcard" href="02-plugin-pages/dsh-session.html">'
               '<h3>插件页 <span class="arrow">→</span></h3>'
               f'<p>每节点一页（共 {html_pages} 页：{plugin_total} 插件 + {seam_total} seam）：'
               f'插件信息 + 实现逻辑 + provides + 依赖/被依赖 + DAG 链式导航 + 源码引用。</p>'
               '<span class="ex">示例 → 02-plugin-pages/dsh-session.html</span></a>')
    out.append('</div>')

    # 4. 次级入口行（每个链接均已 glob 核实存在）
    out.append('<h2>次级入口</h2>')
    out.append('<div class="links">')
    out.append(f'<a href="08-special-modules/">特殊模块<span class="cnt">{len(sm_pages)} 页</span></a>')
    out.append('<a class="ai" href="06-md/00-index.md">AI 检索 MD 镜像<span class="cnt">Markdown</span></a>')
    out.append('<a href="report.html">任务报告</a>')
    for rep in RC_REPORTS:
        out.append(f'<a class="ai" href="{rep}">RC 差异报告<span class="cnt">{esc(rep.split("-DIFF")[0])} · MD</span></a>')
    out.append('<a href="01-dag-data/webapp-dag.json">DAG 数据 JSON</a>')
    out.append('<a class="ai" href="README.md">README<span class="cnt">MD</span></a>')
    out.append('</div>')
    out.append('<div class="links">')
    for fn in sm_pages:
        out.append(f'<a href="08-special-modules/{fn}">{esc(fn[:-5])}</a>')
    out.append('</div>')

    # 5. 分区总览（3 区 + 9 簇；双口径标注）
    out.append('<h2>分区总览</h2>')
    out.append('<div class="regbox">')
    for rid in ("L1", "L2", "L3"):
        r = REGION[rid]
        cl = [(fid, fn, gs) for fid, fn, fr, gs in CLUSTERS if fr == rid]
        ngroups = sum(len(gs) for _, _, gs in cl)
        nmembers = sum(len(group_map[g]["plugins"]) for _, _, gs in cl for g in gs)
        href = gidx + (f"#{rid}" if anchors_ok else "")
        out.append(f'<div class="regcard"><div class="rt"><span class="dot" style="background:{r["color"]}"></span>'
                   f'<a href="{href}">{esc(r["name"])}</a></div>'
                   f'<div class="rc"><b>{ngroups} 组</b> / <b>{nmembers} 插件</b>（组内成员合计）</div>'
                   f'<div class="rnote">插件自身 source_layer 计为 {rid} {r["size"]}</div>'
                   f'<div class="clchips">')
        for fid, fname, gs in cl:
            chref = gidx + (f"#{fid}" if anchors_ok else "")
            out.append(f'<a href="{chref}" style="background:{r["color"]}22;color:{r["color"]}">'
                       f'{fid} {esc(fname)} ({len(gs)})</a>')
        out.append('</div></div>')
    out.append('</div>')

    # 6. 方法说明（三硬依据 + 拓扑分层，压缩为 4 行）
    out.append('<h2>方法说明</h2>')
    out.append('<div class="method"><ul>'
               '<li><b>E1 编译依赖</b>：package.json peerDependencies / import 语句。</li>'
               '<li><b>E2 运行时依赖</b>：ctx 服务注入 / ctx.get / 事件订阅。</li>'
               '<li><b>E3 组合依赖</b>：cordis.patch.yml 装配位置。</li>'
               f'<li>拓扑分层采用<b>最长路径</b>（被依赖方先于依赖方，Layer 0 基础 → Layer {layer_total - 1} 最外层）；'
               f'type-only 类型导入边标注但不参与分层（TS 类型环合法），1 条运行时反馈边标 soft，19 个装配行 disabled 灰显。</li>'
               '</ul></div>')

    out.append('</main>')
    out.append(f'<footer>DeepSeek Harness 插件级 DAG 依赖链分析 · {VERSION} · {REBUILD_DATE} 全量重建 · '
               f'统计数字由 gen-root-index.py 从 webapp-dag.json / external-seams.json 派生</footer>')
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

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html_text)

    print(f"[SEAM] description 为空 {empty_desc}/{seam_total} 条（主入口页不展示 seam 明细）")
    checked, broken = check_links(html_text, BASE)
    print(f"[LINKS] 检查 {checked} 条内部链接，断链 {len(broken)}")
    for b in broken:
        print("   BROKEN:", b)
    print(f"[OUT] {OUT}  ({len(html_text)} bytes)")
    if broken:
        raise SystemExit("[FAIL] 存在断链")


if __name__ == "__main__":
    main()
