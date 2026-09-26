#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S4b 交互总览页生成: 04-interactive/index.html

本脚本是 04-interactive/index.html 的唯一权威生成器（determinism: 同输入 → 同字节）。

组级视图（主 DAG）· 新排布方案：
  - 一级分区 = EXT / L1 / L2 / L3（组内多数 source_layer 所属；EXT = 73 seam 合为 1 节点）
  - 二级功能簇 = 固定表 F1..F10（断言恰好覆盖 50 组 + EXT，无遗漏无重复）
  - cytoscape layout:'preset' —— 坐标全部在 Python 侧算好，渲染零随机
  - 侧栏/簇计数取「簇总数」；拆列簇标题写 (1/2)(2/2)
  - 内容竖向填充率 ≥ 画布(916) 的 80%，且折叠侧栏时 zoom≈1.0 不溢出
  - hover 差异化高亮：橙=上游依赖(出边) / 绿=下游依赖(入边) / 蓝=自身；双向节点橙优先 + 绿描边

组内下钻视图（主 Agent 已裁定口径）：
  - stub 按所属外部组聚合为一个节点（label「<组名> · 入口 N」，N = 该外部组连到本组的成员数）
  - 序列排序键 = (layer 升序, 是否成员(成员优先), id 升序)；行主序填充网格 → layer 沿阅读方向单调不减
  - 每节点 label 带 layer 角标（L#）；member / stub 由 kind（plugin/seam/disabled vs stub）+ 灰显区分
  - 网格尺寸由「装进画布 + 标签整体落在节点框内 + 节点不重叠」反推：pick_drill_grid() 按节点面积
    择优（字号优先 10px，仅当 10px 不可满足才退 9px）。label 在 Python 侧按实测字符 advance 折行
    并写入显式 '\n'（cytoscape 只按空格折行，不会断开长 token），因此标签不会溢出框。
    build_drills() 内 assert：包围盒 <= 可用区、标签行宽 <= 节点内宽、行高 <= 节点高、
    两两 bounding box 不相交、zoom >= 0.9
  - 下钻边默认 opacity 0.12 / 线宽 1（与组级视图口径一致，防边糊屏）；hover 才升到 0.9 / 1.8
  - 下钻布局全部在 Python 侧算好并写入 DATA.drill（JS 只取用，零布局计算 → 与 assert 同源）
  - member 高亮 / stub 灰显；同样使用差异化 hover；双击成员打开插件详情页，双击聚合 stub 下钻外部组

保留既有能力：?drill=Gxx / #Gxx 深链 + hashchange、返回组级按钮、图例（插件/ seam / 边方向/视图）、
disabled 灰显红边、seam 虚线边、状态栏（模式/节点数/zoom）。

