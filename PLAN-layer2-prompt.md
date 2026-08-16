# 第二层执行启动 Prompt（复制本文件内容给下一轮 Agent）

## 任务

继续 deepseek-harness 插件级 DAG 依赖链分析的**第二层（L2：web-app bundle）**。

> 第一层（L1 核心集）已完成，所有资产在 `D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag\`。

## 必读文档（按顺序）

1. **`D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag\PLAN-layer2-webapp.md`** ← 最重要，完整第二层计划（范围/复用资产/执行步骤/坑经验）
2. `D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag\README.md` — 第一层成果总览
3. `D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag\01-dag-data\core-dag.json` — 第一层 DAG 数据（76 节点 schema）
4. `D:\Opencode_Download\Mission-file\2026-08\0816-plugin-dag\01-dag-data\external-seams.json` — 36 外部 seam
5. 源码仓库：`D:\Opencode_Download\Mission-file\2026-08\0814-deepseek-harness源码解析\01-source-clone\packages\bundle\web-app\cordis.patch.yml` — L2 装配清单
6. `D:\Opencode_Download\Mission-file\2026-08\0814-deepseek-harness源码解析\07-checkpoint\PACKAGE-MAP.json` — 包路径映射

## 初步计划（高层）

| Stage | 内容 |
|-------|------|
| S0 | 提取 web-app/cordis.patch.yml 装配行 → 与 PACKAGE-MAP 核验 → 按域分组（宿主服务/客户端 runtime/UI 域） |
| S1 | 委派 3-4 路 explore 子Agent 三依据采集（宿主层 / client runtime / UI 大包 / UI 小包） |
| S2 | 复用 build-dag.py 建模：L2 插件 + L1 节点合并扩展 DAG，层次遍历重算拓扑层 |
| S3 | 复用 inject-data.py 更新交互图 DATA（新交互方案：组级+点击下钻） |
| S4 | 复用 gen-html.py 生成 L2 插件页（链接 L1 已分析插件，勿重复采集） |
| S5 | drawio-worker 分 2 批绘制 L2 插件内部图 |
| S6 | 复用 quality-gate.py 全量门控 ALL PASS |
| S7 | 更新 README + 生成 PLAN-layer3.md + 留档询问 + Reflection |

## 关键约束

- **三硬依据**：E1 编译 / E2 运行时 / E3 组合，每条依赖带源码行引用
- **层次遍历**：DAG 结构化用拓扑分层 BFS（被依赖方先于依赖方）
- **交互图已定稿**：组级视图 + 点击下钻（不要改回缩放联动）
- **cytoscape 配色**：样式必须用**数据属性选择器** `node[kind="plugin"]` / `edge[kind="seam"]`，不用类选择器（`node.plugin` 需要 classes 字段，缺失则全部不命中 → 节点白色无配色）
- **python -c 被禁**：脚本写成独立 .py
- **质量门控**：quality-gate.py 必须 ALL PASS 才算完成
- **交接文件**：完成前必须落盘 PLAN-layer3.md

## 完成后核对（验收清单）

- [ ] 交互图 DATA 含 L2 插件，组级视图彩色（每组颜色不同）+ 下钻视图插件按组配色
- [ ] headless Chrome `--screenshot` + VLM 验证：组级 25+ 节点、下钻节点非 0、配色正确
- [ ] L2 插件页全部生成，依赖链接指向 L1 已分析插件（不重复采集）
- [ ] quality-gate.py ALL PASS
- [ ] PLAN-layer3.md 已落盘
- [ ] 已向用户发起留档询问（5 段模板）

## 完成后产出

- L2 插件页 + 交互图扩展 + drawio + MD 镜像
- PLAN-layer3.md（第三层接力）
- 留档询问（5 段模板）
