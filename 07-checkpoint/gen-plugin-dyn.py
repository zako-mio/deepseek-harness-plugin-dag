#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S4b L3 插件页动态 DAG 内嵌增强脚本:
在每个插件页 <h2>② 注册/提供</h2> 之前插入:
  1. cytoscape vendor 引用 (../04-interactive/vendor/)
  2. 深色主题动态 DAG 容器 + 渲染脚本 (插件 + 上游/下游节点)
- 数据从 webapp-dag.json 读取 (与 gen-html-l3.py 同源)
- 深色配色与插件页 CSS 变量一致 (--panel/--accent/--ext/--dis)
- 点击节点跳转对应页面
"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0819-plugin-dag-rc7"
DAG = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
EXT = os.path.join(BASE, "01-dag-data", "external-seams.json")
PAGES = os.path.join(BASE, "02-plugin-pages")
VENDOR_REL = "../04-interactive/vendor/"

with open(DAG, "r", encoding="utf-8") as f:
    dag = json.load(f)
with open(EXT, "r", encoding="utf-8") as f:
    ext = json.load(f)

nodes = {n["id"]: n for n in dag["nodes"]}
groups = {g["id"]: g for g in dag["groups"]}
ext_map = {e["id"]: e for e in ext["seams"]}

# 边索引
out_edges = {}
in_edges = {}
for nid in nodes:
    out_edges[nid] = []
    in_edges[nid] = []
for e in dag["edges"]:
    out_edges[e["from"]].append(e)
    in_edges[e["to"]].append(e)

# seam 被依赖
seam_dependents = {sid: s.get("referred_by", []) for sid, s in ext_map.items()}

# 深色主题 cytoscape 样式
DYN_CSS = """
<style>
#dyn-dag{width:100%;height:480px;background:var(--panel);border:1px solid var(--border);border-radius:8px;margin:12px 0;}
#dyn-dag-label{font-size:12px;color:var(--dim);margin:10px 0 4px;}
#dyn-dag-legend{display:flex;gap:16px;font-size:12px;color:var(--dim);margin:6px 0 2px;flex-wrap:wrap;}
#dyn-dag-legend .item{display:flex;align-items:center;gap:5px;}
#dyn-dag-legend .dot{width:10px;height:10px;border-radius:3px;display:inline-block;}
.dyn-self{background:var(--accent);}
.dyn-up{background:#e8933b;}
.dyn-down{background:#2fb98a;}
.dyn-seam{background:var(--ext);}
</style>
"""

DYN_HTML = """
<div id="dyn-dag-label">内部结构动态 DAG（深色主题：橙色=上游依赖 · 绿色=下游依赖 · 棕色=外部seam · 蓝=本插件）</div>
<div id="dyn-dag-legend">
  <span class="item"><span class="dot dyn-self"></span>本插件</span>
  <span class="item"><span class="dot dyn-up"></span>上游依赖</span>
  <span class="item"><span class="dot dyn-down"></span>下游依赖</span>
  <span class="item"><span class="dot dyn-seam"></span>外部 seam</span>
</div>
<div id="dyn-dag"></div>
"""

def dyn_script(nid):
    n = nodes[nid]
    ups = sorted(set(e["to"] for e in out_edges.get(nid, [])), key=lambda x: x)
    downs = sorted(set(e["from"] for e in in_edges.get(nid, [])), key=lambda x: x)
    ups = [u for u in ups if u in nodes or u in ext_map]
    downs = [d for d in downs if d in nodes]
    layer = n["layer"]

    # 构建 cytoscape elements
    # 颜色映射: cls 字段直接存颜色值 (cytoscape 'background-color': 'data(cls)')
    COLOR_SELF = "#4f8cff"   # 蓝: 本插件
    COLOR_UP = "#e8933b"     # 橙: 上游依赖
    COLOR_DOWN = "#2fb98a"   # 绿: 下游依赖
    COLOR_SEAM = "#b48a3c"   # 棕: 外部 seam
    elements = []
    def add_node(pid, kind, color):
        label = pid
        url = ""
        if pid in nodes:
            url = f"{pid}.html"
        elif pid in ext_map:
            url = f"../02-plugin-pages/{pid}.html"
        elements.append({
            "data": {"id": pid, "label": label, "kind": kind, "cls": color, "url": url}
        })
    # 本插件
    add_node(nid, "self", COLOR_SELF)
    # 上游
    for u in ups:
        k = "seam" if u in ext_map else "up"
        c = COLOR_SEAM if u in ext_map else COLOR_UP
        add_node(u, k, c)
    # 下游
    for d in downs:
        add_node(d, "down", COLOR_DOWN)

    # 边: 本插件 <- 上游 (上游 -> 本插件), 本插件 -> 下游
    edges = []
    for u in ups:
        edges.append({"data": {"id": f"{u}->{nid}", "source": u, "target": nid}})
    for d in downs:
        edges.append({"data": {"id": f"{nid}->{d}", "source": nid, "target": d}})

    data_json = json.dumps({"elements": elements + edges}, ensure_ascii=False)

    return f"""
<script src="{VENDOR_REL}cytoscape.min.js"></script>
<script src="{VENDOR_REL}cytoscape-dagre.min.js"></script>
<script>
(function(){{
  const raw = {data_json};
  const cy = cytoscape({{
    container: document.getElementById('dyn-dag'),
    elements: raw.elements,
    style: [
      {{
        selector: 'node',
        style: {{
          'label': 'data(label)',
          'background-color': 'data(cls)',
          'color': '#e6e8ee',
          'font-size': 11,
          'text-valign': 'bottom',
          'text-margin-y': 4,
          'width': 46,
          'height': 46,
          'shape': 'round-rectangle',
          'border-width': 2,
          'border-color': '#2a2f3a'
        }}
      }},
      {{
        selector: 'node[kind="self"]',
        style: {{
          'border-width': 3,
          'border-color': '#4f8cff',
          'width': 60,
          'height': 60,
          'font-size': 12,
          'font-weight': 700
        }}
      }},
      {{
        selector: 'edge',
        style: {{
          'width': 1.5,
          'line-color': '#4a5263',
          'target-arrow-color': '#4a5263',
          'target-arrow-shape': 'triangle',
          'curve-style': 'bezier'
        }}
      }}
    ],
    layout: {{
      name: 'dagre',
      rankDir: 'LR',
      nodeSep: 30,
      rankSep: 60,
      padding: 20
    }},
    wheelSensitivity: 0.2,
    minZoom: 0.2,
    maxZoom: 2.5
  }});
  cy.on('tap', 'node', (evt) => {{
    const url = evt.target.data('url');
    if (url) window.location.href = url;
  }});
  // 等渲染完自适应容器尺寸
  setTimeout(() => cy.resize(), 100);
}})();
</script>
"""

# 修改每个插件页
count = 0
for nid in nodes:
    fp = os.path.join(PAGES, f"{nid}.html")
    if not os.path.exists(fp):
        print(f"[WARN] missing page: {nid}")
        continue
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()

    # 幂等: 已有 dyn-dag 则跳过
    if 'id="dyn-dag"' in content:
        count += 1
        continue

    # 插入点: <h2>② 注册/提供（provides）</h2>
    marker = '<h2>② 注册/提供（provides）</h2>'
    insert_block = DYN_CSS + DYN_HTML + dyn_script(nid) + marker
    if marker in content:
        content = content.replace(marker, insert_block, 1)
    else:
        print(f"[WARN] marker not found in {nid}, skip")
        continue

    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    count += 1

print(f"[OK] 插件页动态 DAG 内嵌: {count} 页 (共 {len(nodes)})")
