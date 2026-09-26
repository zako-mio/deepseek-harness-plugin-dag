#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
S3 L3 交互图 DATA 注入（幂等同步器）。

管线顺序: gen-overview.py  →  inject-data-l3.py
- gen-overview.py 是 04-interactive/index.html 的唯一权威生成器（含新组级网格 + 下钻数据）。
- 本脚本从 gen-overview.build_payload() 复用同一份 payload（绝不重复实现数据逻辑），
  定位 `const DATA = ...;` 行并原地替换。
- 幂等: payload 与页内现有 DATA 一致时不改动字节；因此「同输入 → 同产物」的确定性成立，
  且历史事故（旧版本脚本用只有插件数据的 payload 覆盖整行、冲掉 grid 数据）不再复现。
"""
import json, os, re, sys, importlib.util

sys.stdout.reconfigure(encoding="utf-8")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(SCRIPT_DIR)
HTML = os.path.join(BASE, "04-interactive", "index.html")


def load_builder():
    spec = importlib.util.spec_from_file_location("gen_overview", os.path.join(SCRIPT_DIR, "gen-overview.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    mod = load_builder()
    payload, _stats = mod.build_payload()
    data_json = json.dumps(payload, ensure_ascii=False)
    new_line = "const DATA = " + data_json + ";"

    with open(HTML, "r", encoding="utf-8", newline="") as f:
        content = f.read()

    lines = content.split("\n")  # 保留行尾 '\r'
    idx = None
    for i, l in enumerate(lines):
        if l.startswith("const DATA = "):
            idx = i
            break
    if idx is None:
        print("[ERR] const DATA 行未找到")
        raise SystemExit(1)

    cr = "\r" if lines[idx].endswith("\r") else ""
    if lines[idx] == new_line + cr:
        print(f"[OK] DATA 已同步（{len(new_line)} 字符），无改动")
    else:
        old_len = len(lines[idx])
        lines[idx] = new_line + cr
        with open(HTML, "w", encoding="utf-8", newline="") as f:
            f.write("\n".join(lines))
        print(f"[OK] DATA 行已替换: {old_len} -> {len(lines[idx])} 字符")

    # disabled 样式选择器必须存在（质量门控检查项）
    if 'node[kind="disabled"]' not in content:
        print("[WARN] 样式缺 node[kind=disabled]")

    print(f"[OK] plugins={len(payload['plugins'])} seams={len(payload['seams'])} "
          f"groups={len(payload['groups'])} gridNodes={len(payload['grid']['nodes'])} "
          f"disabled={len(payload['disabledIds'])}")


if __name__ == "__main__":
    main()