只读 01-dag-data/*.json + 07-checkpoint/v017/disabled-rows.json；只写 04-interactive/index.html。
"""
import json, os, sys, math, collections

sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
DAG_P = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
EXT_P = os.path.join(BASE, "01-dag-data", "external-seams.json")
INV_P = os.path.join(BASE, "07-checkpoint", "v017", "disabled-rows.json")
OUT = os.path.join(BASE, "04-interactive", "index.html")

# ---------------------------------------------------------------- 固定功能簇契约
CLUSTERS = [
    ("F1",  "运行时基座",       "L1", ["G04", "G09", "G45", "G42", "G22"]),
    ("F2",  "会话与上下文",     "L1", ["G33", "G34", "G07", "G17", "G44", "G15", "G21"]),
    ("F3",  "智能与协议",       "L1", ["G23", "G25", "G26"]),
    ("F4",  "工具与执行面",     "L1", ["G36", "G37", "G41", "G47", "G18", "G30", "G38", "G16", "G40", "G10", "G28"]),
    ("F5",  "宿主与工作区",     "L1", ["G03", "G35", "G49"]),
    ("F6",  "客户端 UI",        "L2", ["G06"]),
    ("F7",  "客户端运行时与宿主接入", "L2", ["G05", "G02", "G08", "G11", "G12", "G14", "G20", "G31", "G50"]),
    ("F8",  "协议与远程",       "L3", ["G01", "G24", "G32", "G39", "G43"]),
    ("F9",  "实验与扩展",       "L3", ["G13", "G19", "G27", "G29", "G46", "G48"]),
    ("F10", "外部基座 seam",    "EXT", []),   # EXT 合成为 1 个节点
]
ZONE_ORDER = ["EXT", "L1", "L2", "L3"]

# 与 04-interactive 生产配色一致（38 色循环，50 组按 gid 升序取色）
PALETTE = ["#4f8cff", "#7b61ff", "#2fb98a", "#e8933b", "#e05563", "#3b9fe0", "#9a7bf0", "#e0a03b",
           "#3bc4a0", "#d0546b", "#6c8df5", "#b48a3c", "#54a0e8", "#8a5cf0", "#3ab7c4", "#e07b54",
           "#5f8de0", "#9b6bd4", "#4aa8a0", "#d06a4a", "#6b9bd4", "#b07bd4", "#4ac48e", "#d48a5b",
           "#e8a13b", "#6b8fe8", "#3bc48a", "#d07bd4", "#4f8ce8",
           "#c44f6e", "#4f9ce8", "#8a7bf0", "#2fbfa0", "#e0a03b", "#d46b54", "#6b8fe8", "#a05be0"]
EXT_COLOR = "#b48a3c"

# ---- 组级网格尺寸（受填充率约束反推，见 assert 段） ----
NODE_W, NODE_H = 100, 64
ROW_GAP = 34
COL_GAP, CLUSTER_GAP, ZONE_GAP = 16, 24, 36
CLUSTER_TITLE_H, ZONE_TITLE_H = 20, 26
MAX_ROWS_PER_COL = 10       # 组级：单列超过 10 组则均分为两个子列

# 画布常量（1600x1000 viewport, header 56 + status 28）
CANVAS_H = 916
FILL_MIN = 0.80
COLLAPSED_W = 1600 - 32     # pad 16 两侧
COLLAPSED_H = CANVAS_H - 32

# ---- 组内下钻：确定性网格 + 标签内嵌（label 折行全在 Python 侧算好，JS 零布局计算） ----
D_CANVAS_W = 1300           # 侧栏展开时 #graph 实测宽（1600 - 300）
D_CANVAS_H = 916
D_PAD = 18                  # 与 GRID.layout.bboxPad 一致（cy.fit 的内边距）
D_MIN_ZOOM = 0.9
D_FS = 10.0                 # 下钻节点标签字号（硬性 >= 10px；9px 仅作兜底）
D_LINE_H = D_FS * 1.15      # 行高（与 CSS line-height:1.15 一致）
D_COL_GAP, D_ROW_GAP = 10, 8
D_NODE_MAX_W, D_NODE_MAX_H = 170.0, 62.0
D_NODE_MIN_W, D_NODE_MIN_H = 64.0, 24.0
D_HPAD = 8                  # 文字与框边水平内边距（每侧）→ 折行可用宽 = w - 2*D_HPAD
D_VPAD = 4                  # 文字与框边垂直内边距（每侧）
D_TMW_PAD = 14              # text-max-width = 节点宽 - D_TMW_PAD（须 > 2*D_HPAD，保证不二次折行）

# 每字符 advance（font-size 9px，font-family "Helvetica Neue, Helvetica, sans-serif"）：
# 由 headless Chromium canvas measureText 对本页全部 label 字符实测（2026-09-27），
# 供 build_drills 在 Python 侧确定性地折行；其它字号按 fs/9.0 线性缩放。
_ADV9 = {
    ' ':2.5, '-':2.997, '0':5.005, '1':5.005, '2':5.005, '3':5.005, '4':5.005, '5':5.005, '6':5.005,
    '7':5.005, '8':5.005, '9':5.005, 'A':6.003, 'C':6.5, 'D':6.5, 'H':6.5, 'I':2.5, 'K':6.003, 'L':5.005,
    'M':7.497, 'P':6.003, 'S':6.003, 'U':6.5, 'W':8.495, 'a':5.005, 'b':5.005, 'c':4.5, 'd':5.005, 'e':5.005,
    'f':2.5, 'g':5.005, 'h':5.005, 'i':2, 'j':2, 'k':4.5, 'l':2, 'm':7.497, 'n':5.005, 'o':5.005, 'p':5.005,
    'q':5.005, 'r':2.997, 's':4.5, 't':2.5, 'u':5.005, 'v':4.5, 'w':6.5, 'x':4.5, 'y':4.5, 'z':4.5,
    '·':2.997, '上':9, '下':9, '与':9, '业':9, '主':9, '互':9, '交':9, '付':9, '代':9, '令':9, '件':9, '会':9, '作':9,
    '储':9, '入':9, '关':9, '具':9, '凭':9, '出':9, '划':9, '制':9, '办':9, '务':9, '动':9, '包':9, '区':9, '协':9, '卫':9,
    '压':9, '反':9, '口':9, '启':9, '命':9, '器':9, '型':9, '基':9, '处':9, '外':9, '契':9, '子':9, '存':9, '守':9, '定':9,
    '实':9, '客':9, '宿':9, '展':9, '工':9, '度':9, '座':9, '式':9, '待':9, '心':9, '性':9, '成':9, '户':9, '执':9, '扩':9,
    '技':9, '据':9, '授':9, '控':9, '插':9, '文':9, '断':9, '时':9, '服':9, '权':9, '架':9, '标':9, '核':9, '框':9, '档':9,
    '检':9, '模':9, '沙':9, '注':9, '流':9, '溢':9, '物':9, '特':9, '理':9, '目':9, '码':9, '程':9, '端':9, '管':9, '箱':9,
    '类':9, '系':9, '索':9, '约':9, '终':9, '统':9, '缩':9, '网':9, '置':9, '能':9, '行':9, '规':9, '计':9, '议':9, '设':9,
    '访':9, '诊':9, '话':9, '调':9, '运':9, '进':9, '远':9, '适':9, '通':9, '道':9, '部':9, '配':9, '问':9, '附':9, '集':9,
    '预':9, '馈':9, '验':9,
}


def load():
    with open(DAG_P, "r", encoding="utf-8") as f:
        dag = json.load(f)
    with open(EXT_P, "r", encoding="utf-8") as f:
        ext = json.load(f)
    with open(INV_P, "r", encoding="utf-8") as f:
        inv = json.load(f)
    return dag, ext, inv


# ---------------------------------------------------------------- 组内下钻布局
def _chw(ch, fs):
    """单字符 advance（px）@font-size fs；未知字符取保守上界（不低估，避免溢出）。"""
    w = _ADV9.get(ch)
    if w is None:
        w = 9.0 if ord(ch) >= 0x2e80 else 5.005
    return w * fs / 9.0


def _text_w(s, fs):
    return sum(_chw(c, fs) for c in s)


def _hard_split(s, maxw, fs):
    """无断点可用时的按字符硬断。"""
    out, cur = [], ""
    for ch in s:
        if cur and _text_w(cur + ch, fs) > maxw:
            out.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        out.append(cur)
    return out or [""]


def wrap_label(s, maxw, fs):
    """把 label 折成若干行（每行宽 <= maxw，按 fs 的字符 advance 计）。

    优先在 '-', '/', ' ' 断点折行；仍超宽的残段按字符硬断。
    折行在 Python 侧完成，label 中写入显式 '\\n'；cytoscape 侧不再二次折行。
    """
    lines, cur = [], ""
    for ch in s:
        if cur and _text_w(cur + ch, fs) > maxw:
            idx = max(cur.rfind("-"), cur.rfind("/"), cur.rfind(" "))
            if idx >= 0:
                lines.append(cur[:idx + 1]); cur = cur[idx + 1:] + ch
            else:
                lines.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    fixed = []
    for ln in lines:
        if _text_w(ln, fs) > maxw + 1e-9:
            fixed.extend(_hard_split(ln, maxw, fs))
        else:
            fixed.append(ln)
    return [l.rstrip() for l in fixed if l.strip()] or [""]


def pick_drill_grid(n, labels, fs):
    """选格：装进画布(留 D_PAD) + 标签全部可容于节点框内 + 节点不重叠。

    返回 (area, nc, nr, w, h) 或 None。评分 = 节点面积（越大越可读），
    在满足标签容纳与画布约束的候选里取最大值。
    """
    best = None
    for nc in range(1, n + 1):
        nr = (n + nc - 1) // nc
        availW = D_CANVAS_W - 2 * D_PAD - (nc - 1) * D_COL_GAP
        availH = D_CANVAS_H - 2 * D_PAD - (nr - 1) * D_ROW_GAP
        if availW <= 0 or availH <= 0:
            continue
        w = min(D_NODE_MAX_W, availW / nc)
        h = min(D_NODE_MAX_H, availH / nr)
        if w < D_NODE_MIN_W or h < D_NODE_MIN_H:
            continue
        innerW = w - 2 * D_HPAD
        need_lines = max(len(wrap_label(lb, innerW, fs)) for lb in labels)
        if need_lines * D_LINE_H + 2 * D_VPAD > h + 1e-9:
            continue
        bw = nc * w + (nc - 1) * D_COL_GAP
        bh = nr * h + (nr - 1) * D_ROW_GAP
        if bw > D_CANVAS_W - 2 * D_PAD + 1e-6 or bh > D_CANVAS_H - 2 * D_PAD + 1e-6:
            continue
        area = w * h
        if best is None or area > best[0] + 1e-9:
            best = (area, nc, nr, w, h)
    return best


def build_drills(dag, ext_map, seam_ids, nodes, groups, gstat, disabled_ids):
    """为 50 组 + EXT 各生成一份确定性下钻网格（坐标全在 Python 侧算好）。

    契约（主 Agent 裁定口径）：
      1. stub 按所属外部组聚合为一个节点：label="<组名> · 入口 N"，
         N = 该外部组连到本组的成员数（去重）。
      2. 序列排序键 = (layer 升序, 是否成员(成员优先), id 升序)，行主序填充网格
         → layer 号沿阅读方向单调不减；每节点 label 带 layer 角标 "L#",
         member/stub 由 kind(=plugin/seam/disabled vs stub) 与灰显样式区分。
      3. 网格尺寸由 pick_drill_grid() 反推：装进画布 + 每个标签整体落在节点框内 +
         节点不重叠（字号优先 10px，兜底 9px）。并在本函数内 assert：包围盒 <= 可用区、
         标签行宽/行高 <= 节点框、两两 bounding box 不相交、zoom >= 0.9。
    """
    GNAME = {g: groups[g]["name"] for g in groups}
    GNAME["EXT"] = "外部基座 seam"
    GLAYER = {g: int(round(gstat[g][1])) for g in groups}
    GLAYER["EXT"] = 0

    directed = []
    for e in dag["edges"]:
        directed.append((e["from"], e["to"], "core"))
    for sid, s in ext_map.items():
        for dep in (s.get("referred_by") or []):
            if dep in nodes:
                directed.append((dep, sid, "seam"))

    def member_meta(m):
        if m in nodes:
            n = nodes[m]
            kind = "disabled" if m in disabled_ids else "plugin"
            return n["group_name"], int(n["layer"]), kind, "../02-plugin-pages/%s.html" % m
        return "外部基座seam", 0, "seam", "../02-plugin-pages/%s.html" % m

    drills = {}
    drill_stats = []
    for g in sorted(groups.keys()) + ["EXT"]:
        M = set(seam_ids) if g == "EXT" else set(groups[g]["plugins"])
        mm = set()
        stub_members = collections.defaultdict(set)
        stub_edges = {}                       # (s_final, t_final) -> kind
        for (s, t, kind) in directed:
            si, ti = s in M, t in M
            if si and ti:
                mm.add((s, t, kind))
                continue
            if not (si or ti):
                continue
            member = s if si else t
            other = t if si else s
            og = nodes[other]["group"] if other in nodes else ("EXT" if other in seam_ids else None)
            if og is None or og == g:
                continue
            stub_members[og].add(member)
            sid = "stub_%s_%s" % (g, og)
            s2, t2 = (member, sid) if si else (sid, member)
            stub_edges[(s2, t2)] = "seam" if (stub_edges.get((s2, t2)) == "seam" or kind == "seam") else kind

        seq = []
        for m in M:
            gname, layer, kind, url = member_meta(m)
            seq.append({"layer": layer, "ismember": 0, "id": m,
                        "data": {"id": m, "label": "L%d · %s" % (layer, m), "kind": kind,
                                 "group": g, "gname": gname, "layer": layer,
                                 "url": url, "mode": "member"}})
        for og in sorted(stub_members):
            layer = GLAYER.get(og, 0)
            nm = GNAME.get(og, og)
            sid = "stub_%s_%s" % (g, og)
            seq.append({"layer": layer, "ismember": 1, "id": sid,
                        "data": {"id": sid, "label": "L%d · %s · 入口 %d" % (layer, nm, len(stub_members[og])),
                                 "kind": "stub", "group": og, "gname": nm, "layer": layer,
                                 "mode": "stub", "drill": og}})
        seq.sort(key=lambda x: (x["layer"], x["ismember"], x["id"]))

        # 聚合前 stub 数（旧行为：每个跨组连接点一个 stub）= 与本组相连的外部「节点」去重数
        before = set()
        for (s, t, kind) in directed:
            si, ti = s in M, t in M
            if si == ti:
                continue
            other = t if si else s
            og = nodes[other]["group"] if other in nodes else ("EXT" if other in seam_ids else None)
            if og is not None and og != g:
                before.add(other)
        n_total = len(seq)

        labels = [it["data"]["label"] for it in seq]
        # 字号优先 10px；仅当 10px 下确实装不下（画布/标签容纳不可满足）才退 9px
        pick, fs = None, D_FS
        for fs_try in (D_FS, 9.0):
            pick = pick_drill_grid(n_total, labels, fs_try)
            if pick is not None:
                fs = fs_try
                break
        assert pick is not None, f"[{g}] 下钻 {n_total} 节点在 9px 下仍无法装入画布"
        _, nc, nr, w, h = pick
        cg, rg = D_COL_GAP, D_ROW_GAP
        innerW = w - 2 * D_HPAD
        tmw = w - D_TMW_PAD

        nodes_out = []
        for i, item in enumerate(seq):
            col, row = i % nc, i // nc
            cx = col * (w + cg) + w / 2.0
            cy = row * (h + rg) + h / 2.0
            d = dict(item["data"])
            d["label"] = "\n".join(wrap_label(item["data"]["label"], innerW, fs))
            d["w"], d["h"], d["fs"], d["mw"] = w, h, fs, tmw
            nodes_out.append({"data": d, "position": {"x": round(cx, 2), "y": round(cy, 2)}})

        edges_out = []
        for (s, t, kind) in sorted(mm):
            edges_out.append({"data": {"id": "%s->%s" % (s, t), "source": s, "target": t,
                                       "kind": kind, "mode": "drill"}})
        for (s, t) in sorted(stub_edges):
            edges_out.append({"data": {"id": "%s->%s" % (s, t), "source": s, "target": t,
                                       "kind": stub_edges[(s, t)], "mode": "drill"}})

        # ---------------- 断言：包围盒 / 标签内嵌 / 不重叠 / zoom ----------------
        bw = nc * w + (nc - 1) * cg
        bh = nr * h + (nr - 1) * rg
        assert bw <= D_CANVAS_W - 2 * D_PAD + 1e-6, f"[{g}] 下钻包围盒宽 {bw} 超可用区"
        assert bh <= D_CANVAS_H - 2 * D_PAD + 1e-6, f"[{g}] 下钻包围盒高 {bh} 超可用区"
        # 标签必须整体落在节点框内：行宽 <= 可用宽；行数*行高 + 上下内边距 <= 节点高
        for nd in nodes_out:
            lns = nd["data"]["label"].split("\n")
            lw = max(_text_w(l, fs) for l in lns)
            lh = len(lns) * D_LINE_H + 2 * D_VPAD
            assert lw <= nd["data"]["mw"] + 1e-6, \
                f"[{g}] {nd['data']['id']} 标签行宽 {lw:.1f} 超 text-max-width {nd['data']['mw']:.1f}"
            assert lw <= w - 2 * D_HPAD + 1e-6, \
                f"[{g}] {nd['data']['id']} 标签行宽 {lw:.1f} 超节点内宽 {w - 2 * D_HPAD:.1f}"
            assert lh <= h + 1e-6, \
                f"[{g}] {nd['data']['id']} 标签 {len(lns)} 行高 {lh:.1f} 超节点高 {h:.1f}"
        zoom = min(1.0, (D_CANVAS_W - 2 * D_PAD) / bw, (D_CANVAS_H - 2 * D_PAD) / bh)
        assert zoom >= D_MIN_ZOOM - 1e-9, f"[{g}] 下钻 zoom {zoom:.3f} < {D_MIN_ZOOM}"
        boxes = [(p["position"]["x"] - w / 2.0, p["position"]["y"] - h / 2.0, w, h)
                 for p in nodes_out]
        for a in range(len(boxes)):
            ax, ay, aw, ah = boxes[a]
            for b in range(a + 1, len(boxes)):
                bx, by, bw2, bh2 = boxes[b]
                if ax < bx + bw2 and bx < ax + aw and ay < by + bh2 and by < ay + ah:
                    raise AssertionError(f"[{g}] 下钻节点重叠: {nodes_out[a]['data']['id']} "
                                         f"vs {nodes_out[b]['data']['id']}")
        lay = [x["layer"] for x in seq]
        assert lay == sorted(lay), f"[{g}] 下钻序列 layer 非单调不减"

        hint = ("%s · %d 节点（成员 %d + 聚合 stub %d）· 行主序网格 %d×%d · 字号 %.0fpx · 角标 L# = layer"
                % (g, n_total, len(M), len(stub_members), nc, nr, fs))
        drills[g] = {"nodes": nodes_out, "edges": edges_out,
                     "meta": {"hint": hint, "n": n_total, "members": len(M),
                              "stubs": len(stub_members), "stubsBefore": len(before),
                              "cols": nc, "rows": nr, "nodeW": round(w, 2), "nodeH": round(h, 2),
                              "colGap": cg, "rowGap": rg, "fontSize": fs,
                              "bboxW": round(bw, 2), "bboxH": round(bh, 2), "zoom": round(zoom, 4)}}
        drill_stats.append((g, len(M), len(stub_members), len(before), n_total,
                            round(bw, 2), round(bh, 2), round(zoom, 4), fs))
    return drills, drill_stats


def build_payload():
    dag, ext, inv = load()
    nodes = {n["id"]: n for n in dag["nodes"]}
    groups = {g["id"]: g for g in dag["groups"]}
    ext_map = {e["id"]: e for e in ext["seams"]}
    seams = ext["seams"]

    gids_sorted = sorted(groups.keys())
    GROUP_COLOR = {g: PALETTE[i % len(PALETTE)] for i, g in enumerate(gids_sorted)}

    # ---------------- 自检 1: 功能簇表恰好覆盖 50 组 + EXT ----------------
    all_gids = set(groups.keys())
    listed = []
    for cid, cname, zone, gl in CLUSTERS:
        listed.extend(gl)
    assert len(listed) == len(set(listed)), "功能簇表存在重复组"
    assert set(listed) == all_gids, f"功能簇表覆盖不符: 缺 {sorted(all_gids-set(listed))} / 多 {sorted(set(listed)-all_gids)}"
    assert len(all_gids) == 50, f"组数应为 50, 实为 {len(all_gids)}"
    assert sum(1 for c in CLUSTERS if c[3] == []) == 1, "EXT 功能簇应恰好 1 个"

    # ---------------- 组统计 ----------------
    def group_stats(gid):
        pl = groups[gid]["plugins"]
        lay = [nodes[p]["layer"] for p in pl if p in nodes]
        avg = (sum(lay) / len(lay)) if lay else 0.0
        asm = collections.Counter()
        for p in pl:
            v = nodes.get(p, {}).get("assembled_in") or []
            if not v:
                asm["—"] += 1
            for a in v:
                asm[a] += 1
        top = asm.most_common(1)[0][0] if asm else "—"
        return len(pl), avg, top

    GSTAT = {g: group_stats(g) for g in gids_sorted}

    # ---------------- 列构建（F4 超 10 组 → 拆两子列） ----------------
    columns = []
    for zone in ZONE_ORDER:
        for cid, cname, czone, gl in CLUSTERS:
            if czone != zone:
                continue
            ordered = sorted(gl, key=lambda g: (GSTAT[g][1], g))
            if cid == "F10":
                chunks = [["EXT"]]
            elif len(ordered) > MAX_ROWS_PER_COL:
                half = math.ceil(len(ordered) / 2)
                chunks = [ordered[:half], ordered[half:]]
            else:
                chunks = [ordered] if ordered else [[]]
            for si, ch in enumerate(chunks):
                columns.append({"cid": cid, "cname": cname, "zone": czone,
                                "gids": ch, "sub": si, "nsub": len(chunks),
                                "ctotal": len(gl) if cid != "F10" else 1})

    def gap_for(idx):
        if idx == 0:
            return None
        prev, cur = columns[idx - 1], columns[idx]
        if cur["cid"] == prev["cid"]:
            return COL_GAP
        if cur["zone"] == prev["zone"]:
            return CLUSTER_GAP
        return ZONE_GAP

    lefts = [0.0]
    for i in range(1, len(columns)):
        lefts.append(lefts[-1] + NODE_W + gap_for(i))
    width = lefts[-1] + NODE_W

    max_rows = max(len(c["gids"]) for c in columns)
    node_bbox_h = (max_rows - 1) * (NODE_H + ROW_GAP) + NODE_H
    content_h = ZONE_TITLE_H + CLUSTER_TITLE_H + max_rows * NODE_H + (max_rows - 1) * ROW_GAP

    # ---------------- 尺寸断言（填充率 / 不溢出） ----------------
    assert width <= COLLAPSED_W, f"内容宽 {width} 超折叠画布可容纳宽 {COLLAPSED_W}"
    assert node_bbox_h <= COLLAPSED_H, f"内容高 {node_bbox_h} 超折叠画布可容纳高 {COLLAPSED_H}"
    assert node_bbox_h / CANVAS_H >= FILL_MIN, f"竖向填充率 {node_bbox_h/CANVAS_H:.3f} < {FILL_MIN}"

    # ---------------- 节点坐标（preset，零随机） ----------------
    positions = {}
    for i, col in enumerate(columns):
        cx = lefts[i] + NODE_W / 2.0
        y0 = ZONE_TITLE_H + CLUSTER_TITLE_H + NODE_H / 2.0
        for r, gid in enumerate(col["gids"]):
            positions[gid] = (round(cx, 2), round(y0 + r * (NODE_H + ROW_GAP), 2))
        col["x1"] = round(lefts[i], 2)
        col["x2"] = round(lefts[i] + NODE_W, 2)

    assert set(positions.keys()) == all_gids | {"EXT"}, "坐标未覆盖全部 50 组 + EXT"

    min_gap = 1e9
    ids = list(positions.keys())
    for a in range(len(ids)):
        for b in range(a + 1, len(ids)):
            xa, ya = positions[ids[a]]
            xb, yb = positions[ids[b]]
            dx, dy = abs(xa - xb), abs(ya - yb)
            assert dx >= NODE_W - 0.01 or dy >= NODE_H - 0.01, f"组坐标重叠: {ids[a]} vs {ids[b]}"
            min_gap = min(min_gap, math.hypot(dx, dy))

    # ---------------- 组级边（264 = 218 非EXT + 46 EXT） ----------------
    pair_set = set()
    for e in dag["edges"]:
        a, b = nodes.get(e["from"]), nodes.get(e["to"])
        if a and b and a["group"] != b["group"]:
            pair_set.add((a["group"], b["group"]))
    non_ext_pairs = len(pair_set)
    ext_pairs = set()
    for s in seams:
        for dep in (s.get("referred_by") or []):
            if dep in nodes:
                ext_pairs.add((nodes[dep]["group"], "EXT"))
    edge_pairs = sorted(pair_set | ext_pairs)
    assert len(edge_pairs) == 264, f"组间边应为 264, 实为 {len(edge_pairs)}"

    # ---------------- 组级节点元素 ----------------
    grid_nodes = []
    node_by_gid = {}
    for gid in gids_sorted:
        cnt, avg, asm = GSTAT[gid]
        x, y = positions[gid]
        label = groups[gid]["name"] + "\n" + gid + " · " + str(cnt)
        nd = {"data": {"id": "grp-" + gid, "label": label, "kind": "group", "group": gid,
                       "gname": groups[gid]["name"], "count": cnt, "asm": asm,
                       "avg_layer": round(avg, 2), "color": GROUP_COLOR[gid]},
              "position": {"x": x, "y": y}}
        grid_nodes.append(nd)
        node_by_gid[gid] = nd["data"]

    ex, ey = positions["EXT"]
    ext_nd = {"data": {"id": "grp-EXT", "label": "外部基座 seam\nEXT · " + str(len(seams)),
                       "kind": "ext", "group": "EXT", "gname": "外部基座 seam",
                       "count": len(seams), "asm": "vendor", "avg_layer": 0, "color": EXT_COLOR},
              "position": {"x": ex, "y": ey}}
    grid_nodes.append(ext_nd)
    node_by_gid["EXT"] = ext_nd["data"]

    grid_edges = [{"data": {"id": "grp-%s->grp-%s" % (gs, gt), "source": "grp-" + gs,
                            "target": "grp-" + gt, "kind": "group", "mode": "grp"}}
                  for gs, gt in edge_pairs]

    # ---------------- 侧栏三级树（簇 count = 簇总数，只出现一次） ----------------
    tree = []
    for zone in ZONE_ORDER:
        zclusters = []
        for cid, cname, czone, gl in CLUSTERS:
            if czone != zone:
                continue
            cols = [c for c in columns if c["cid"] == cid]
            item = {"id": cid, "name": cname,
                    "count": (1 if cid == "F10" else len(gl)), "groups": []}
            for c in cols:
                for gid in c["gids"]:
                    d = node_by_gid[gid]
                    item["groups"].append({"gid": gid, "name": d["gname"], "count": d["count"],
                                           "asm": d["asm"], "color": d["color"], "sub": c["sub"]})
            zclusters.append(item)
        tree.append({"zone": zone, "count": sum(c["count"] for c in zclusters), "clusters": zclusters})

    zones_ov = []
    for zone in ZONE_ORDER:
        cols = [c for c in columns if c["zone"] == zone]
        zones_ov.append({"name": zone, "count": sum(len(c["gids"]) for c in cols),
                         "x1": min(c["x1"] for c in cols), "x2": max(c["x2"] for c in cols)})
    clusters_ov = []
    for c in columns:
        title = c["cname"] + " · " + str(c["ctotal"])
        if c["nsub"] > 1:
            title += " (%d/%d)" % (c["sub"] + 1, c["nsub"])
        clusters_ov.append({"id": c["cid"], "zone": c["zone"], "title": title,
                            "count": c["ctotal"], "sub": c["sub"], "nsub": c["nsub"],
                            "x1": c["x1"], "x2": c["x2"]})

    grid = {
        "nodes": grid_nodes,
        "edges": grid_edges,
        "tree": tree,
        "overlay": {"zones": zones_ov, "clusters": clusters_ov,
                    "zoneTitleH": ZONE_TITLE_H, "clusterTitleH": CLUSTER_TITLE_H,
                    "contentH": round(content_h, 2)},
        "layout": {"nodeW": NODE_W, "nodeH": NODE_H, "width": round(width, 2),
                   "height": round(content_h, 2), "bboxPad": 18},
        "stats": {"groups": 50, "nodes": len(grid_nodes), "edges": len(grid_edges),
                  "seams": len(seams), "nonExtEdges": non_ext_pairs, "extEdges": len(ext_pairs),
                  "nodeBboxH": node_bbox_h, "fillRatio": round(node_bbox_h / CANVAS_H, 4),
                  "minCenterDist": round(min_gap, 2)},
    }

    # ---------------- 插件 / seam / 下钻数据（与既有生产一致） ----------------
    disabled_ids = set()
    for d in inv.get("disabled_base_rows", []):
        if d.get("node") and d["node"] in nodes:
            disabled_ids.add(d["node"])

    # 下钻网格（确定性，坐标在 Python 侧算好；含装进画布/不重叠/zoom 断言）
    drills, drill_stats = build_drills(dag, ext_map, set(ext_map.keys()), nodes, groups,
                                       GSTAT, disabled_ids)

    plugin_nodes = []
    for nid, n in nodes.items():
        plugin_nodes.append({"data": {
            "id": nid, "label": nid,
            "kind": "disabled" if nid in disabled_ids else "plugin",
            "group": n["group"], "gname": n["group_name"], "layer": n["layer"],
            "url": f"../02-plugin-pages/{nid}.html"}})

    ext_nodes = []
    for sid, s in ext_map.items():
        ext_nodes.append({"data": {
            "id": sid, "label": sid, "kind": "seam", "group": "EXT",
            "gname": "外部基座seam", "layer": 0,
            "url": f"../02-plugin-pages/{sid}.html"}})

    edge_list = []
    for e in dag["edges"]:
        edge_list.append({"data": {"id": f"{e['from']}->{e['to']}", "source": e["from"],
                                   "target": e["to"], "kind": "core"}})
    for sid, s in ext_map.items():
        for dep in s.get("referred_by", []):
            if dep in nodes:
                edge_list.append({"data": {"id": f"{dep}->{sid}", "source": dep,
                                           "target": sid, "kind": "seam"}})

    group_edges = []
    seen = set()
    for e in dag["edges"]:
        gs, gt = nodes[e["from"]]["group"], nodes[e["to"]]["group"]
        if gs != gt and (gs, gt) not in seen:
            seen.add((gs, gt))
            group_edges.append({"data": {"id": f"grp-{gs}->grp-{gt}", "source": "grp-"+gs,
                                         "target": "grp-"+gt, "kind": "group"}})
    for sid, s in ext_map.items():
        for dep in s.get("referred_by", []):
            if dep in nodes:
                gs = nodes[dep]["group"]
                if (gs, "EXT") not in seen:
                    seen.add((gs, "EXT"))
                    group_edges.append({"data": {"id": f"grp-{gs}->grp-EXT", "source": "grp-"+gs,
                                                 "target": "grp-EXT", "kind": "group"}})

    l1 = sum(1 for n in nodes.values() if n.get("source_layer") == "L1")
    l2 = sum(1 for n in nodes.values() if n.get("source_layer") == "L2")
    l3 = sum(1 for n in nodes.values() if n.get("source_layer") == "L3")

    payload = {
        "grid": grid,
        "drill": drills,
        "plugins": plugin_nodes,
        "seams": ext_nodes,
        "edges": edge_list,
        "groupEdges": group_edges,
        "groups": {gid: {"name": groups[gid]["name"], "color": GROUP_COLOR[gid]} for gid in gids_sorted},
        "groupColor": GROUP_COLOR,
        "extColor": EXT_COLOR,
        "disabledIds": sorted(disabled_ids),
        "legend": {"pluginCount": len(nodes), "l1": l1, "l2": l2, "l3": l3,
                   "seamCount": len(seams), "groupCount": len(gids_sorted)},
    }
    stats = {"nodes": len(grid_nodes), "edges": len(grid_edges), "columns": len(columns),
             "width": round(width, 2), "nodeBboxH": node_bbox_h,
             "fillRatio": round(node_bbox_h / CANVAS_H, 4), "minCenterDist": round(min_gap, 2),
             "plugins": len(plugin_nodes), "seams": len(ext_nodes),
             "disabled": len(disabled_ids), "coreEdges": len(edge_list), "groupEdges": len(group_edges),
             "drills": len(drills), "drillStats": drill_stats}
    return payload, stats


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DeepSeek Harness 插件 DAG 交互总览</title>
<style>
  :root { --bg:#0f1117; --panel:#161a22; --border:#2a2f3a; --text:#e6e8ee; --dim:#9aa3b2;
          --accent:#4f8cff; --ext:#b48a3c; --up:#e8933b; --down:#2fb98a; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,sans-serif; height:100vh; overflow:hidden; }
  header { position:fixed; top:0; left:0; right:0; height:56px; z-index:12; background:var(--panel);
           border-bottom:1px solid var(--border); padding:10px 16px; display:flex; align-items:center; gap:12px; flex-wrap:wrap; }
  header h1 { font-size:15px; font-weight:600; white-space:nowrap; }
  .badge { background:#20324f; color:#7fb0ff; padding:2px 9px; border-radius:20px; font-size:11px; white-space:nowrap; }
  .badge.ext { background:#3a2f1a; color:#e0b25e; }
  header a { color:var(--accent); text-decoration:none; font-size:12px; white-space:nowrap; }
  header a:hover { text-decoration:underline; }
  header button { background:#20324f; color:#7fb0ff; border:1px solid #2a3a55; border-radius:20px;
                  padding:4px 12px; font-size:12px; cursor:pointer; white-space:nowrap; }
  header button:hover { background:#28406a; }
  .hint { color:var(--dim); font-size:11px; }
  /* #graph 显式留给侧栏 300px —— 修掉 right:0 与 fixed 侧栏重叠 */
  #graph { position:fixed; top:56px; left:0; right:300px; bottom:28px; background:transparent; }
  /* overlay 是 <canvas>(replaced element): left/right 撑不开尺寸, JS 按 #graph 容器显式设宽高 */
  #overlay { position:fixed; top:56px; left:0; pointer-events:none; z-index:8; }
  #side { position:fixed; right:0; top:56px; bottom:28px; width:300px; background:var(--panel);
          border-left:1px solid var(--border); padding:12px; overflow:auto; z-index:9; }
  #side h2 { font-size:12px; margin:12px 0 6px; color:var(--dim); letter-spacing:.05em; }
  #side .legend { font-size:11px; color:var(--dim); line-height:1.85; }
  #side .legend b { color:var(--text); }
  .sw-inline { display:inline-block; width:10px; height:10px; border-radius:2px; vertical-align:middle; margin-right:3px; }
  .znode { font-size:12px; font-weight:700; color:#c8d4eb; margin:8px 0 4px; padding:4px 6px;
           background:#1b2130; border-radius:4px; }
  .cnode { font-size:11px; color:#9fb0cc; margin:6px 0 3px 4px; }
  .gitem { display:flex; align-items:center; gap:6px; font-size:11px; color:var(--dim);
           padding:3px 6px; border-radius:4px; cursor:pointer; margin-left:8px; }
  .gitem:hover { background:#22304a; color:var(--text); }
  .gitem.active { background:#2b4066; color:var(--text); }
  .gitem .sw { width:11px; height:11px; border-radius:2px; flex:0 0 auto; }
  .gitem .gname { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; max-width:104px; }
  .gitem .gid { color:#7f8ea8; font-family:ui-monospace,monospace; }
  .gitem .drillbtn { margin-left:auto; background:#243040; color:#9fc0f0; border:1px solid #33465f;
                     border-radius:9px; padding:0 7px; font-size:10px; cursor:pointer; }
  .gitem .drillbtn:hover { background:#2f4568; }
  #status { position:fixed; left:0; right:0; bottom:0; height:28px; z-index:12; background:var(--panel);
            border-top:1px solid var(--border); display:flex; align-items:center; gap:18px;
            padding:0 16px; font-size:11px; color:var(--dim); }
  #status b { color:var(--text); }
</style>
</head>
<body>
<header>
  <h1>DeepSeek Harness 插件 DAG <span class="badge">交互总览</span> <span class="badge ext">外部 seam 基座</span></h1>
  <a href="../index.html">← 返回任务目录</a>
  <a href="../03-groups/index.html">组目录</a>
  <span id="groupcrumb" style="display:none;color:var(--accent);font-size:13px;font-weight:600;"></span>
  <button id="backbtn" style="display:none;">← 返回组级视图</button>
  <button id="togglebtn">折叠侧栏</button>
  <span class="hint">单击节点=差异化高亮邻域 · 双击组节点=下钻 · 侧栏悬停=高亮 · 拖拽平移 / 滚轮缩放</span>
</header>
<div id="side">
  <h2>图例</h2>
  <div class="legend">
    <b>插件节点</b>（__PLUGIN_COUNT__ 个：L1 __L1__ 核心 + L2 __L2__ web-app + L3 __L3__）<br>
    <b>外部 seam 节点</b>（__SEAM_COUNT__ 个基座包）<br>
    <b>依赖边</b>：A → B 表示 A 依赖 B<br>
    <b>hover 高亮</b>：
      <span class="sw-inline" style="background:#e8933b"></span>橙 = 上游依赖（本节点依赖它）·
      <span class="sw-inline" style="background:#2fb98a"></span>绿 = 下游依赖（它依赖本节点）·
      <span class="sw-inline" style="background:#4f8cff"></span>蓝 = 自身<br>
    <span style="color:#8fb0e0">橙边 + 绿描边</span> = 同时存在上下游（橙色优先显示，绿描边表下游）<br>
    <b>灰色</b> = 组内下钻的聚合 stub（按外部组聚合，label「组名 · 入口 N」，双击下钻到该外部组）·
    <b>红边灰底</b> = disabled 装配行<br>
    <b>虚线边</b> = 外部 seam 依赖<br>
    <b>视图</b>：组级（__GROUP_COUNT__ 组）→ 双击组节点 / 侧栏「下钻」进入组内插件 DAG；
    组内：双击插件节点打开详情页
  </div>
  <h2>导航（区 / 簇 / 组）</h2>
  <div id="tree"></div>
  <h2>组配色</h2>
  <div id="glegend"></div>
</div>
<div id="status">
  模式 <b id="zmode">组级</b> · 节点 <b id="zcount">0</b> · zoom <b id="zzoom">-</b> · 包围盒 <b id="zbbox">-</b>
</div>
<div id="graph"></div>
<canvas id="overlay"></canvas>

<script src="vendor/cytoscape.min.js"></script>
<script src="vendor/cytoscape-dagre.min.js"></script>
<script>
const DATA = __DATA__;
const GRID = DATA.grid;
const NODE_W = GRID.layout.nodeW, NODE_H = GRID.layout.nodeH;
const C_SELF = '#4f8cff', C_UP = '#e8933b', C_DOWN = '#2fb98a';

let currentGroup = null;   // null = 组级视图; 'G01'.. / 'EXT' = 组内视图
let drillMeta = null;

// ---------------- URL 路由: ?drill=Gxx 或 #Gxx ----------------
function groupFromUrl(){
  const u = new URL(window.location.href);
  let g = u.searchParams.get('drill');
  if (!g && u.hash) g = decodeURIComponent(u.hash.replace(/^#/, ''));
  if (!g) return null;
  if (g === 'EXT') return 'EXT';
  return (DATA.groups && DATA.groups[g]) ? g : null;
}
function syncUrl(){
  const u = new URL(window.location.href);
  if (currentGroup === null){ u.searchParams.delete('drill'); u.hash = ''; }
  else { u.searchParams.set('drill', currentGroup); u.hash = currentGroup; }
  history.replaceState(null, '', u.pathname + (u.search || '') + (u.hash || ''));
}

// ---------------- 组内下钻: 读取生成器预算的确定性网格（stub 按外部组聚合） ----------------
// 布局全部由 07-checkpoint/gen-overview.py 的 build_drills() 在 Python 侧算好并断言
// （包围盒 <= 画布 / 两两不重叠 / zoom >= 0.9），此处只做取用，不做任何布局计算。
function buildDrill(g){
  const d = DATA.drill[g];
  if (!d) return {nodes:[], edges:[], meta:{hint:''}};
  const nodes = d.nodes.map(function(n){ return {data:Object.assign({}, n.data),
                                                position:{x:n.position.x, y:n.position.y}}; });
  const edges = d.edges.map(function(e){ return {data:Object.assign({}, e.data)}; });
  return {nodes:nodes, edges:edges, meta:d.meta};
}

// ---------------- cytoscape ----------------
const cy = cytoscape({
  container: document.getElementById('graph'),
  elements: [],
  style: [
    { selector:'node', style:{
        label:'data(label)', 'text-valign':'center', 'text-halign':'center', color:'#ffffff',
        'font-size':9, 'line-height':1.15, 'text-wrap':'wrap', 'text-max-width': NODE_W - 14 }},
    { selector:'node[kind="group"]', style:{
        'background-color':'data(color)', width:NODE_W, height:NODE_H, shape:'round-rectangle',
        'border-width':2.5, 'border-color':'rgba(255,255,255,0.55)' }},
    { selector:'node[kind="ext"]', style:{
        'background-color':'data(color)', width:NODE_W, height:NODE_H, shape:'round-rectangle',
        'border-width':3, 'border-color':'#e0b25e' }},
    // ---- 组内下钻节点（尺寸/字号由生成器按画布反推，随 data 下发） ----
    { selector:'node[kind="plugin"]', style:{
        'background-color': function(ele){ return DATA.groupColor[ele.data('group')] || '#2b3550'; },
        'border-width':1.5, 'border-color':'rgba(255,255,255,0.35)',
        width:'data(w)', height:'data(h)',
        shape:'round-rectangle', 'font-size':'data(fs)', 'text-max-width':'data(mw)' }},
    { selector:'node[kind="seam"]', style:{
        'background-color':'#3a2f1a', 'border-width':1.5, 'border-color':'#8a6a30',
        width:'data(w)', height:'data(h)', shape:'round-rectangle', 'font-size':'data(fs)',
        'text-max-width':'data(mw)' }},
    { selector:'node[kind="disabled"]', style:{
        'background-color':'#3a3f4a', 'border-width':1.5, 'border-color':'#c0504d',
        width:'data(w)', height:'data(h)', shape:'round-rectangle', opacity:0.55,
        'font-size':'data(fs)', 'text-max-width':'data(mw)' }},
    { selector:'node[kind="stub"]', style:{
        'background-color':'#2a2e38', 'border-width':1, 'border-color':'#555a66',
        width:'data(w)', height:'data(h)', opacity:0.6, 'font-size':'data(fs)',
        'text-max-width':'data(mw)', color:'#9aa3b2' }},
    // ---- 边：组级 / 下钻 / seam ----
    { selector:'edge[mode="grp"]', style:{
        'curve-style':'straight', 'line-color':'#6a7488', 'target-arrow-color':'#6a7488',
        width:1, 'target-arrow-shape':'triangle', 'arrow-scale':0.6, opacity:0.15 }},
    { selector:'edge[mode="drill"]', style:{
        'curve-style':'bezier', 'line-color':'#4a5265', 'target-arrow-color':'#4a5265',
        width:1, 'target-arrow-shape':'triangle', 'arrow-scale':0.7, opacity:0.12 }},
    { selector:'edge[kind="seam"]', style:{
        'line-color':'#8a6a30', 'target-arrow-color':'#8a6a30', width:1.2, 'line-style':'dashed' }},
    // ---- 差异化高亮（必须最后定义以获得优先权） ----
    { selector:'node.hl-self', style:{ 'border-color':C_SELF, 'border-width':4, opacity:1 }},
    { selector:'node.hl-up',   style:{ 'border-color':C_UP, 'border-width':3, opacity:1 }},
    { selector:'node.hl-down', style:{ 'border-color':C_DOWN, 'border-width':3, opacity:1 }},
    { selector:'node.hl-both', style:{ 'border-color':C_UP, 'border-width':3,
        'outline-color':C_DOWN, 'outline-width':3, 'outline-opacity':1, opacity:1 }},
    { selector:'node.hl-dim',  style:{ opacity:0.12 }},
    { selector:'edge.hl-up',   style:{ 'line-color':C_UP, 'target-arrow-color':C_UP, opacity:0.9, width:1.8 }},
    { selector:'edge.hl-down', style:{ 'line-color':C_DOWN, 'target-arrow-color':C_DOWN, opacity:0.9, width:1.8 }},
    { selector:'edge.hl-dim',  style:{ opacity:0.05, width:1 }}
  ],
  layout: { name:'preset' },
  wheelSensitivity: 0.3, minZoom: 0.1, maxZoom: 4
});
window.__cy = cy;

// ---------------- 侧栏三级列表 ----------------
const side = document.getElementById('tree');
function makeGroupItem(g){
  const d = document.createElement('div');
  d.className = 'gitem';
  d.dataset.gid = g.gid;
  d.innerHTML = '<span class="sw" style="background:' + g.color + '"></span>'
    + '<span class="gname" title="' + g.name + '">' + g.name + '</span>'
    + '<span class="gid">' + g.gid + '</span>'
    + '<span class="gid">' + g.count + '</span>'
    + '<button class="drillbtn" title="进入组内下钻">下钻</button>';
  d.addEventListener('mouseenter', function(){ applyHighlight(cy.getElementById('grp-' + g.gid)); });
  d.addEventListener('mouseleave', clearHighlight);
  d.addEventListener('click', function(ev){
    if (ev.target && ev.target.classList.contains('drillbtn')) return;
    const n = cy.getElementById('grp-' + g.gid);
    if (n && n.length){ applyHighlight(n); cy.animate({center:{eles:n}, zoom:Math.max(cy.zoom(), 0.9)}, {duration:300}); }
  });
  d.querySelector('.drillbtn').addEventListener('click', function(ev){
    ev.stopPropagation(); enterGroup(g.gid);
  });
  return d;
}
GRID.tree.forEach(function(zn){
  const h = document.createElement('div');
  h.className = 'znode';
  h.textContent = zn.zone + ' 区 · ' + zn.count + ' 组';
  side.appendChild(h);
  zn.clusters.forEach(function(cl){
    const ch = document.createElement('div');
    ch.className = 'cnode';
    ch.textContent = cl.id + ' ' + cl.name + ' · ' + cl.count + ' 组';
    side.appendChild(ch);
    cl.groups.forEach(function(g){ side.appendChild(makeGroupItem(g)); });
  });
});

// 组配色图例
const gl = document.getElementById('glegend');
Object.keys(DATA.groups).forEach(g => {
  const d = document.createElement('div');
  d.style.cssText = 'display:flex;align-items:center;gap:8px;font-size:11px;margin:2px 0;color:var(--dim);';
  const sw = document.createElement('span');
  sw.style.cssText = 'width:12px;height:12px;border-radius:3px;background:' + DATA.groupColor[g] + ';';
  d.appendChild(sw);
  d.appendChild(document.createTextNode(DATA.groups[g].name + ' (' + g + ')'));
  gl.appendChild(d);
});

// ---------------- 差异化高亮 ----------------
function clearHighlight(){
  cy.elements().removeClass('hl-self hl-up hl-down hl-both hl-dim');
}
function applyHighlight(node){
  clearHighlight();
  if (!node || node.length === 0) return;
  const selfId = node.id();
  node.addClass('hl-self');
  const outEdges = node.outgoers('edge');
  const inEdges = node.incomers('edge');
  const outNodes = node.outgoers('node');
  const inNodes = node.incomers('node');
  const outIds = new Set(outNodes.map(n => n.id()));
  const inIds = new Set(inNodes.map(n => n.id()));
  outEdges.addClass('hl-up');
  inEdges.addClass('hl-down');
  cy.edges().not(outEdges.union(inEdges)).addClass('hl-dim');
  cy.nodes().forEach(n => {
    const id = n.id();
    if (id === selfId) return;
    const o = outIds.has(id), i = inIds.has(id);
    if (o && i) n.addClass('hl-both');       // 双向: 橙优先 + 绿描边
    else if (o) n.addClass('hl-up');
    else if (i) n.addClass('hl-down');
    else n.addClass('hl-dim');
  });
}
window.__applyHighlight = applyHighlight;
window.__clearHighlight = clearHighlight;
window.__hlSets = function(){
  const ids = sel => cy.nodes(sel).map(n => n.id()).sort();
  return { self: ids('.hl-self'), up: ids('.hl-up'), down: ids('.hl-down'),
           both: ids('.hl-both'), dim: ids('.hl-dim') };
};

// ---------------- overlay（区带/区标题/簇标题；下钻列标题） ----------------
const canvas = document.getElementById('overlay');
const octx = canvas.getContext('2d');
let dpr = window.devicePixelRatio || 1;
function sizeCanvas(){
  // <canvas> 是 replaced element: left/right 撑不开尺寸, 必须按 #graph 容器显式设定
  const g = document.getElementById('graph');
  const w = g.clientWidth, h = g.clientHeight;
  dpr = window.devicePixelRatio || 1;
  canvas.style.width = w + 'px';
  canvas.style.height = h + 'px';
  canvas.width = Math.round(w * dpr);
  canvas.height = Math.round(h * dpr);
}
function drawOverlay(){
  const z = cy.zoom(), pan = cy.pan();
  const W = canvas.clientWidth, H = canvas.clientHeight;
  octx.setTransform(dpr, 0, 0, dpr, 0, 0);
  octx.clearRect(0, 0, W, H);
  const mx = x => x * z + pan.x;
  const my = y => y * z + pan.y;
  octx.textAlign = 'center';
  octx.textBaseline = 'middle';
  if (currentGroup === null){
    GRID.overlay.zones.forEach(function(zn){
      const x1 = mx(zn.x1) - 7, x2 = mx(zn.x2) + 7;
      const y1 = my(0), y2 = my(GRID.overlay.contentH);
      octx.fillStyle = 'rgba(255,255,255,0.025)';
      octx.fillRect(x1, y1, x2 - x1, y2 - y1);
      octx.strokeStyle = 'rgba(255,255,255,0.10)';
      octx.strokeRect(x1, y1, x2 - x1, y2 - y1);
      octx.fillStyle = 'rgba(205,216,238,0.95)';
      octx.font = 'bold 13px system-ui,sans-serif';
      octx.fillText(zn.name + ' 区 · ' + zn.count + ' 组', (x1 + x2) / 2, my(GRID.overlay.zoneTitleH / 2));
    });
    GRID.overlay.clusters.forEach(function(cl){
      const cx = (mx(cl.x1) + mx(cl.x2)) / 2;
      octx.fillStyle = cl.zone === 'EXT' ? 'rgba(224,178,94,0.92)' : 'rgba(155,172,200,0.92)';
      octx.font = '10px system-ui,sans-serif';
      octx.fillText(cl.title, cx, my(GRID.overlay.zoneTitleH + GRID.overlay.clusterTitleH / 2));
    });
  } else if (drillMeta){
    // 下钻网格提示（行主序 · 角标 L# = layer）。不新增 cytoscape 节点，仅画布文字。
    octx.save();
    octx.textAlign = 'left';
    octx.textBaseline = 'top';
    octx.fillStyle = 'rgba(155,172,200,0.88)';
    octx.font = 'bold 11px system-ui,sans-serif';
    octx.fillText(drillMeta.hint || '', 12, 12);
    octx.restore();
  }
}
function refreshOverlay(){ sizeCanvas(); drawOverlay(); }

// ---------------- 渲染 ----------------
function fitView(){
  cy.resize();
  cy.fit(cy.elements(), GRID.layout.bboxPad);
  if (cy.zoom() > 1){ cy.zoom(1); cy.center(); }
}
function render(){
  clearHighlight();
  cy.elements().remove();
  drillMeta = null;
  if (currentGroup === null){
    cy.add(GRID.nodes);
    cy.add(GRID.edges);
  } else {
    const r = buildDrill(currentGroup);
    drillMeta = r.meta;
    cy.add(r.nodes);
    cy.add(r.edges);
  }
  cy.layout({ name:'preset' }).run();
  fitView();
  refreshOverlay();
  updateUI();
}

// ---------------- 模式 / URL ----------------
function enterGroup(g){
  currentGroup = (g === 'EXT') ? 'EXT' : g;
  render(); syncUrl();
}
function goBack(){
  if (currentGroup !== null){ currentGroup = null; render(); syncUrl(); }
}
document.getElementById('backbtn').addEventListener('click', goBack);

// ---------------- 交互分工: 单击=高亮 · 双击=下钻(组级)/打开详情(组内) ----------------
cy.on('mouseover', 'node', function(evt){ applyHighlight(evt.target); });   // hover: 差异化高亮
cy.on('mouseout', 'node', function(){ clearHighlight(); });
cy.on('tap', 'node', function(evt){
  clearHighlight();
  applyHighlight(evt.target);           // 单击: 高亮
});
cy.on('dbltap', 'node', function(evt){
  const n = evt.target;
  if (currentGroup === null){
    const g = n.data('group');
    if (g) enterGroup(g);               // 组级双击: 下钻
  } else {
    const dg = n.data('drill');         // 聚合 stub 双击: 下钻到其所属外部组
    if (dg) { enterGroup(dg); return; }
    const url = n.data('url');
    if (url) window.location.href = url;  // 组内双击: 打开详情页
  }
});
cy.on('tap', function(evt){ if (evt.target === cy) clearHighlight(); });

// ---------------- 侧栏折叠 ----------------
let collapsed = false;
const graphEl = document.getElementById('graph');
function setSidebar(){
  document.getElementById('side').style.display = collapsed ? 'none' : 'block';
  graphEl.style.right = collapsed ? '0px' : '300px';
  document.getElementById('togglebtn').textContent = collapsed ? '展开侧栏' : '折叠侧栏';
  cy.resize();
  setTimeout(function(){ fitView(); refreshOverlay(); }, 30);
}
document.getElementById('togglebtn').addEventListener('click', function(){ collapsed = !collapsed; setSidebar(); });
window.addEventListener('resize', function(){ cy.resize(); refreshOverlay(); });
cy.on('pan zoom', function(){ drawOverlay(); updateStatus(); });

// ---------------- 状态栏 ----------------
function updateStatus(){
  document.getElementById('zcount').textContent = cy.nodes().length;
  document.getElementById('zzoom').textContent = cy.zoom().toFixed(2);
  const bb = cy.elements().boundingBox();
  document.getElementById('zbbox').textContent = Math.round(bb.w) + ' x ' + Math.round(bb.h);
}
function updateUI(){
  const cnt = cy.nodes().length;
  document.getElementById('zcount').textContent = cnt;
  if (currentGroup === null){
    document.getElementById('zmode').textContent = '组级';
    document.getElementById('groupcrumb').textContent = '';
    document.getElementById('backbtn').style.display = 'none';
  } else {
    const gname = DATA.groups[currentGroup] ? DATA.groups[currentGroup].name : '外部基座seam';
    document.getElementById('zmode').textContent = currentGroup + ' · ' + gname;
    document.getElementById('groupcrumb').textContent = currentGroup + ' · ' + gname;
    document.getElementById('backbtn').style.display = 'inline-block';
  }
  updateStatus();
  document.querySelectorAll('.gitem').forEach(function(d){
    d.classList.toggle('active', d.dataset.gid === currentGroup);
  });
}

// ---------------- 初始渲染: ?drill=Gxx / #Gxx 深链 ----------------
currentGroup = groupFromUrl();
render();
syncUrl();
window.addEventListener('hashchange', function(){ currentGroup = groupFromUrl(); render(); });
</script>
</body>
</html>
"""


def render_html(payload):
    lg = payload["legend"]
    html_page = TEMPLATE
    html_page = html_page.replace("__DATA__", json.dumps(payload, ensure_ascii=False))
    html_page = (html_page
                 .replace("__PLUGIN_COUNT__", str(lg["pluginCount"]))
                 .replace("__L1__", str(lg["l1"]))
                 .replace("__L2__", str(lg["l2"]))
                 .replace("__L3__", str(lg["l3"]))
                 .replace("__SEAM_COUNT__", str(lg["seamCount"]))
                 .replace("__GROUP_COUNT__", str(lg["groupCount"])))
    return html_page


def main():
    payload, stats = build_payload()
    html_page = render_html(payload)

    # 产物自检: UTF-8 无替换字符 / div 配平
    assert "\ufffd" not in html_page, "产物含替换字符 U+FFFD"
    n_open = html_page.count("<div")
    n_close = html_page.count("</div>")
    assert n_open == n_close, f"div 不配平: open={n_open} close={n_close}"

    with open(OUT, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(html_page)

    print(f"[OK] 组级网格: 宽 {stats['width']} x 高 {stats['nodeBboxH']} "
          f"(填充率 {stats['fillRatio']:.3f}, 最近中心距 {stats['minCenterDist']})")
    print(f"[OK] 组级节点={stats['nodes']} 边={stats['edges']} 列={stats['columns']}")
    print(f"[OK] 下钻网格 {stats['drills']} 组: 全部 assert 通过"
          f"（包围盒<=可用区 / 标签整体在节点框内 / 两两不重叠 / zoom>=0.9）")
    for (g, nm, ns, nb, n, bw, bh, z, fs) in sorted(stats["drillStats"], key=lambda r: -r[4])[:5]:
        print(f"      {g}: 成员 {nm} + 聚合stub {ns}（改造前 stub {nb}）→ {n} 节点, "
              f"bbox {bw}x{bh}, zoom {z}, 字号 {fs:.0f}px")
    print(f"[OK] 插件页数据 plugins={stats['plugins']} seams={stats['seams']} "
          f"disabled={stats['disabled']} coreEdges={stats['coreEdges']} groupEdges={stats['groupEdges']}")
    print(f"[OK] 写出 {OUT} ({len(html_page.encode('utf-8'))} bytes) div {n_open}/{n_close}")


if __name__ == "__main__":
    main()
