#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S6b L3 MD 镜像全量生成: 06-md/ 目录 (L1+L2+L3 全覆盖)
数据源: webapp-dag.json (173 节点) + external-seams.json (49 seam)
- 00-index.md        总览 (更新 L1/L2/L3 统计)
- 01-groups.md       分组清单 (37 组)
- 02-layers.md       拓扑分层 (17 层)
- plugins/{id}.md    每插件一页 (AI 友好, 含来源层标注)
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-plugin-dag-rc8"
DAG = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
EXT = os.path.join(BASE, "01-dag-data", "external-seams.json")
MD = os.path.join(BASE, "06-md")
MDP = os.path.join(MD, "plugins")

with open(DAG, "r", encoding="utf-8") as f:
    dag = json.load(f)
with open(EXT, "r", encoding="utf-8") as f:
    ext = json.load(f)

nodes = {n["id"]: n for n in dag["nodes"]}
groups = {g["id"]: g for g in dag["groups"]}
ext_map = {e["id"]: e for e in ext["seams"]}

out_edges = {nid: [] for nid in nodes}
in_edges = {nid: [] for nid in nodes}
for e in dag["edges"]:
    out_edges[e["from"]].append(e)
    in_edges[e["to"]].append(e)

os.makedirs(MDP, exist_ok=True)

LAYER_LABEL = {"L1": "L1 核心集", "L2": "L2 web-app", "L3": "L3 其余"}

def mech_label(m):
    return {"E1": "编译依赖", "E2": "运行时依赖", "E3": "组合依赖"}.get(m, m)

# ---- 每插件 MD ----
count = 0
for nid, n in nodes.items():
    src = n.get("source_layer", "L1")
    lines = [f"# {nid}", ""]
    lines.append(f"- 包名: `{n['name']}`")
    lines.append(f"- 分组: {n['group']} {n['group_name']}")
    lines.append(f"- 拓扑层: Layer {n['layer']}")
    lines.append(f"- 来源层: {LAYER_LABEL.get(src, src)}")
    lines.append(f"- 源码路径: `{n.get('path','')}`")
    lines.append("")
    # 为什么需要它（设计初衷）
    why_data = n.get("why", {})
    if why_data and why_data.get("text"):
        lines.append("## 为什么需要它（设计初衷）")
        lines.append(why_data["text"])
        if why_data.get("history"):
            lines.append("")
            lines.append(f"发展史：{why_data['history']}")
        srcs = why_data.get("sources", [])
        if srcs:
            lines.append("")
            lines.append("来源：")
            for s in srcs:
                lines.append(f"- {s}")
        lines.append("")
    lines.append("## 实现逻辑")
    lines.append(n["implementation"])
    lines.append("")
    lines.append("## Provides")
    for p in n.get("provides", []):
        lines.append(f"- {p}")
    lines.append("")
    lines.append("## Depends On (上游依赖)")
    ups = sorted(out_edges.get(nid, []), key=lambda e: e["to"])
    if ups:
        for e in ups:
            lines.append(f"- `{e['to']}` [{mech_label(e.get('mechanism','E1'))}] - {e.get('purpose','')}")
            if e.get("evidence"):
                lines.append(f"  - 证据: `{e['evidence']}`")
    else:
        lines.append("- 无依赖（基础插件）")
    lines.append("")
    lines.append("## Dependents (下游被依赖)")
    downs = sorted(in_edges.get(nid, []), key=lambda e: e["from"])
    if downs:
        for e in downs:
            lines.append(f"- `{e['from']}` - {e.get('purpose','')}")
    else:
        lines.append("- 无下游（叶子/被消费端）")
    lines.append("")
    with open(os.path.join(MDP, f"{nid}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    count += 1

# ---- 外部 seam MD (49 全量) ----
seam_count = 0
for sid, s in ext_map.items():
    lines = [f"# {sid} (外部基座 seam)", ""]
    lines.append(f"- 包名: `{s['name']}`")
    lines.append(f"- 源码路径: `{s.get('path','') or 'vendor 框架包'}`")
    lines.append(f"- 被插件引用: {s.get('ref_count',0)} 次")
    lines.append(f"- 描述: {s.get('description','')}")
    lines.append("")
    lines.append("## 被集依赖 (下游)")
    for d in sorted(s.get("referred_by", [])):
        lines.append(f"- `{d}`")
    lines.append("")
    lines.append("## 依赖机制")
    lines.append("、".join(mech_label(m) for m in s.get("mechanisms", [])))
    lines.append("")
    with open(os.path.join(MDP, f"{sid}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    seam_count += 1

# ---- 分组清单 ----
lines = ["# 插件分组清单", ""]
lines.append(f"共 {len(groups)} 组 / {len(nodes)} 核心插件 / {len(ext_map)} 外部 seam")
lines.append("")
for gid, g in groups.items():
    lines.append(f"## {gid} · {g['name']} ({len(g['plugins'])} 插件)")
    for pid in g["plugins"]:
        if pid in nodes:
            n = nodes[pid]
            src = n.get("source_layer", "L1")
            lines.append(f"- [{pid}](plugins/{pid}.md) - L{n['layer']} ({LAYER_LABEL.get(src, src)})")
    lines.append("")
with open(os.path.join(MD, "01-groups.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# ---- 拓扑分层 ----
lines = ["# 拓扑分层 (层次遍历)", ""]
for lid in sorted(dag["layers"].keys(), key=int):
    ids = dag["layers"][lid]
    lines.append(f"## Layer {lid} ({len(ids)} 插件)")
    for pid in sorted(ids):
        lines.append(f"- [{pid}](plugins/{pid}.md)")
    lines.append("")
with open(os.path.join(MD, "02-layers.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# ---- 总览 ----
# 来源层统计
src_count = {}
for n in dag["nodes"]:
    s = n.get("source_layer", "L1")
    src_count[s] = src_count.get(s, 0) + 1
l2_nodes = src_count.get("L2", 0)
l3_nodes = src_count.get("L3", 0)
l1_nodes = len(dag["nodes"]) - l2_nodes - l3_nodes

lines = [
    "# DeepSeek Harness 插件级 DAG 依赖链分析 (MD 镜像)",
    "",
    "## 统计",
    f"- 插件节点: {len(nodes)}（L1 核心集 {l1_nodes} + L2 web-app {l2_nodes} + L3 其余 {l3_nodes}）",
    f"- 外部 seam 基座: {len(ext_map)}",
    f"- 依赖边: {len(dag['edges'])}",
    f"- 拓扑层: {dag['meta']['layer_count']}",
    f"- 分组: {len(groups)}",
    "",
    "## 阅读导航",
    "- [分组清单](01-groups.md)",
    "- [拓扑分层](02-layers.md)",
    "- [交互总览 HTML](../04-interactive/index.html)",
    "- [每插件 HTML](../02-plugin-pages/index.html)",
    "",
    "## 拓扑分层速览",
]
for lid in sorted(dag["layers"].keys(), key=int):
    ids = dag["layers"][lid]
    lines.append(f"- **Layer {lid}** ({len(ids)}): {', '.join(sorted(ids))}")
lines.append("")
with open(os.path.join(MD, "00-index.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"[OK] MD 镜像全量: {count} 插件 (L1+L2+L3) + {seam_count} seam + 3 索引")
