#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RC8 升级标注注入：在受 primitives/slots 声明移除影响但运行时仍引用的插件页插入说明"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = "/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-plugin-dag-rc8"
PAGES = os.path.join(BASE, "02-plugin-pages")

# 受影响的节点（rc8 移除了 primitives/slots peer 声明但源码仍 import）
affected = ["dsh-client-locale","dsh-client-runtime","dsh-client-ui-agent-preset","dsh-client-ui-attachment",
"dsh-client-ui-commands","dsh-client-ui-conversation","dsh-client-ui-cordis","dsh-client-ui-deliverables",
"dsh-client-ui-directory-picker-browse","dsh-client-ui-goal","dsh-client-ui-input-trigger","dsh-client-ui-jobs",
"dsh-client-ui-layout","dsh-client-ui-message-feedback","dsh-client-ui-model-selection","dsh-client-ui-permission-presets",
"dsh-client-ui-plan","dsh-client-ui-settings","dsh-client-ui-settings-general","dsh-client-ui-settings-models",
"dsh-client-ui-settings-plugin-inventory","dsh-client-ui-settings-plugins","dsh-client-ui-sidebar","dsh-client-ui-skill",
"dsh-client-ui-subagent","dsh-client-ui-theme","dsh-client-ui-tool","dsh-client-ui-trajectory","dsh-client-ui-user-questions",
"dsh-client-ui-workflow-run","dsh-client-ui-workspace","dsh-client-web","dsh-session-log-export"]

NOTE = '<div class="whybox" style="border-color:#7a5f2f;background:#1d1810;"><span class="tag" style="color:#e0b25e;">RC8 变更 · 依赖声明调整</span><p>本包在 <b>RC8</b> 中移除了对 <code>dsh-client-ui-primitives</code> / <code>dsh-client-ui-slots</code> 的 <code>peerDependencies</code> 声明，但源码 <code>src/</code> 仍通过 import 实际引用（运行时依赖未变）。这是 RC8 对 UI 依赖的声明层解耦重构。DAG 依赖边按实际引用保留。</p></div>'

# 锚点：在 "① 实现逻辑" 的 </h2> 后插入
ANCHOR = '<h2>① 实现逻辑</h2>'

count = 0
for nid in affected:
    fp = os.path.join(PAGES, f"{nid}.html")
    if not os.path.exists(fp):
        print(f"[SKIP] 页面不存在: {nid}")
        continue
    txt = open(fp, encoding="utf-8").read()
    if "RC8 变更 · 依赖声明调整" in txt:
        continue
    if ANCHOR not in txt:
        print(f"[WARN] 无锚点: {nid}")
        continue
    txt = txt.replace(ANCHOR, ANCHOR + NOTE, 1)
    open(fp, "w", encoding="utf-8").write(txt)
    count += 1

print(f"[OK] 注入 RC8 声明调整标注: {count} 页")
