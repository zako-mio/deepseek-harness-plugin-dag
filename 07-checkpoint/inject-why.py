# -*- coding: utf-8 -*-
"""S2: inject-why.py
将 07-checkpoint/research/aggregated.json 的 why 数据合并进 webapp-dag.json 每个节点
- 深度 why（设计初衷+发展史+来源）优先
- fallback why_short（一句话定位）
- 无数据时按分组名+实现逻辑自动推导
"""
import json, os, sys

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0819-plugin-dag-rc7"
DAG = os.path.join(BASE, "01-dag-data", "webapp-dag.json")
AGG = os.path.join(BASE, "07-checkpoint", "research", "aggregated.json")
sys.stdout.reconfigure(encoding="utf-8")

with open(DAG, encoding="utf-8") as f:
    dag = json.load(f)
with open(AGG, encoding="utf-8") as f:
    agg = json.load(f)

research = agg["plugins"]  # {id: {...}}

ok = True
deep_count = 0
short_count = 0
auto_count = 0
no_why = []

for n in dag["nodes"]:
    nid = n["id"]
    r = research.get(nid, {})
    if r.get("why"):
        n["why"] = {
            "text": r["why"],
            "history": r.get("history", ""),
            "sources": r.get("sources", []),
            "tier": "deep"
        }
        deep_count += 1
    elif r.get("why_short"):
        n["why"] = {
            "text": r["why_short"],
            "history": "",
            "sources": r.get("sources", []),
            "tier": "short"
        }
        short_count += 1
    else:
        # 自动推导：分组名 + 实现逻辑首句
        impl = n.get("implementation", "")
        first = impl.split("。")[0][:60] if impl else ""
        n["why"] = {
            "text": f"【自动推导】属于「{n.get('group_name', '未分组')}」域的插件。{first}",
            "history": "",
            "sources": [],
            "tier": "auto"
        }
        auto_count += 1
        no_why.append(nid)

print(f"深度 why: {deep_count} / 简版: {short_count} / 自动推导: {auto_count}")
if no_why:
    print(f"自动推导列表({len(no_why)}): {no_why[:20]}")

# 门控：全部有 why
missing = [n["id"] for n in dag["nodes"] if not n.get("why", {}).get("text")]
if missing:
    ok = False
    print(f"[FAIL] 缺 why: {missing}")

# 写回
with open(DAG, "w", encoding="utf-8") as f:
    json.dump(dag, f, ensure_ascii=False, indent=2)
print(f"[{'OK' if ok else 'HAS ISSUE'}] 已写回 webapp-dag.json，节点 {len(dag['nodes'])}")
sys.exit(0 if ok else 1)
