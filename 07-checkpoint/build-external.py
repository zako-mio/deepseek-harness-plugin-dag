#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查询 39 个外部 seam 包在 PACKAGE-MAP.json 中的路径/描述, 输出外部包元数据清单"""
import json, os, glob, collections

BASE = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-plugin-dag-rc8"
CHK = os.path.join(BASE, "07-checkpoint")
MAP = r"D:\Opencode_Download\Mission-file\2026-08\0814-deepseek-harness源码解析\07-checkpoint\PACKAGE-MAP.json"

# 1. 收集外部包引用
refs = collections.Counter()
ref_evidence = collections.defaultdict(list)  # pid -> [(plugin_id, mechanism, evidence)]
for fp in glob.glob(os.path.join(CHK, "stage-01-r*.json")):
    with open(fp, "r", encoding="utf-8") as f:
        data = json.load(f)
    for p in data["plugins"]:
        for d in p.get("depends_on", []):
            pid = d.get("plugin_id", "")
            # 处理组合引用如 "dsh-session-projection + dsh-session-persistence" -> 拆成两条
            if " + " in pid:
                for part in pid.split(" + "):
                    np = part.strip()
                    if np.startswith("@deepseek-ai/"):
                        np = np[len("@deepseek-ai/"):]
                    if "/" in np:
                        np = np.split("/")[0]
                    if np.startswith("dsh-") or np.startswith("cordis-plugin-"):
                        refs[np] += 1
                        ref_evidence[np].append((p["id"], d.get("mechanism","E1"), d.get("evidence","")))
                continue
            pid = pid.strip()
            # 组合引用如 "dsh-llm / dsh-agent / dsh-scope" -> 拆成多条
            if " / " in pid:
                for part in pid.split(" / "):
                    np = part.strip()
                    if np.startswith("@deepseek-ai/"):
                        np = np[len("@deepseek-ai/"):]
                    if "/" in np and np.count("/") == 1 and not np.startswith("cordis"):
                        np = np.split("/")[0]
                    if np.startswith("dsh-") or np.startswith("cordis-plugin-"):
                        refs[np] += 1
                        ref_evidence[np].append((p["id"], d.get("mechanism","E1"), d.get("evidence","")))
                continue
            if pid.startswith("@deepseek-ai/"):
                pid = pid[len("@deepseek-ai/"):]
            if "/" in pid:
                pid = pid.split("/")[0]
            if pid.startswith("dsh-") or pid.startswith("cordis-plugin-"):
                refs[pid] += 1
                ref_evidence[pid].append((p["id"], d.get("mechanism","E1"), d.get("evidence","")))

# 2. 76 集合内 id
with open(os.path.join(BASE, "01-dag-data", "core-dag.json"), "r", encoding="utf-8") as f:
    dag = json.load(f)
node_ids = {n["id"] for n in dag["nodes"]}
external = sorted([k for k in refs if k not in node_ids], key=lambda x: (-refs[x], x))

# 3. 查 PACKAGE-MAP
with open(MAP, "r", encoding="utf-8") as f:
    pkgmap = json.load(f)
pkg_by_name = {p["name"]: p for p in pkgmap["packages"]}

out = []
for pid in external:
    full = "@deepseek-ai/" + pid
    meta = pkg_by_name.get(full, {})
    entry = {
        "id": pid,
        "name": full,
        "path": meta.get("path", ""),
        "ts_count": meta.get("ts_count", 0),
        "description": meta.get("description", ""),
        "ref_count": refs[pid],
        "referred_by": sorted(set(r[0] for r in ref_evidence[pid])),
        "mechanisms": sorted(set(r[1] for r in ref_evidence[pid]))
    }
    out.append(entry)

# 4. 输出
with open(os.path.join(BASE, "01-dag-data", "external-seams.json"), "w", encoding="utf-8") as f:
    json.dump({"count": len(out), "seams": out}, f, ensure_ascii=False, indent=2)

print(f"外部 seam 包: {len(out)}")
for e in out:
    print(f"  {e['id']} x{e['ref_count']} | path={e['path'] or 'N/A'} | desc={e['description'][:50]}")
