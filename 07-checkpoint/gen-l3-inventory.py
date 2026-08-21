#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L3 S0: 生成 stage-00-l3-inventory.json — 基于 4 决策点收敛的 L3 清单
决策:
1. bundle自身(bundle/base, bundle/headless) + boot(app-boot, cmdline) → 特殊独立分析模块 (不进主DAG, 单独一节)
2. test-support 6 包 → 归入 seam (不建插件节点)
3. L3 新增抽象 seam (e2b/lsp/mcp-client/hook-protocol/sdk-protocol/terminal/acp等) → 并入 external-seams.json
4. 主 DAG → 更新 webapp-dag.json
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

MAP = r"D:\Opencode_Download\Mission-file\2026-08\0814-deepseek-harness源码解析\07-checkpoint\PACKAGE-MAP.json"
DAG = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0822-plugin-dag-v0.1.1-rc2\01-dag-data\webapp-dag.json"
EXT = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0822-plugin-dag-v0.1.1-rc2\01-dag-data\external-seams.json"
OUT = r"/home/zako-mio/opencode/archive/Mission-file/2026-08/0822-plugin-dag-v0.1.1-rc2\07-checkpoint\stage-00-l3-inventory.json"

with open(MAP, "r", encoding="utf-8") as f:
    pkgmap = json.load(f)
with open(DAG, "r", encoding="utf-8") as f:
    dag = json.load(f)
with open(EXT, "r", encoding="utf-8") as f:
    ext = json.load(f)

all_pkgs = {p["name"]: p for p in pkgmap["packages"]}
analyzed_names = {n["name"] for n in dag["nodes"]} | {s["name"] for s in ext["seams"]}
uncovered = [p for p in all_pkgs.values() if p["name"] not in analyzed_names]
print(f"[INFO] uncovered: {len(uncovered)}")

# 决策1: 特殊独立分析模块
SPECIAL = {
    "@deepseek-ai/dsh-base": "bundle 自身",
    "@deepseek-ai/dsh-headless": "独立 bundle (有 cordis.patch.yml)",
    "@deepseek-ai/dsh-app-boot": "启动框架",
    "@deepseek-ai/dsh-cmdline": "命令行解析",
}
# 决策2: test-support → seam
TEST_SUPPORT = {
    "@deepseek-ai/dsh-acp-snapshot", "@deepseek-ai/dsh-agent-loop-testkit",
    "@deepseek-ai/dsh-client-test-runtime", "@deepseek-ai/dsh-llm-mock-server",
    "@deepseek-ai/dsh-llm-replay", "@deepseek-ai/dsh-loader-smoke",
}
# 决策3: 抽象基座 seam (L3 并入 external-seams)
ABSTRACT_SEAMS = {
    "@deepseek-ai/dsh-e2b", "@deepseek-ai/dsh-lsp", "@deepseek-ai/dsh-mcp-client",
    "@deepseek-ai/dsh-hook-protocol", "@deepseek-ai/dsh-sdk-protocol",
    "@deepseek-ai/dsh-terminal", "@deepseek-ai/dsh-acp",
}

special_list, seam_list, plugin_list = [], [], []
for p in uncovered:
    if p["name"] in SPECIAL:
        special_list.append(p)
    elif p["name"] in TEST_SUPPORT or p["name"] in ABSTRACT_SEAMS:
        seam_list.append(p)
    else:
        plugin_list.append(p)

print(f"[INFO] 特殊独立模块: {len(special_list)}")
for p in special_list:
    print(f"  {p['name']} @ {p['path']} ({p.get('ts_count',0)} ts)")

print(f"\n[INFO] 归入 seam: {len(seam_list)}")
for p in seam_list:
    print(f"  {p['name']} @ {p['path']} ({p.get('ts_count',0)} ts)")

print(f"\n[INFO] L3 插件节点: {len(plugin_list)}")
for p in sorted(plugin_list, key=lambda x: x["name"]):
    print(f"  {p['name']} @ {p['path']} ({p.get('ts_count',0)} ts)")

