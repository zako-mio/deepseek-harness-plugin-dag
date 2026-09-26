#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v0.1.7-rc.2 分类器（终版）
  special   = bundle 包 + boot 胶水 → 08-special-modules
  node      = (被 bundle 装配) ∪ (有插件导出特征 ∧ 非抽象基座 ∧ 非纯库 ∧ 非测试支撑)
  seam      = 非 node ∧ 被 node 引用 ∧ (抽象基座 ∨ 纯库 ∨ 测试支撑 ∨ 未被装配的变体)
  uncovered = 其余（记账上报）
分组：域 + 大域子簇
"""
import json, os, sys
from collections import defaultdict, Counter
sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SCRIPT_DIR, "v017")
inv = json.load(open(os.path.join(OUT, "inventory.json"), encoding="utf-8"))
facts = json.load(open(os.path.join(OUT, "facts.json"), encoding="utf-8"))

SPECIAL = set(inv["special"])
TEST_HINT = ("test-support", "testkit", "mock", "snapshot", "smoke", "replay")

DOMAIN_CN = {
    "acp": "ACP 协议", "api": "API 网关与控制器", "attachment": "附件", "boot": "启动与插件管理",
    "browser-use": "浏览器自动化", "bundle": "Bundle 装配", "client": "Web 客户端",
    "compaction": "上下文压缩", "computer-use": "桌面自动化", "context": "上下文注入",
    "core": "核心运行时", "credentials": "凭据与授权", "deliverables": "交付物",
    "document": "文档处理", "experimental": "实验特性", "extensions": "宿主扩展",
    "feedback": "反馈通道", "fs": "文件系统", "goal": "目标与计划", "guard": "工具守卫",
    "hooks": "Hooks 扩展", "host": "宿主服务", "identity": "身份标识", "interaction": "交互命令",
    "jobs": "作业调度", "llm": "LLM 适配", "lsp": "LSP 集成", "mcp": "MCP 协议",
    "plan": "规划模式", "preset": "Agent 预设", "ptc-runtime": "代码执行运行时",
    "runtime-diagnostics": "运行时诊断", "sandbox": "沙箱", "schedule": "定时调度",
    "sdk": "SDK 与协议", "session": "会话", "session-query": "会话检索", "settings": "设置",
    "shell": "Shell 执行", "skill": "技能", "spill": "溢出存储", "ssh": "SSH 远程执行",
    "storage": "存储", "subagent": "子代理", "subprocess": "子进程", "terminal": "终端",
    "test-support": "测试支撑", "todo": "待办", "typert": "类型契约", "util": "工具库",
    "vendor": "框架 vendor", "web": "Web 访问", "webhook": "Webhook", "workflow": "工作流",
    "workspace": "工作区", "identity": "身份标识",
}

nodes, seams, uncovered = {}, {}, {}
node_ids = set()

for pid, f in facts.items():
    if pid in SPECIAL:
        continue
    m = f["markers"]
    has_plugin_export = bool(m["export_default"] or m["export_apply"] or m["export_inject"] or m["export_name"])
    abstract_base = m["extends_service"] > 0 and not f["assembled_in"]
    is_test = any(h in f["path"].lower() or h in pid for h in TEST_HINT)
    is_lib = not any(m.values())
    assembled = bool(f["assembled_in"])
    if assembled or (has_plugin_export and not abstract_base and not is_test and not is_lib):
        node_ids.add(pid)
        nodes[pid] = f

imported_by = defaultdict(set)
for pid in node_ids:
    f = facts[pid]
    for dep in f["import_pkgs"]:
        imported_by[dep].add(pid)
    for kind in ("peer", "deps"):
        for dep in f["declared"][kind]:
            imported_by[dep].add(pid)

for pid, f in facts.items():
    if pid in node_ids or pid in SPECIAL:
        continue
    m = f["markers"]
    abstract_base = m["extends_service"] > 0
    is_test = any(h in f["path"].lower() or h in pid for h in TEST_HINT)
    is_lib = not any(m.values())
    if imported_by.get(pid) or abstract_base or is_lib or is_test:
        seams[pid] = f
    else:
        uncovered[pid] = f

# ---- 分组 ----
def group_key(pid, f):
    d = f["domain"]
    if d == "client":
        return "client-ui" if pid.startswith("dsh-client-ui-") or pid.startswith("dsh-client-") and "-ui-" in pid else "client-runtime"
    if d == "session":
        return "session-format" if "format" in pid else "session-core"
    if d == "util":
        return "util"
    return d


GROUPS = {}
for pid, f in nodes.items():
    gk = group_key(pid, f)
    GROUPS.setdefault(gk, []).append(pid)

groups = []
for i, gk in enumerate(sorted(GROUPS), 1):
    if gk == "client-ui":
        nm = "客户端 UI 包"
    elif gk == "client-runtime":
        nm = "客户端运行时"
    elif gk == "session-core":
        nm = "会话核心"
    elif gk == "session-format":
        nm = "会话格式迁移"
    else:
        nm = DOMAIN_CN.get(gk, gk)
    groups.append({"id": f"G{i:02d}", "name": nm, "key": gk, "plugins": sorted(GROUPS[gk])})

print(f"facts total: {len(facts)} | special: {len(SPECIAL)} | NODES: {len(nodes)} | SEAMS: {len(seams)} | UNCOVERED: {len(uncovered)}")
print(f"groups: {len(groups)}")
for g in groups:
    print(f"  {g['id']} {g['name']} ({len(g['plugins'])})")
print("\n[seams]", len(seams))
for pid in sorted(seams):
    print("   ", pid)
print("\n[uncovered]", len(uncovered))
for pid in sorted(uncovered):
    print("   ", pid, "|", uncovered[pid]["path"])

cls = {
    "meta": {"version": "0.1.7-rc.2"},
    "special": sorted(SPECIAL),
    "nodes": sorted(nodes),
    "seams": sorted(seams),
    "uncovered": sorted(uncovered),
    "groups": groups,
    "imported_by": {k: sorted(v) for k, v in imported_by.items()},
}
with open(os.path.join(OUT, "classification.json"), "w", encoding="utf-8") as f:
    json.dump(cls, f, ensure_ascii=False, indent=1)
print(f"\n[OK] wrote classification.json")
