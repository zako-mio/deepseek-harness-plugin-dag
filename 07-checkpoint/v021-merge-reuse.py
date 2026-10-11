#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增量级联核心：把 v0.1.7-rc.2 的既有节点分析复用到 v0.2.1-alpha.2。

判定（对 classification.json 的每个 node）：
  1. 该 id 在旧版分析里存在，且
  2. 其包源码在 delta-017-021.json 中为 version_only / tests_changed / identical
     （即 src/ 逐字节未变）
  ⇒ 直接复用旧 entry（implementation / provides / depends_on 均以包内相对路径
     引用源码行，src 未变则证据依然成立）。

  否则 ⇒ 进入 redo 列表，交给子 Agent 重读源码重做。

产出：
  - 07-checkpoint/v021/reuse-map.json         复用/重做清单 + 原因
  - 07-checkpoint/v021/stage-01-shard-00-reuse.json   复用 entry（build-dag 的
    `stage-01-shard-` glob 会自动纳入）

另附**证据存活性自检**：对复用 entry 的 evidence 做 file:line 解析，确认文件仍存在
且行号仍在文件范围内（src 未变时应当 100% 通过；不通过则说明复用判定有漏洞）。
"""
import os, sys, json, re, glob

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
OUT = os.path.join(SCRIPT_DIR, "v021")
OLD_OUT = os.path.join(SCRIPT_DIR, "v017")
SRC = os.path.join(BASE, "05-source", "dsh-v0.2.1-alpha.2", "deepseek-harness-dsh-v0.2.1-alpha.2")

REUSE_CATS = {"version_only", "tests_changed", "identical"}

cls = json.load(open(os.path.join(OUT, "classification.json"), encoding="utf-8"))
facts = json.load(open(os.path.join(OUT, "facts.json"), encoding="utf-8"))
delta = json.load(open(os.path.join(OUT, "delta-017-021.json"), encoding="utf-8"))

# ---- 旧版分析（239 节点）----
old_analysis = {}
for f in sorted(glob.glob(os.path.join(OLD_OUT, "stage-01-shard-*.json"))):
    for x in json.load(open(f, encoding="utf-8")):
        old_analysis[x["id"]] = x
print(f"[INFO] 旧版分析 entry: {len(old_analysis)}")

cat = delta["category"]
reuse, redo, reason = {}, [], {}

for pid in cls["nodes"]:
    c = cat.get(pid)
    if c is None:
        redo.append(pid); reason[pid] = "added-new-package"
    elif pid not in old_analysis:
        redo.append(pid); reason[pid] = "no-prior-analysis"
    elif c in REUSE_CATS:
        reuse[pid] = old_analysis[pid]; reason[pid] = f"reuse-{c}"
    else:
        redo.append(pid); reason[pid] = f"redo-{c}"

# ---- 证据存活性自检 ----
RE_EV = re.compile(r"([A-Za-z0-9_./\-]+\.(?:ts|tsx|mts|json|yml|yaml)):(\d+)(?:-(\d+))?")
ev_total = ev_bad_file = ev_bad_line = 0
ev_problems = []
for pid, x in reuse.items():
    pkgdir = os.path.join(SRC, facts[pid]["path"])
    for dp in x.get("depends_on", []):
        for m in RE_EV.finditer(dp.get("evidence", "")):
            f, ln = m.group(1), int(m.group(2))
            ev_total += 1
            # evidence 里可能写包内相对路径、src/ 下相对路径、或仓根相对路径（E3 装配文件）
            cands = [os.path.join(pkgdir, f), os.path.join(pkgdir, "src", f), os.path.join(SRC, f)]
            existing = [c for c in cands if os.path.isfile(c)]
            if not existing:
                ev_bad_file += 1
                ev_problems.append(f"{pid}: 文件不存在 {f}")
                continue
            # 记法可能不规范（如只写 index.ts），任一候选文件能容纳该行号即视为证据仍存活
            if not any(sum(1 for _ in open(c, encoding="utf-8", errors="replace")) >= ln for c in existing):
                ev_bad_line += 1
                ev_problems.append(f"{pid}: {f}:{ln} 超出所有候选文件行数")

stats = {
    "nodes_total": len(cls["nodes"]),
    "reused": len(reuse),
    "redo": len(redo),
    "reuse_ratio": round(len(reuse) / max(1, len(cls["nodes"])), 4),
    "redo_breakdown": {},
    "evidence_checked": ev_total,
    "evidence_bad_file": ev_bad_file,
    "evidence_bad_line": ev_bad_line,
}
from collections import Counter
stats["redo_breakdown"] = dict(Counter(reason[p] for p in redo))

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "reuse-map.json"), "w", encoding="utf-8") as f:
    json.dump({"stats": stats, "reused": sorted(reuse), "redo": sorted(redo),
               "reason": reason, "evidence_problems": ev_problems[:50]}, f, ensure_ascii=False, indent=1)

with open(os.path.join(OUT, "stage-01-shard-00-reuse.json"), "w", encoding="utf-8") as f:
    json.dump([reuse[p] for p in sorted(reuse)], f, ensure_ascii=False, indent=1)

print(f"[OK] 节点 {stats['nodes_total']}  →  复用 {stats['reused']} / 重做 {stats['redo']}"
      f"  （复用率 {stats['reuse_ratio']*100:.1f}%）")
print(f"[INFO] 重做原因: {stats['redo_breakdown']}")
print(f"[INFO] 证据自检: 检查 {ev_total} 条 file:line，文件缺失 {ev_bad_file}，行号越界 {ev_bad_line}")
for p in ev_problems[:10]:
    print("    [WARN]", p)
print(f"[OK] wrote reuse-map.json + stage-01-shard-00-reuse.json")
