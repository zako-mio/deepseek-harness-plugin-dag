#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 L3-DELEGATE-PROMPTS.md 覆盖 stage-00-l3-inventory.json 全部 39 插件 + 13 seam + 4 特殊模块"""
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

DOC = r"D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag\07-checkpoint\L3-DELEGATE-PROMPTS.md"
INV = r"D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag\07-checkpoint\stage-00-l3-inventory.json"

with open(DOC, "r", encoding="utf-8") as f:
    doc = f.read()
with open(INV, "r", encoding="utf-8") as f:
    inv = json.load(f)

# 收集 inventory 中所有 id
inv_ids = set()
special_ids = set()
seam_ids = set()
plugin_ids = set()
for s in inv.get("special_modules", []):
    inv_ids.add(s["id"]); special_ids.add(s["id"])
for s in inv.get("l3_seams", []):
    inv_ids.add(s["id"]); seam_ids.add(s["id"])
for g in inv.get("groups", []):
    for p in g.get("plugins", []):
        inv_ids.add(p["id"]); plugin_ids.add(p["id"])

# 文档中出现的 dsh- id
doc_ids = set(re.findall(r'\bdsh-[a-z0-9-]+', doc))

# test-support 6 seam 是故意不进采集的（已归 seam + 有占位页）
EXEMPT = {"dsh-acp-snapshot", "dsh-agent-loop-testkit", "dsh-client-test-runtime",
          "dsh-llm-mock-server", "dsh-llm-replay", "dsh-loader-smoke"}

missing = sorted((inv_ids - doc_ids) - EXEMPT)
print(f"[INFO] inventory ids: {len(inv_ids)} (plugin={len(plugin_ids)}, seam={len(seam_ids)}, special={len(special_ids)})")
print(f"[INFO] doc mentions dsh- ids: {len(doc_ids)}")
print(f"[INFO] missing from doc (excluding exempt seam): {len(missing)}")
for m in missing:
    print(f"  [MISSING] {m}")

# 每路 prompt 覆盖检查（宽松：从 '### 需要分析的 N 个插件' 到下一个 '### ' 或 '## '）
route_markers = [
    ("R1", "需要分析的 11 个插件"),
    ("R2", "需要分析的 8 个插件"),
    ("R3", "需要分析的 10 个插件"),
    ("R4", "需要分析的 6 个插件"),
    ("R5", "需要分析的 5 个插件"),
]
for rid, marker in route_markers:
    idx = doc.find(marker)
    if idx == -1:
        print(f"  {rid}: MARKER NOT FOUND")
        continue
    nxt = doc.find("\n### ", idx + 10)
    nxt2 = doc.find("\n## ", idx + 10)
    ends = [x for x in (nxt, nxt2) if x > 0]
    end = min(ends) if ends else len(doc)
    block = doc[idx:end]
    ids = sorted(set(re.findall(r'\bdsh-[a-z0-9-]+', block)) - {"dsh-xxx"})
    print(f"  {rid}: {len(ids)} ids -> {ids}")

# 特殊模块在 R4 中
if "特殊模块结构分析" in doc and all(x in doc for x in ["dsh-base", "dsh-headless", "dsh-app-boot", "dsh-cmdline"]):
    print("\n[OK] special modules covered in R4")
else:
    print("\n[WARN] special modules may be incomplete")

# seam 核实任务
if "referred_by" in doc and all(x in doc for x in ["dsh-acp", "dsh-e2b", "dsh-hook-protocol", "dsh-lsp", "dsh-mcp-client", "dsh-sdk-protocol", "dsh-terminal"]):
    print("[OK] 7 abstract seam verify task present")
else:
    print("[WARN] abstract seam verify task incomplete")

print(f"\n{'[OK] 文档覆盖完整' if not missing else f'[FAIL] 缺失 {len(missing)} 个'}")