# 分组建议
PLUGIN_GROUPS = {
    "G30 外部执行后端": ["@deepseek-ai/dsh-fs-e2b", "@deepseek-ai/dsh-subprocess-e2b",
                     "@deepseek-ai/dsh-terminal-bash", "@deepseek-ai/dsh-tool-terminal",
                     "@deepseek-ai/dsh-tool-bash-persistent", "@deepseek-ai/dsh-schedule"],
    "G31 协议与SDK": ["@deepseek-ai/dsh-sdk-client", "@deepseek-ai/dsh-sdk-jsonrpc-server"],
    "G32 LSP集成": ["@deepseek-ai/dsh-lsp-stdio", "@deepseek-ai/dsh-tool-lsp"],
    "G33 子代理外部后端": ["@deepseek-ai/dsh-subagent-acp", "@deepseek-ai/dsh-subagent-claude-code",
                       "@deepseek-ai/dsh-subagent-codex", "@deepseek-ai/dsh-subagent-dsh-sdk"],
    "G34 Web上下文扩展": ["@deepseek-ai/dsh-web-fetch-http", "@deepseek-ai/dsh-web-search-exa",
                       "@deepseek-ai/dsh-web-search-perplexity", "@deepseek-ai/dsh-session-reference",
                       "@deepseek-ai/dsh-time-context", "@deepseek-ai/dsh-tmux-context"],
    "G35 会话存储变体": ["@deepseek-ai/dsh-session-persistence-sqlite", "@deepseek-ai/dsh-storage-sqlite",
                     "@deepseek-ai/dsh-session-title-all-prompts-llm", "@deepseek-ai/dsh-tool-session-query"],
    "G36 Hooks工具扩展": ["@deepseek-ai/dsh-hooks-claude-code", "@deepseek-ai/dsh-hooks-codex",
                      "@deepseek-ai/dsh-tool-cordis", "@deepseek-ai/dsh-tool-ask-user",
                      "@deepseek-ai/dsh-persona", "@deepseek-ai/dsh-agent-tool-presentation"],
    "G37 示例与框架": ["@deepseek-ai/dsh-acp-demo", "@deepseek-ai/dsh-agent-spine-demo",
                    "@deepseek-ai/dsh-sdk-jsonrpc-demo", "@deepseek-ai/dsh-typert-generator",
                    "@deepseek-ai/dsh-native-command", "@deepseek-ai/dsh-host-frontend-static",
                    "@deepseek-ai/dsh-host-directory-picker", "@deepseek-ai/dsh-host-directory-picker-browse",
                    "@deepseek-ai/dsh-host-directory-picker-native"],
}

import collections
name_to_group = {}
for gname, names in PLUGIN_GROUPS.items():
    for n in names:
        name_to_group[n] = gname

# 校验分组覆盖
covered = set()
for gname, names in PLUGIN_GROUPS.items():
    covered.update(names)
unplaced = [p["name"] for p in plugin_list if p["name"] not in covered]
print(f"\n[CHECK] 分组覆盖: {len(covered)}/{len(plugin_list)}, 未分配: {unplaced}")

inventory = {
    "meta": {
        "mission": "L3 其余插件 DAG 分析",
        "generated_at": "2026-08-17",
        "uncovered_total": len(uncovered),
        "special_module_count": len(special_list),
        "seam_count": len(seam_list),
        "plugin_node_count": len(plugin_list),
        "decisions": [
            "bundle自身+boot层 → 特殊独立分析模块(不进主DAG,单独一节)",
            "test-support 6包 → 归入 seam",
            "L3抽象基座 seam → 并入 external-seams.json",
            "主DAG → 更新 webapp-dag.json"
        ]
    },
    "special_modules": [{"id": p["name"].replace("@deepseek-ai/dsh-", "dsh-"), "name": p["name"], "path": p["path"], "note": SPECIAL[p["name"]], "ts_count": p.get("ts_count", 0)} for p in special_list],
    "l3_seams": [{"id": p["name"].replace("@deepseek-ai/dsh-", "dsh-"), "name": p["name"], "path": p["path"], "note": "test-support" if p["name"] in TEST_SUPPORT else "抽象基座", "ts_count": p.get("ts_count", 0)} for p in seam_list],
    "groups": [
        {"id": "G30", "name": "外部执行后端", "plugins": [{"id": n.replace("@deepseek-ai/dsh-", "dsh-"), "name": n, "path": all_pkgs[n]["path"]} for n in PLUGIN_GROUPS["G30 外部执行后端"]]},
        {"id": "G31", "name": "协议与SDK", "plugins": [{"id": n.replace("@deepseek-ai/dsh-", "dsh-"), "name": n, "path": all_pkgs[n]["path"]} for n in PLUGIN_GROUPS["G31 协议与SDK"]]},
        {"id": "G32", "name": "LSP集成", "plugins": [{"id": n.replace("@deepseek-ai/dsh-", "dsh-"), "name": n, "path": all_pkgs[n]["path"]} for n in PLUGIN_GROUPS["G32 LSP集成"]]},
        {"id": "G33", "name": "子代理外部后端", "plugins": [{"id": n.replace("@deepseek-ai/dsh-", "dsh-"), "name": n, "path": all_pkgs[n]["path"]} for n in PLUGIN_GROUPS["G33 子代理外部后端"]]},
        {"id": "G34", "name": "Web上下文扩展", "plugins": [{"id": n.replace("@deepseek-ai/dsh-", "dsh-"), "name": n, "path": all_pkgs[n]["path"]} for n in PLUGIN_GROUPS["G34 Web上下文扩展"]]},
        {"id": "G35", "name": "会话存储变体", "plugins": [{"id": n.replace("@deepseek-ai/dsh-", "dsh-"), "name": n, "path": all_pkgs[n]["path"]} for n in PLUGIN_GROUPS["G35 会话存储变体"]]},
        {"id": "G36", "name": "Hooks工具扩展", "plugins": [{"id": n.replace("@deepseek-ai/dsh-", "dsh-"), "name": n, "path": all_pkgs[n]["path"]} for n in PLUGIN_GROUPS["G36 Hooks工具扩展"]]},
        {"id": "G37", "name": "示例与框架", "plugins": [{"id": n.replace("@deepseek-ai/dsh-", "dsh-"), "name": n, "path": all_pkgs[n]["path"]} for n in PLUGIN_GROUPS["G37 示例与框架"]]},
    ]
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(inventory, f, ensure_ascii=False, indent=2)
print(f"\n[OK] wrote {OUT}")
