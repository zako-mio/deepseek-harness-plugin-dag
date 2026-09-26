#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
0927-dsh-plugin-dag-017rc2 · 只读原型 demo 生成器
产出: <repo>/09-prototype/grid.html  —— 「主 DAG 组级视图 · 新排布方案」评审用 demo

设计要点（与主 Agent 裁定契约一致）:
- 一级分区 = 固定功能簇表（F1..F10）所归属的 L1/L2/L3/EXT 区；EXT 独立最左一列
- 二级功能簇 = F1..F10（固定表，断言恰好覆盖 50 组 + EXT，无遗漏无重复）
- 布局: cytoscape layout:'preset' —— 坐标全部在 Python 侧算好写入元素 position，渲染零随机
- 组间边: 由 webapp-dag.json 的 edges 推导（跨组去重，218 条）+ EXT 组级边（46 条）= 264 条
- 组配色: 与生产 04-interactive/index.html 的 DATA.groupColor 完全一致（palette 循环取色，
  50 组按 group id 升序），生成时对生产值做 0 差异断言

本脚本只读 01-dag-data/*, 04-interactive/index.html（用于配色一致性核对）；只写 <repo>/09-prototype/grid.html
"""
import json, os, sys, math, collections

sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(SCRIPT_DIR))          # <repo>
DAG_P = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
EXT_P = os.path.join(BASE, "01-dag-data", "external-seams.json")
PROD_P = os.path.join(BASE, "04-interactive", "index.html")
OUT = os.path.join(BASE, "09-prototype", "grid.html")

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

# ---------------------------------------------------------------- 读数据
with open(DAG_P, encoding="utf-8") as f:
    dag = json.load(f)
with open(EXT_P, encoding="utf-8") as f:
    ext = json.load(f)

nodes = {n["id"]: n for n in dag["nodes"]}
groups = {g["id"]: g for g in dag["groups"]}
seams = ext["seams"]
N_SEAMS = len(seams)

# ---------------- 自检 1: 功能簇表恰好覆盖 50 组 + EXT，无遗漏无重复 ----------------
all_gids = set(groups.keys())
listed = []
for cid, cname, zone, gids in CLUSTERS:
    listed.extend(gids)
assert len(listed) == len(set(listed)), "功能簇表存在重复组"
assert set(listed) == all_gids, f"功能簇表覆盖不符: 缺 {sorted(all_gids - set(listed))} / 多 {sorted(set(listed) - all_gids)}"
assert len(all_gids) == 50, f"组数应为 50, 实为 {len(all_gids)}"
n_ext_cluster = sum(1 for c in CLUSTERS if c[3] == [])
assert n_ext_cluster == 1, "EXT 功能簇应恰好 1 个"
print(f"[OK] 功能簇表覆盖 50 组 + EXT：{'/'.join(c[0] for c in CLUSTERS)}")

# ---------------- 组配色: 与生产一致 ----------------
PALETTE = ["#4f8cff", "#7b61ff", "#2fb98a", "#e8933b", "#e05563", "#3b9fe0", "#9a7bf0", "#e0a03b",
           "#3bc4a0", "#d0546b", "#6c8df5", "#b48a3c", "#54a0e8", "#8a5cf0", "#3ab7c4", "#e07b54",
           "#5f8de0", "#9b6bd4", "#4aa8a0", "#d06a4a", "#6b9bd4", "#b07bd4", "#4ac48e", "#d48a5b",
           "#e8a13b", "#6b8fe8", "#3bc48a", "#d07bd4", "#4f8ce8",
           "#c44f6e", "#4f9ce8", "#8a7bf0", "#2fbfa0", "#e0a03b", "#d46b54", "#6b8fe8", "#a05be0"]
gids_sorted = sorted(groups.keys())
GROUP_COLOR = {g: PALETTE[i % len(PALETTE)] for i, g in enumerate(gids_sorted)}
EXT_COLOR = "#b48a3c"

# 与生产 DATA.groupColor 做零差异核对（只读）
prod_mismatch = -1
if os.path.exists(PROD_P):
    try:
        s = open(PROD_P, encoding="utf-8").read()
        i = s.find("const DATA = ")
        j = s.find("\n", i)
        prod = json.loads(s[i + len("const DATA = "):j].rstrip(";").strip())
        pc = prod.get("groupColor", {})
        prod_mismatch = sum(1 for g in gids_sorted if pc.get(g) != GROUP_COLOR[g])
    except Exception as e:  # pragma: no cover
        print(f"[WARN] 生产配色核对失败: {e}")
print(f"[OK] 组配色 vs 生产 04-interactive groupColor 差异数 = {prod_mismatch}")

# ---------------- 组聚合: 插件数 / 平均 layer / 主导装配来源 ----------------
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

# ---------------- 列构建 ----------------
def cluster_sorted_gids(gids):
    return sorted(gids, key=lambda g: (GSTAT[g][1], g))

columns = []   # dict: cid, cname, zone, gids, sub
for zone in ZONE_ORDER:
    for cid, cname, czone, gids in CLUSTERS:
        if czone != zone:
            continue
        ordered = cluster_sorted_gids(gids)
        if len(ordered) > 10:
            half = math.ceil(len(ordered) / 2)
            chunks = [ordered[:half], ordered[half:]]
        else:
            chunks = [ordered] if ordered else [[]]
        # EXT 簇: 单节点（无插件组）→ 用一个占位 gid 'EXT'
        if cid == "F10":
            chunks = [["EXT"]]
        for si, ch in enumerate(chunks):
            columns.append({"cid": cid, "cname": cname, "zone": czone,
                            "gids": ch, "sub": si, "nsub": len(chunks)})

# ---------------- 尺寸参数 + 收敛（先缩列间距 → 后缩节点宽 → 最后缩行距） ----------------
NODE_W, NODE_H = 110, 46
ROW_GAP = 18
COL_GAP, CLUSTER_GAP, ZONE_GAP = 26, 36, 60
CLUSTER_TITLE_H, ZONE_TITLE_H = 20, 26
TARGET_W, TARGET_H = 1470, 860   # 内部目标: 略严于 1560, 保证侧栏展开时 fit-zoom ≥ 0.85


def gap_for(idx):
    if idx == 0:
        return None
    prev, cur = columns[idx - 1], columns[idx]
    if cur["cid"] == prev["cid"]:
        return "col"
    if cur["zone"] == prev["zone"]:
        return "cluster"
    return "zone"


def compute_width(cg, clg, zg, nw):
    gaps = {"col": cg, "cluster": clg, "zone": zg}
    lefts = [0.0]
    for i in range(1, len(columns)):
        lefts.append(lefts[-1] + nw + gaps[gap_for(i)])
    return lefts, lefts[-1] + nw


def col_height(n):
    return CLUSTER_TITLE_H + n * NODE_H + max(0, n - 1) * ROW_GAP


scale = 1.0
lefts, width = compute_width(COL_GAP, CLUSTER_GAP, ZONE_GAP, NODE_W)
if width > TARGET_W:                                  # 阶段1: 缩列间距
    while width > TARGET_W and scale > 0.30:
        scale -= 0.005
        cg = max(12.0, COL_GAP * scale)
        clg = max(14.0, CLUSTER_GAP * scale)
        zg = max(20.0, ZONE_GAP * scale)
        lefts, width = compute_width(cg, clg, zg, NODE_W)
    COL_GAP, CLUSTER_GAP, ZONE_GAP = round(cg), round(clg), round(zg)
    lefts, width = compute_width(COL_GAP, CLUSTER_GAP, ZONE_GAP, NODE_W)
if width > TARGET_W:                                  # 阶段2: 缩节点宽 (≥104)
    while width > TARGET_W and NODE_W > 104:
        NODE_W -= 1
        lefts, width = compute_width(COL_GAP, CLUSTER_GAP, ZONE_GAP, NODE_W)
if width > TARGET_W:                                  # 阶段3: 缩行距 (≥14)
    while width > TARGET_W and ROW_GAP > 14:
        ROW_GAP -= 1
        lefts, width = compute_width(COL_GAP, CLUSTER_GAP, ZONE_GAP, NODE_W)

max_col_h = max(col_height(len(c["gids"])) for c in columns)
content_h = ZONE_TITLE_H + max_col_h
print(f"[OK] 最终尺寸参数: node={NODE_W}x{NODE_H} row_gap={ROW_GAP} col_gap={COL_GAP} "
      f"cluster_gap={CLUSTER_GAP} zone_gap={ZONE_GAP}")
print(f"[OK] 内容包围盒: 宽 {width:.0f} x 高 {content_h:.0f} (目标 ≤{TARGET_W}x{TARGET_H})")
assert width <= 1560, f"内容宽 {width} 超上限 1560"
assert content_h <= 860, f"内容高 {content_h} 超上限 860"

# ---------------- 节点坐标（preset，零随机） ----------------
positions = {}
for i, col in enumerate(columns):
    cx = lefts[i] + NODE_W / 2.0
    y0 = ZONE_TITLE_H + CLUSTER_TITLE_H + NODE_H / 2.0
    for r, gid in enumerate(col["gids"]):
        positions[gid] = (round(cx, 2), round(y0 + r * (NODE_H + ROW_GAP), 2))
    col["x1"] = round(lefts[i], 2)
    col["x2"] = round(lefts[i] + NODE_W, 2)

# ---------------- 覆盖度/重叠自检 ----------------
assert set(positions.keys()) == all_gids | {"EXT"}, "坐标未覆盖全部 50 组 + EXT"
print(f"[OK] 节点数 = {len(positions)} (50 组 + EXT)")

min_gap = 1e9
ids = list(positions.keys())
for a in range(len(ids)):
    for b in range(a + 1, len(ids)):
        xa, ya = positions[ids[a]]
        xb, yb = positions[ids[b]]
        dx, dy = abs(xa - xb), abs(ya - yb)
        if dx < NODE_W - 0.01 and dy < NODE_H - 0.01:
            raise AssertionError(f"组坐标重叠: {ids[a]} vs {ids[b]}")
        d = math.hypot(dx, dy)
        min_gap = min(min_gap, d)
print(f"[OK] 组坐标无两两重叠; 最近节点中心距 = {min_gap:.2f}")

# ---------------- 边: 264 条组间边 ----------------
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
print(f"[OK] 组间边 = {len(edge_pairs)} (非EXT {non_ext_pairs} + EXT {len(ext_pairs)})")
assert len(edge_pairs) == 264, f"组间边应为 264, 实为 {len(edge_pairs)}"

# ---------------- 组装 cytoscape 元素 ----------------
node_els = []
tree = []
node_by_gid = {}
for gid in gids_sorted:
    name = groups[gid]["name"]
    cnt, avg, asm = GSTAT[gid]
    x, y = positions[gid]
    label = name + "\n" + gid + " · " + str(cnt)
    nd = {"data": {"id": "grp-" + gid, "label": label, "kind": "group", "group": gid,
                   "gname": name, "count": cnt, "asm": asm, "avg_layer": round(avg, 2),
                   "color": GROUP_COLOR[gid]},
          "position": {"x": x, "y": y}}
    node_els.append(nd)
    node_by_gid[gid] = nd["data"]

ex, ey = positions["EXT"]
node_els.append({"data": {"id": "grp-EXT", "label": "外部基座 seam\nEXT · " + str(N_SEAMS),
                          "kind": "ext", "group": "EXT", "gname": "外部基座 seam",
                          "count": N_SEAMS, "asm": "vendor", "color": EXT_COLOR},
                 "position": {"x": ex, "y": ey}})
node_by_gid["EXT"] = node_els[-1]["data"]

edge_els = []
for gs, gt in edge_pairs:
    edge_els.append({"data": {"id": "grp-%s->grp-%s" % (gs, gt),
                              "source": "grp-" + gs, "target": "grp-" + gt}})

# 侧栏三级树
zi = 0
for zone in ZONE_ORDER:
    zclusters = []
    for col in columns:
        if col["zone"] != zone:
            continue
        item = {"id": col["cid"], "name": col["cname"], "count": len(col["gids"]),
                "groups": []}
        for gid in col["gids"]:
            d = node_by_gid[gid]
            item["groups"].append({"gid": gid, "name": d["gname"], "count": d["count"],
                                   "asm": d["asm"], "color": d["color"], "sub": col["sub"]})
        # 同簇子列合并展示
        merged = next((c for c in zclusters if c["id"] == col["cid"]), None)
        if merged:
            merged["groups"].extend(item["groups"])
        else:
            zclusters.append(item)
    zc = sum(c["count"] for c in zclusters)
    tree.append({"zone": zone, "count": zc, "clusters": zclusters})

zones_ov = []
for zone in ZONE_ORDER:
    cols = [c for c in columns if c["zone"] == zone]
    zones_ov.append({"name": zone, "count": sum(len(c["gids"]) for c in cols),
                     "x1": min(c["x1"] for c in cols), "x2": max(c["x2"] for c in cols)})
clusters_ov = [{"id": c["cid"], "name": c["cname"], "zone": c["zone"],
                "count": len(c["gids"]), "x1": c["x1"], "x2": c["x2"]} for c in columns]

payload = {
    "nodes": node_els,
    "edges": edge_els,
    "tree": tree,
    "overlay": {"zones": zones_ov, "clusters": clusters_ov,
                "zoneTitleH": ZONE_TITLE_H, "clusterTitleH": CLUSTER_TITLE_H,
                "contentH": round(content_h, 2)},
    "layout": {"nodeW": NODE_W, "nodeH": NODE_H, "width": round(width, 2),
               "height": round(content_h, 2),
               "bboxPad": 16},
    "stats": {"groups": 50, "nodes": len(node_els), "edges": len(edge_els),
              "seams": N_SEAMS, "nonExtEdges": non_ext_pairs, "extEdges": len(ext_pairs)},
}

# ---------------------------------------------------------------- HTML 模板
TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>主 DAG 组级视图 · 新排布方案 demo（只读原型）</title>
<style>
  :root { --bg:#0f1117; --panel:#161a22; --border:#2a2f3a; --text:#e6e8ee; --dim:#9aa3b2; --accent:#4f8cff; --warn:#e0b25e; --pb:34px; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,sans-serif; height:100vh; overflow:hidden; }
  .proto-banner { position:fixed; top:0; left:0; right:0; height:var(--pb); z-index:30; background:#3a2f1a;
                  color:var(--warn); border-bottom:1px solid #4a3a15; font-size:12.5px;
                  display:flex; align-items:center; justify-content:center; gap:6px; }
  .proto-banner a { color:#ffd08a; text-decoration:underline; }
  header { position:fixed; top:var(--pb); left:0; right:0; height:56px; z-index:10; background:var(--panel);
           border-bottom:1px solid var(--border); padding:10px 16px; display:flex; align-items:center; gap:12px; flex-wrap:wrap; }
  header h1 { font-size:15px; font-weight:600; white-space:nowrap; }
  .badge { background:#20324f; color:#7fb0ff; padding:2px 9px; border-radius:20px; font-size:11px; white-space:nowrap; }
  .badge.demo { background:#3a2f1a; color:var(--warn); }
  header a { color:var(--accent); text-decoration:none; font-size:12px; white-space:nowrap; }
  header a:hover { text-decoration:underline; }
  header button { background:#20324f; color:#7fb0ff; border:1px solid #2a3a55; border-radius:20px;
                  padding:4px 12px; font-size:12px; cursor:pointer; white-space:nowrap; }
  header button:hover { background:#28406a; }
  .hint { color:var(--dim); font-size:11px; }
  /* 侧栏默认留位 300px —— 修掉生产页 right:0 遮挡 bug */
  #graph { position:fixed; top:calc(var(--pb) + 56px); left:0; right:300px; bottom:28px; background:transparent; }
  #overlay { position:fixed; top:calc(var(--pb) + 56px); left:0; pointer-events:none; z-index:8; }
  #side { position:fixed; right:0; top:calc(var(--pb) + 56px); bottom:28px; width:300px; background:var(--panel);
          border-left:1px solid var(--border); padding:12px; overflow:auto; z-index:9; }
  #side h2 { font-size:12px; margin:10px 0 6px; color:var(--dim); letter-spacing:.05em; }
  .znode { font-size:12px; font-weight:700; color:#c8d4eb; margin:8px 0 4px; padding:4px 6px;
           background:#1b2130; border-radius:4px; }
  .cnode { font-size:11px; color:#9fb0cc; margin:6px 0 3px 4px; }
  .gitem { display:flex; align-items:center; gap:6px; font-size:11px; color:var(--dim);
           padding:3px 6px; border-radius:4px; cursor:pointer; margin-left:8px; }
  .gitem:hover { background:#22304a; color:var(--text); }
  .gitem .sw { width:11px; height:11px; border-radius:2px; flex:0 0 auto; }
  .gitem .gid { color:#7f8ea8; font-family:ui-monospace,monospace; }
  .gitem .asm { margin-left:auto; background:#243040; color:#8fb0e0; border-radius:9px;
                padding:0 6px; font-size:10px; }
  #note { position:fixed; top:calc(var(--pb) + 64px); right:312px; z-index:11; max-width:360px; font-size:11px;
          color:var(--warn); background:#241d0e; border:1px solid #4a3a15; border-radius:6px;
          padding:6px 10px; line-height:1.5; }
  #status { position:fixed; left:0; right:0; bottom:0; height:28px; z-index:10; background:var(--panel);
            border-top:1px solid var(--border); display:flex; align-items:center; gap:18px;
            padding:0 16px; font-size:11px; color:var(--dim); }
  #status b { color:var(--text); }
</style>
</head>
<body>
<div class="proto-banner">本页为评审原型，非生产入口；生产入口见 <a href="../index.html">../index.html</a></div>
<header>
  <h1>主 DAG 组级视图 <span class="badge">新排布方案</span> <span class="badge demo">只读原型 demo</span></h1>
  <a href="../index.html">← 返回任务目录</a>
  <button id="backbtn">返回组级视图</button>
  <button id="togglebtn">折叠侧栏</button>
  <span class="hint">单击节点=高亮一跳邻域 · 双击节点=下钻(占位) · 悬停侧栏项=高亮 · 拖拽平移 / 滚轮缩放</span>
</header>
<div id="note">下钻视图：demo 未实现，待确认组级方案后再定</div>
<div id="side"></div>
<canvas id="overlay"></canvas>
<div id="graph"></div>
<div id="status">
  模式 <b id="s-mode">组级</b> · 节点 <b id="s-count">0</b> · zoom <b id="s-zoom">-</b> · 包围盒 <b id="s-bbox">-</b>
</div>

<script src="../04-interactive/vendor/cytoscape.min.js"></script>
<script>
const DATA = __DATA_JSON__;

const NODE_W = DATA.layout.nodeW, NODE_H = DATA.layout.nodeH;
const BASE_EDGE_OP = 0.12, DIM_NODE_OP = 0.15, DIM_EDGE_OP = 0.05;

const cy = cytoscape({
  container: document.getElementById('graph'),
  elements: DATA.nodes.concat(DATA.edges),
  style: [
    { selector:'node', style:{
        label:'data(label)', 'text-valign':'center', 'text-halign':'center',
        color:'#ffffff', 'font-size':9, 'text-wrap':'wrap', 'text-max-width':100
    }},
    { selector:'node[kind="group"]', style:{
        'background-color':'data(color)', width:NODE_W, height:NODE_H, shape:'round-rectangle',
        'border-width':2.5, 'border-color':'rgba(255,255,255,0.55)'
    }},
    { selector:'node[kind="ext"]', style:{
        'background-color':'data(color)', width:NODE_W, height:NODE_H, shape:'round-rectangle',
        'border-width':3, 'border-color':'#e0b25e'
    }},
    { selector:'edge', style:{
        'curve-style':'straight', 'line-color':'#6a7488', 'target-arrow-color':'#6a7488',
        width:1, 'target-arrow-shape':'triangle', 'arrow-scale':0.6, opacity:BASE_EDGE_OP
    }}
  ],
  layout: { name:'preset' },
  wheelSensitivity: 0.3, minZoom: 0.1, maxZoom: 4
});
window.__cy = cy;
window.__layout = DATA.layout;
window.__stats = DATA.stats;

// ---------------- 侧栏三级列表 ----------------
const side = document.getElementById('side');
DATA.tree.forEach(function(zn){
  const h = document.createElement('div');
  h.className = 'znode';
  h.textContent = zn.zone + ' 区 · ' + zn.count + ' 组';
  side.appendChild(h);
  zn.clusters.forEach(function(cl){
    const ch = document.createElement('div');
    ch.className = 'cnode';
    ch.textContent = cl.id + ' ' + cl.name + ' · ' + cl.count + ' 组';
    side.appendChild(ch);
    cl.groups.forEach(function(g){
      const d = document.createElement('div');
      d.className = 'gitem';
      d.dataset.gid = g.gid;
      d.innerHTML = '<span class="sw" style="background:' + g.color + '"></span>'
        + '<span>' + g.name + '</span>'
        + '<span class="gid">' + g.gid + '</span>'
        + '<span class="gid">' + g.count + ' 插件</span>'
        + '<span class="asm">' + g.asm + '</span>';
      d.addEventListener('mouseenter', function(){ highlightNode(cy.getElementById('grp-' + g.gid)); });
      d.addEventListener('mouseleave', clearHighlight);
      d.addEventListener('click', function(){
        const n = cy.getElementById('grp-' + g.gid);
        highlightNode(n);
        cy.animate({ center:{ eles:n }, zoom: Math.max(cy.zoom(), 0.95) }, { duration:400 });
        setMode(g.gid + ' · ' + g.name);
      });
      side.appendChild(d);
    });
  });
});

// ---------------- 高亮 / 恢复 ----------------
function clearHighlight(){
  cy.nodes().style('opacity', 1);
  cy.edges().style('opacity', BASE_EDGE_OP).style('width', 1);
}
function highlightNode(n){
  if (!n || n.length === 0) return;
  clearHighlight();
  const nbh = n.closedNeighborhood();
  cy.nodes().not(nbh.nodes()).style('opacity', DIM_NODE_OP);
  nbh.nodes().style('opacity', 1);
  const inc = n.connectedEdges();
  cy.edges().not(inc).style('opacity', DIM_EDGE_OP).style('width', 1);
  inc.style('opacity', 0.9).style('width', 1.8);
}
cy.on('mouseover', 'node', function(evt){ highlightNode(evt.target); });
cy.on('mouseout', 'node', function(){ clearHighlight(); });
cy.on('tap', 'node', function(evt){ highlightNode(evt.target); });
cy.on('dbltap', 'node', function(evt){
  const g = evt.target.data('gname');
  window.alert('下钻视图：demo 未实现，待确认组级方案后再定\n\n（目标：' + g + '）');
});
cy.on('tap', function(evt){ if (evt.target === cy) { clearHighlight(); setMode('组级'); } });

// ---------------- overlay: 区带 / 区标题 / 簇标题（确定性坐标随 cy 变换重绘） ----------------
const canvas = document.getElementById('overlay');
const octx = canvas.getContext('2d');
let dpr = window.devicePixelRatio || 1;
function sizeCanvas(){
  // <canvas> 是 replaced element: left/right 撑不开, 必须按容器显式设定尺寸
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
  const mx = function(x){ return x * z + pan.x; };
  const my = function(y){ return y * z + pan.y; };
  DATA.overlay.zones.forEach(function(zn){
    const x1 = mx(zn.x1) - 7, x2 = mx(zn.x2) + 7;
    const y1 = my(0), y2 = my(DATA.overlay.contentH);
    octx.fillStyle = 'rgba(255,255,255,0.025)';
    octx.fillRect(x1, y1, x2 - x1, y2 - y1);
    octx.strokeStyle = 'rgba(255,255,255,0.10)';
    octx.strokeRect(x1, y1, x2 - x1, y2 - y1);
    octx.fillStyle = 'rgba(205,216,238,0.95)';
    octx.font = 'bold 13px system-ui,sans-serif';
    octx.textAlign = 'center';
    octx.textBaseline = 'middle';
    octx.fillText(zn.name + ' 区 · ' + zn.count + ' 组', (x1 + x2) / 2, my(DATA.overlay.zoneTitleH / 2));
  });
  DATA.overlay.clusters.forEach(function(cl){
    const cx = (mx(cl.x1) + mx(cl.x2)) / 2;
    octx.fillStyle = cl.zone === 'EXT' ? 'rgba(224,178,94,0.92)' : 'rgba(155,172,200,0.92)';
    octx.font = '11px system-ui,sans-serif';
    octx.textAlign = 'center';
    octx.textBaseline = 'middle';
    octx.fillText(cl.name + ' · ' + cl.count, cx, my(DATA.overlay.zoneTitleH + DATA.overlay.clusterTitleH / 2));
  });
}
function refreshOverlay(){ sizeCanvas(); drawOverlay(); }
cy.on('pan zoom resize', drawOverlay);

// ---------------- fit (侧栏展开 ≥0.85; 折叠 ≈1.0) ----------------
function fitClamped(pad){
  cy.fit(cy.elements(), pad);
  if (cy.zoom() > 1){ cy.zoom(1); cy.center(); }
  else if (cy.zoom() < 0.85){ cy.zoom(0.85); cy.center(); }
}
fitClamped(DATA.layout.bboxPad);
refreshOverlay();

// ---------------- 侧栏折叠 ----------------
let collapsed = false;
const graphEl = document.getElementById('graph');
function setSidebar(){
  document.getElementById('side').style.display = collapsed ? 'none' : 'block';
  graphEl.style.right = collapsed ? '0px' : '300px';
  document.getElementById('note').style.right = collapsed ? '12px' : '312px';
  document.getElementById('togglebtn').textContent = collapsed ? '展开侧栏' : '折叠侧栏';
  cy.resize();
  setTimeout(function(){ fitClamped(DATA.layout.bboxPad); refreshOverlay(); }, 30);
}
document.getElementById('togglebtn').addEventListener('click', function(){ collapsed = !collapsed; setSidebar(); });
document.getElementById('backbtn').addEventListener('click', function(){
  clearHighlight(); setMode('组级'); fitClamped(DATA.layout.bboxPad); refreshOverlay();
});
window.addEventListener('resize', function(){ cy.resize(); refreshOverlay(); });

// ---------------- 状态栏 ----------------
function setMode(t){ document.getElementById('s-mode').textContent = t; }
function updateStatus(){
  document.getElementById('s-count').textContent = cy.nodes().length;
  document.getElementById('s-zoom').textContent = cy.zoom().toFixed(2);
  const bb = cy.elements().boundingBox();
  document.getElementById('s-bbox').textContent = Math.round(bb.w) + ' x ' + Math.round(bb.h);
}
cy.on('zoom pan', updateStatus);
setMode('组级');
updateStatus();
</script>
</body>
</html>
"""

html_out = TEMPLATE.replace("__DATA_JSON__", json.dumps(payload, ensure_ascii=False))

# ---------------- 产物自检: UTF-8 / 替换字符 / div 配平 ----------------
assert "\ufffd" not in html_out, "产物含替换字符 U+FFFD"
n_open = html_out.count("<div")
n_close = html_out.count("</div>")
assert n_open == n_close, f"div 不配平: open={n_open} close={n_close}"
with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(html_out)

print(f"[OK] 写出 {OUT} ({len(html_out.encode('utf-8'))} bytes)  div open/close = {n_open}/{n_close}")
print(f"[OK] 节点={len(node_els)} 边={len(edge_els)} 侧栏区={len(tree)} 簇列={len(clusters_ov)}")
