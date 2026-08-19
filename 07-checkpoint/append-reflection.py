#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""追加 cycle-20260816-plugin-dag 到 pending.json (4层封装)"""
import json, os, io, sys

PENDING = r"D:\Opencode_Download\Reflection\pending.json"

new_cycle = {
    "id": "cycle-20260816-plugin-dag",
    "timestamp": "2026-08-16",
    "mission": "DeepSeek Harness 插件级 DAG 依赖链分析 - 第一层核心集",
    "status": "waiting",
    "layers": {
        "layer_a_gate": {
            "gate": "[GATE] 范围=5 深度=5 操作=5 风险=3 → 总分=18 → Deep",
            "complexity": 18,
            "decisions": [
                "范围=全量分层,本窗口核心集(base bundle 76插件),第二/三层后续窗口",
                "HTML导航=目录(树状分组)+DAG链式翻页双导航",
                "交付物=HTML(每插件≥1页)+MD镜像+drawio(每插件内部结构图)+交互DAG总览",
                "依赖依据=三硬依据(E1编译/E2运行时/E3组合)+源码行引用逐条溯源",
                "DAG粒度=24组(20-25区间),交互图缩放联动三级(组→插件),总览图只展示插件名与依赖",
                "交互图=cytoscape.js vendor本地+缩放联动+点击跳转;demo先行后铺开",
                "执行边界=本窗口完整执行核心集+制定第二层计划并落盘接力文件",
                "输出目录=新建 0816-plugin-dag 独立目录",
                "用户提醒=DAG结构化用层次遍历(拓扑分层BFS),已被采纳"
            ]
        },
        "layer_b_subagent_results": {
            "aggregate": "success",
            "stage0": "目录初始化+核心集清单(76插件/24组,与cordis.patch.yml 78行交叉核验无遗漏)",
            "stage1": "6路并行explore子Agent采集(核心服务/执行/交互状态/会话治理/子代理工作流/框架杂项),81插件条目全带文件:行号三依据",
            "stage2": "build-dag.py层次遍历拓扑分层:76节点/194边/8层/24组,无环校验通过;external-seams 36个(组合引用拆分修复)",
            "stage3": "cytoscape 3.30.2 vendor+交互图demo(llm→agent→tools→tool-fs链路);用户反馈节点0→定位cytoscape缺dagre布局扩展,vendor cytoscape-dagre 4.0.0修复,headless Chrome截图确认25节点渲染",
            "stage4": "gen-html.py生成112插件页(76核心+36seam)+24组索引+根入口,每页DAG链式双导航+层序翻页;gen-overview.py交互总览(112节点/333边/72组间边)",
            "stage5": "drawio-worker 4批生成78张内部结构图(核心12/执行13/交互21/治理12/子代理14/框架6),VLM抽验无截断,字体≥12pt,单图≤30节点,scale=2导出",
            "stage6": "MD镜像115文件(76插件+36seam+3索引);quality-gate.py全PASS(JSON合法/DAG无环/HTML 139页断链0/drawio 78张/vendor完整/覆盖76+36)",
            "stage7": "README+PLAN-layer2-webapp.md接力文件(数据接口+坑经验);留档已确认,Reflection写入"
        },
        "layer_c_memory_snapshot": "MEMORY.md 现有§:Reflection系统/中文偏好/编码安全/edit优先/Plan先探索/半自动留档/子Agent结构化JSON/Python脚本UTF-8/OpenCode配置路径/备份路径/MCP精兵策略/权限三层/Compaction阶梯式/plan与build prompt独立/全局MEMORY/Per-agent行为约束/auto-mode缓存前缀敏感/DeepSeek参数/DEEPSEEK_API_KEY环境变量/prefix-cache优化/recruit-assist复盘/browser-harness教训/opencode-config修正/多路并行领域分片检索/HTML双交付质量门控/多维权衡矩阵收敛选型法",
        "layer_d_archive_report": {
            "status": "已确认留档",
            "path": "/home/zako-mio/opencode/archive/Mission-file/2026-08/0820-plugin-dag-rc8",
            "summary": "第一层核心集插件级DAG分析:76核心插件+36外部seam+194边+8拓扑层+24组;交付112插件页HTML(每页实现逻辑+provides+上游/下游链式导航+源码引用)、交互DAG总览(cytoscape缩放联动+点击跳转,修复dagre缺失节点0bug)、78张drawio内部结构图、115文件MD镜像;质量门控ALL PASS;PLAN-layer2接力文件落盘供第二窗口续跑。全程委派子Agent执行(6路explore采集+4批drawio-worker),主Agent仅调度/聚合/建模/门控,含层次遍历拓扑分层与断链修复闭环。"
        }
    }
}

with open(PENDING, "r", encoding="utf-8") as f:
    pending = json.load(f)

# 防重复
for c in pending["cycles"]:
    if c["id"] == new_cycle["id"]:
        print("cycle already exists, skip")
        sys.exit(0)

pending["cycles"].append(new_cycle)
pending["meta"]["waiting_count"] += 1

# 原子写回
tmp = PENDING + ".tmp"
with open(tmp, "w", encoding="utf-8") as f:
    json.dump(pending, f, ensure_ascii=False, indent=2)
os.replace(tmp, PENDING)

print(f"[OK] appended cycle, waiting_count={pending['meta']['waiting_count']}")
