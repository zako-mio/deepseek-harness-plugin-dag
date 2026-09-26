# -*- coding: utf-8 -*-
"""S0: DAG 重要性权重计算（完整版）
读 webapp-dag.json，计算被依赖数/依赖数/拓扑层/组，按 DAG 重要性分级
核心(deep why) / 普通 / 轻量(简版 why)
"""
import json, os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
DAG = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
OUT = os.path.join(BASE, "07-checkpoint", "plugin-weight.json")
sys.stdout.reconfigure(encoding="utf-8")

with open(DAG, encoding="utf-8") as f:
    d = json.load(f)

nodes = d["nodes"]
edges = d["edges"]

# 被依赖数（作为 to 的边数 = 下游消费者数）
depended = {}
depends = {}
for e in edges:
    frm, to = e["from"], e["to"]
    depended[to] = depended.get(to, 0) + 1
    depends[frm] = depends.get(frm, 0) + 1

# 组装
result = []
for n in nodes:
    nid = n["id"]
    result.append({
        "id": nid,
        "name": n.get("name", nid),
        "group": n.get("group", ""),
        "group_name": n.get("group_name", ""),
        "layer": n.get("layer", -1),
        "depended_count": depended.get(nid, 0),  # 被依赖数
        "depends_count": depends.get(nid, 0),    # 依赖数
        "is_seam": nid.startswith("dsh-") and ("seam" in nid or nid in ("dsh-invariants", "dsh-scope", "dsh-timeout"))
    })

# 分组（按 group 统计每组的最大被依赖数，用于识别组代表）
group_max = {}
for r in result:
    g = r["group"]
    if r["depended_count"] > group_max.get(g, {"count": -1, "id": ""})["count"]:
        group_max[g] = {"count": r["depended_count"], "id": r["id"]}

# 权重分级：
# - seam 基座 = 轻量（它们是抽象包，why 由 dsh 框架统一说明）
# - 核心：被依赖数 >= 8 或 层 <= 2 且被依赖 >= 3 或 组代表
# - 轻量：被依赖数 <= 1 且 层 >= 5（叶子）
# - 其余普通
for r in result:
    g_rep = group_max.get(r["group"], {}).get("id") == r["id"]
    if r.get("is_seam"):
        r["weight"] = "light"
    elif r["depended_count"] >= 8 or g_rep or (r["layer"] <= 2 and r["depended_count"] >= 3):
        r["weight"] = "core"
    elif r["depended_count"] <= 1 and r["layer"] >= 5:
        r["weight"] = "light"
    else:
        r["weight"] = "normal"

# 统计
wc = collections.Counter(r["weight"] for r in result) if "collections" in dir() else {}
from collections import Counter
wc = Counter(r["weight"] for r in result)
print(f"核心(core): {wc['core']} / 普通(normal): {wc['normal']} / 轻量(light): {wc['light']}")

# 输出核心列表
print("\n=== 核心节点（深度 why）===")
for r in sorted([x for x in result if x["weight"] == "core"], key=lambda x: -x["depended_count"]):
    print(f"  {r['id']:<32} 被依赖:{r['depended_count']:<3} 层:{r['layer']:<3} {r['group_name']}")

with open(OUT, "w", encoding="utf-8") as f:
    json.dump({"meta": {"nodes": len(result), "weights": dict(wc), "criteria": "core: depended>=8 或组代表或(层<=2且depended>=3); light: seam 或(被依赖<=1且层>=5); 其余 normal"}, "plugins": result}, f, ensure_ascii=False, indent=2)
print(f"\n[OUT] 已写入 {OUT}")
