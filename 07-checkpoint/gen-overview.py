#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S4b 总览页生成: 04-interactive/index.html
cytoscape 数据驱动交互图: 112 节点(76核心+36外部seam) + 194核心边 + 外部seam边
缩放联动: 缩小到组级显示组节点, 放大显示插件节点; 点击节点跳转插件页
"""
import json, os, html

BASE = r"D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag"
DAG = os.path.join(BASE, "01-dag-data", "core-dag.json")
EXT = os.path.join(BASE, "01-dag-data", "external-seams.json")
OUT = os.path.join(BASE, "04-interactive", "index.html")

with open(DAG, "r", encoding="utf-8") as f:
    dag = json.load(f)
with open(EXT, "r", encoding="utf-8") as f:
    ext = json.load(f)

nodes = {n["id"]: n for n in dag["nodes"]}
groups = {g["id"]: g for g in dag["groups"]}
edges = dag["edges"]
ext_map = {e["id"]: e for e in ext["seams"]}

# 组配色
GROUP_COLORS = {}
palette = ["#4f8cff","#7b61ff","#2fb98a","#e8933b","#e05563","#3b9fe0","#9a7bf0","#e0a03b",
           "#3bc4a0","#d0546b","#6c8df5","#b48a3c","#54a0e8","#8a5cf0","#3ab7c4","#e07b54",
           "#5f8de0","#9b6bd4","#4aa8a0","#d06a4a","#6b9bd4","#b07bd4","#4ac48e","#d48a5b"]
gids = sorted(groups.keys())
for i, gid in enumerate(gids):
    GROUP_COLORS[gid] = palette[i % len(palette)]

# 插件数据 JSON 注入
plugin_nodes = []
for nid, n in nodes.items():
    gid = n["group"]
    plugin_nodes.append({
        "data": {
            "id": nid, "label": nid, "kind": "plugin", "group": gid,
            "gname": n["group_name"], "layer": n["layer"], "url": f"../02-plugin-pages/{nid}.html"
        }
    })

ext_nodes = []
for sid, s in ext_map.items():
    ext_nodes.append({
        "data": {
            "id": sid, "label": sid, "kind": "seam", "group": "EXT",
            "gname": "外部基座seam", "layer": 0, "url": f"../02-plugin-pages/{sid}.html"
        }
    })

edge_list = []
for e in edges:
    edge_list.append({"data": {"id": f"{e['from']}->{e['to']}", "source": e["from"], "target": e["to"], "kind": "core"}})

# 外部 seam 边: 核心插件 -> 外部 seam (核心依赖外部)
for sid, s in ext_map.items():
    for dep in s.get("referred_by", []):
        if dep in nodes:
            edge_list.append({"data": {"id": f"{dep}->{sid}", "source": dep, "target": sid, "kind": "seam"}})

# 组聚合边 (组级视图)
group_edges = []
for e in edges:
    gs = nodes[e["from"]]["group"]
    gt = nodes[e["to"]]["group"]
    if gs != gt:
        key = f"grp-{gs}->grp-{gt}"
        if not any(ge["data"]["id"] == key for ge in group_edges):
            group_edges.append({"data": {"id": key, "source": "grp-"+gs, "target": "grp-"+gt, "kind": "group"}})
# 外部 seam 也聚合到 EXT 组
for sid, s in ext_map.items():
    for dep in s.get("referred_by", []):
        if dep in nodes:
            gs = nodes[dep]["group"]
            key = f"grp-{gs}->grp-EXT"
            if not any(ge["data"]["id"] == key for ge in group_edges):
                group_edges.append({"data": {"id": key, "source": "grp-"+gs, "target": "grp-EXT", "kind": "group"}})

payload = {
    "plugins": plugin_nodes,
    "seams": ext_nodes,
    "edges": edge_list,
    "groupEdges": group_edges,
    "groups": {gid: {"name": g["name"], "color": GROUP_COLORS[gid]} for gid, g in groups.items()},
    "groupColor": GROUP_COLORS,
    "extColor": "#b48a3c"
}

html_page = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DeepSeek Harness 插件 DAG 交互总览</title>
<style>
  :root { --bg:#0f1117; --panel:#161a22; --border:#2a2f3a; --text:#e6e8ee; --dim:#9aa3b2; --accent:#4f8cff; --ext:#b48a3c; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:var(--bg); color:var(--text); font-family:'Segoe UI',system-ui,sans-serif; height:100vh; overflow:hidden; }
  header { position:fixed; top:0; left:0; right:0; z-index:10; background:var(--panel); border-bottom:1px solid var(--border); padding:10px 20px; display:flex; align-items:center; gap:16px; flex-wrap:wrap; }
  header h1 { font-size:16px; font-weight:600; }
  .badge { background:#20324f; color:#7fb0ff; padding:2px 10px; border-radius:20px; font-size:12px; }
  .badge.ext { background:#3a2f1a; color:#e0b25e; }
  header a { color:var(--accent); text-decoration:none; font-size:13px; }
  header a:hover { text-decoration:underline; }
  .hint { color:var(--dim); font-size:12px; }
  #graph { position:fixed; top:56px; left:0; right:0; bottom:0; }
  #side { position:fixed; right:0; top:56px; bottom:0; width:300px; background:var(--panel); border-left:1px solid var(--border); padding:16px; overflow:auto; z-index:9; }
  #side h2 { font-size:14px; margin-bottom:10px; color:var(--dim); }
  #side .legend { font-size:12px; color:var(--dim); line-height:1.8; }
  #side .legend b { color:var(--text); }
  #zoominfo { position:fixed; bottom:14px; left:20px; background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:8px 14px; font-size:12px; color:var(--dim); z-index:9; }
  #zoominfo b { color:var(--text); }
</style>
</head>
<body>
<header>
  <h1>DeepSeek Harness 插件 DAG <span class="badge">交互总览</span></h1>
  <a href="../index.html">← 返回任务目录</a>
  <a href="../03-groups/index.html">组目录</a>
  <span class="badge ext">外部 seam 基座</span>
  <span class="hint">滚轮缩放：放大→插件节点；缩小→组节点。拖拽平移。点击节点→跳转插件页。</span>
</header>
<div id="side">
  <h2>图例</h2>
  <div class="legend">
    <b>插件节点</b>（76 个核心插件）<br>
    <b>外部 seam 节点</b>（36 个基座包）<br>
    <b>依赖边</b>：A → B 表示 A 依赖 B<br>
    <b>缩放</b>：k≥1 显示插件；k&lt;1 聚合为组<br><br>
    组：运行时框架/类型契约/核心服务/LLM域/文件系统/Shell/沙箱/审批/命令/凭据/附件/作业/目标/技能/子代理/工作流/上下文治理/Web 等 24 组
  </div>
  <h2 style="margin-top:14px;">组配色</h2>
  <div id="glegend"></div>
</div>
<div id="zoominfo">缩放 <b id="zval">1.00</b> · 模式 <b id="zmode">插件级</b> · 节点 <b id="zcount">0</b></div>
<div id="graph"></div>

<script src="vendor/cytoscape.min.js"></script>
<script>
const DATA = __DATA__;

// ---- 构建元素 ----
function buildElements(mode){
  if (mode === 'plugin'){
    const nodes = DATA.plugins.concat(DATA.seams);
    return { nodes, edges: DATA.edges };
  }
  // group 模式: 24 组 + EXT
  const gids = Object.keys(DATA.groups);
  const nodes = gids.map(g => ({
    data:{ id:'grp-'+g, label: DATA.groups[g].name, kind:'group', group:g, gname:DATA.groups[g].name }
  }));
  nodes.push({ data:{ id:'grp-EXT', label:'外部基座seam', kind:'group', group:'EXT', gname:'外部基座seam' } });
  return { nodes, edges: DATA.groupEdges };
}

const cy = cytoscape({
  container: document.getElementById('graph'),
  elements: buildElements('plugin'),
  style: [
    { selector:'node', style:{
      label:'data(label)', 'text-valign':'center','text-halign':'center', color:'#fff',
      'font-size':9, 'text-wrap':'wrap', 'text-max-width':90
    }},
    { selector:'node.plugin', style:{
      'background-color': function(ele){ return DATA.groupColor[ele.data('group')] || '#2b3550'; },
      'border-width':1.5,'border-color':'rgba(255,255,255,0.35)','width':56,'height':30, shape:'round-rectangle'
    }},
    { selector:'node.seam', style:{
      'background-color':'#3a2f1a','border-width':1.5,'border-color':'#8a6a30',
      'width':52,'height':28, shape:'round-rectangle'
    }},
    { selector:'node.group', style:{
      'background-color': function(ele){ return ele.data('group')==='EXT' ? '#3a2f1a' : (DATA.groupColor[ele.data('group')] || '#243040'); },
      'border-width':3,'border-color':'rgba(255,255,255,0.5)','width':130,'height':46,'font-size':13
    }},
    { selector:'edge', style:{
      'curve-style':'bezier','target-arrow-shape':'triangle','arrow-scale':0.7,
      'line-color':'#4a5265','target-arrow-color':'#4a5265','width':1.1
    }},
    { selector:'edge.seam', style:{ 'line-color':'#8a6a30','target-arrow-color':'#8a6a30','width':1.2, 'line-style':'dashed' } }
  ],
  layout: { name:'dagre', rankDir:'LR', nodeSep:36, rankSep:60, padding:40 },
  wheelSensitivity: 0.2,
  minZoom: 0.15,
  maxZoom: 3.5,
});

function modeFromZoom(k){ return k >= 0.9 ? 'plugin' : 'group'; }

function refresh(){
  const k = cy.zoom();
  const mode = modeFromZoom(k);
  document.getElementById('zval').textContent = k.toFixed(2);
  document.getElementById('zmode').textContent = mode === 'plugin' ? '插件级' : '组级';
  document.getElementById('zcount').textContent = cy.nodes().length;
  // 模式切换时重建
  const first = cy.nodes().first();
  const curKind = first ? first.data('kind') : null;
  if ((mode === 'plugin' && curKind !== 'plugin' && curKind !== 'seam') ||
      (mode === 'group' && curKind === 'plugin')){
    const pos = cy.pan();
    const zoom = cy.zoom();
    cy.elements().remove();
    const els = buildElements(mode);
    cy.add(els.nodes);
    cy.add(els.edges);
    cy.layout({ name:'dagre', rankDir:'LR', nodeSep:36, rankSep:60, padding:40 }).run();
    cy.zoom({ level: zoom, position: pos });
  }
}

cy.on('zoom', refresh);
cy.on('tap', 'node', (evt) => {
  const n = evt.target;
  const url = n.data('url');
  if (url) window.location.href = url;
  else {
    // 组节点: 放大到插件级并聚焦该组
    const g = n.data('group');
    const members = cy.$('node[group="' + g + '"]');
    if (members.length) { cy.animate({ fit:{ eles: members, padding: 60 }, duration: 400 }); }
  }
});

// 组配色图例
const gl = document.getElementById('glegend');
Object.keys(DATA.groups).forEach(g => {
  const d = document.createElement('div');
  d.style.cssText = 'display:flex;align-items:center;gap:8px;font-size:12px;margin:3px 0;color:var(--dim);';
  const sw = document.createElement('span');
  sw.style.cssText = 'width:14px;height:14px;border-radius:3px;background:' + DATA.groupColor[g] + ';';
  d.appendChild(sw);
  d.appendChild(document.createTextNode(DATA.groups[g].name + ' (' + g + ')'));
  gl.appendChild(d);
});

refresh();
</script>
</body>
</html>
"""

# 注入 JSON 数据
data_json = json.dumps(payload, ensure_ascii=False)
html_page = html_page.replace("__DATA__", data_json)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html_page)

print(f"[OK] interactive overview: {OUT}")
print(f"[OK] nodes={len(plugin_nodes)+len(ext_nodes)}, edges={len(edge_list)}, groupEdges={len(group_edges)}")
