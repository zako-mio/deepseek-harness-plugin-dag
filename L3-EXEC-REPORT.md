# L3 执行报告 · 其余插件 DAG 分析（2026-08-17）

## 1. 当时情况

deepseek-harness 基于 cordis 插件机制 + 单向依赖 DAG 拼接。用户以**官方基础插件为最小分析单元**理解 harness 装配，分三层上下文窗口执行：
- L1 核心集（base bundle 76 插件 + 36 seam）✅ 已完成
- L2 web-app bundle（58 插件）✅ 已完成 → `0816-plugin-dag/`
- **L3 其余插件（本轮）**

上轮已落盘：`PLAN-layer3.md`（56 包三分法：39 插件 / 13 seam / 4 特殊模块）、`stage-00-l3-inventory.json`、13 seam 追加至 external-seams.json、`L3-DELEGATE-PROMPTS.md`（子Agent 委派模板）。本轮从 S1 采集续跑。

## 2. 制定计划

Plan 阶段（Grill-Me 协议）确认两项决策：
1. **执行范围**：完整 S1-S7 全流程
2. **drawio 范围**：与 L2 完全一致（每插件内部结构图，非仅组级图）

执行管线（复用 L2 资产改造）：
- S1 采集：5 路 explore 并行（G30 外部执行后端 / G31+G32+G33 协议LSP子代理 / G34+G35 Web上下文会话存储 / G36+特殊模块 / G37 示例框架）
- S2 建模：build-dag-l3.py（读 webapp-dag.json + L3 采集 → 合并 173 节点）
- S3 交互图：inject-data-l3.py（37 组 + 49 seam 注入 index.html）
- S4 插件页：gen-html-l3.py（39 L3 页 + 8 组页 + 特殊模块页）
- S5 drawio：4 批 drawio-worker 并行（强制加载 drawio-reference）
- S6 门控：quality-gate-l3.py ALL PASS + headless/VLM
- S7 收尾：README + PLAN-layer4.md + 留档 + Reflection

## 3. 执行情况

**S1 采集（5 路并行）**：全部 success。关键发现：
- R1：仅 dsh-host-directory-picker 系经 web-app bundle 间接装配；其余 8 插件无 bundle 装配（E3 无）
- R2：dsh-sdk-protocol 3 个 referred_by、dsh-lsp 2 个；**subagent-acp 走外部 @agentclientprotocol/sdk 而非 dsh-acp seam**
- R3：10 插件全部无下游（L3 扩展点）；web 搜索变体以 E1 依赖 dsh-web seam
- R4：native-command 为纯库（非插件）；4 特殊模块结构分析完成
- R5：示例包依赖浅；native-command 与 R4 重复（S2 去重）

**S2 建模**：build-dag-l3.py 产出 **173 节点 / 545 边 / 17 层 / 37 组 / 无环**。发现 seam referred_by 缺口（R2 的 7 项只覆盖本路），写 update-l3-seams.py 扫描全部采集补回 **89 条**引用（dsh-hook-protocol 2 / dsh-e2b 2 / dsh-terminal 3 / dsh-acp 1 等补全）。

**S3 交互图**：注入 DATA（173 插件 + 49 seam + 778 边 + 161 组边 + 38 组节点）；图例静态文字 29→37 组更新。

**S4 插件页**：gen-html-l3.py 生成 173 插件页 + 49 seam 页 + 37 组页 + 4 特殊模块页。

**S5 drawio**：4 批委派全部 success，39 张结构图 + PNG（l3-execution/l3-host/l3-sdk-lsp/l3-subagent/l3-web-context/l3-session/l3-hooks/l3-examples 8 域），VLM 抽验中文完整无截断。

**S6 门控**：首跑抓出 **78 条断链**——根因是特殊模块页（08-special-modules/）的 link_plugin 相对路径错误（同目录 vs ../02-plugin-pages/）。修复后复跑 **ALL PASS**（0 error / 0 warning）。headless + VLM：组级 38 节点、G30 下钻 23 节点、G37 下钻 36 节点，中文渲染完整。

**S7 收尾**：README 更新为 L1+L2+L3 完成态 + 关键发现；PLAN-layer4.md 落盘（第四层候选方向 + 坑经验）。

## 4. 完成情况

| 交付物 | 数量 | 状态 |
|--------|------|------|
| webapp-dag.json | 173 节点 / 545 边 / 17 层 / 37 组 | ✅ 无环 |
| external-seams.json | 49 seam（referred_by 全量回填） | ✅ |
| stage-01-l3-r1~r5.json | 5 路采集 | ✅ |
| 02-plugin-pages/ | 222 页（173 插件 + 49 seam） | ✅ |
| 03-groups/ | 37 组页 + 目录 | ✅ |
| 08-special-modules/ | 4 页（base/headless/app-boot/cmdline） | ✅ |
| 04-interactive/index.html | 38 组节点 + 下钻 | ✅ VLM 验证 |
| 05-drawio/ | 39 张 L3 图 + PNG（全量 174） | ✅ |
| quality-gate-l3.py | ALL PASS | ✅ |
| README.md / PLAN-layer4.md | 更新完成 | ✅ |

**改动明细**（脚本）：build-dag-l3.py / update-l3-seams.py / verify-l3-dag.py / inject-data-l3.py / gen-html-l3.py / quality-gate-l3.py / headless-verify-l3.py（全部在 07-checkpoint/）。
**子Agent 委派**：5 路 explore（S1）+ 4 批 drawio-worker（S5）= 9 个任务。

## 5. 反思/分析/建议

**过程反思**：
1. **门控提前抓断链价值大**：78 条断链若靠人眼几乎不可发现（特殊模块页路径错误），质量门控脚本是 L2 留下的最高价值资产
2. **seam 回填需跨路扫描**：采集端 seam_referred_by 只覆盖本路，跨路引用（hooks→hook-protocol 等）必须靠全量 depends_on 扫描补回——这是 L3 新增的认知
3. **重复采集处理**：R4/R5 对 native-command 重复，build 脚本用"keep first + merge dependents"去重，比人工去重可靠

**经验教训**：
- 特殊模块页（子目录）与插件页（同级目录）的链接前缀必须区分（`../02-plugin-pages/` vs 同级）——路径上下文 bug 高发区
- L3 插件多为叶子（G34/G35 全部无下游），drawio 下游泳道用"无下游"占位块处理，避免空泳道误解

**未来改进建议**：
1. 06-md/ AI 检索镜像仍停留在 L1/L2，未含 L3 39 插件（PLAN-layer4.md 方向 A，推荐优先补）
2. 49 个 seam 中 ref_count 高的（dsh-invariants 63 次）可画聚合星型依赖图
3. 三层窗口全量闭环（219/219 包），PACKAGE-MAP 比对可复用为多窗口任务的完成度度量
