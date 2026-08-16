# PLAN · 第四层（如需）：L3 完成后的收尾与扩展

> 生成日期：2026-08-17 ｜ 上一窗口：L3（0816-plugin-dag）已完整交付，质量门控 ALL PASS。
> 本文件为**潜在后续方向**，非必须执行的计划。若用户要求继续深化，新窗口读取本文件 + README.md 即可启动。

## L3 交付确认（已完成）

- **173 节点 / 545 边 / 17 层 / 37 组**（L1 76 + L2 58 + L3 39）
- **49 外部 seam**（36 原有 + 13 L3 追加，referred_by 已全部回填）
- **4 特殊模块**独立分析（08-special-modules/：dsh-base/headless/app-boot/cmdline）
- **222 插件页 + 37 组页 + 4 特殊页 + 交互图**（组级 38 节点）
- **174 张 drawio**（含 L3 8 域：l3-execution/l3-host/l3-sdk-lsp/l3-subagent/l3-web-context/l3-session/l3-hooks/l3-examples）
- 质量门控 `quality-gate-l3.py` ALL PASS + headless/VLM 验证通过

## 56 包三分法完成度（PACKAGE-MAP 219 包全量覆盖）

| 类别 | 数量 | 状态 |
|------|-----|------|
| L3 插件节点 | 39 | ✅ 全部入 DAG（G30-G37） |
| 归入 seam | 13 | ✅ 全部追加 external-seams.json |
| 特殊独立模块 | 4 | ✅ 08-special-modules/ 分析 |
| **PACKAGE-MAP 覆盖** | **219/219** | ✅ 三层窗口全量闭环 |

## 第四层候选方向（按价值排序）

### A. 06-md/ AI 检索镜像补全（推荐）
- 现状：`06-md/00-index.md` 可能仍停留在 L1/L2 阶段，未含 L3 39 插件
- 动作：gen-md 脚本更新，为 L3 插件生成 MD 镜像（与 02-plugin-pages 对应）
- 价值：AI 检索覆盖面完整，低成本

### B. 特殊模块深化（可选）
- dsh-headless 是独立 bundle（有 cordis.patch.yml），可画装配结构图
- dsh-app-boot/dsh-cmdline 是 boot 层胶水，可补启动流程图

### C. seam 依赖图补充（可选）
- 49 个 seam 中 ref_count 高的（dsh-invariants 63 次）可画聚合依赖图
- 展示"抽象基座被多少实现包依赖"的星型结构

### D. 交互图增强（可选）
- 组级视图增加搜索/过滤功能
- 增加 L1/L2/L3 来源层切换过滤

## 若启动第四层

1. 新窗口读：`README.md` + `PLAN-layer4.md` + `07-checkpoint/quality-gate-l3.py`（门控基准）
2. 优先做 A（06-md 补全），一行 gen-md 脚本改造
3. 完成后重跑 `quality-gate-l3.py` 保持 ALL PASS
4. 留档询问 + Reflection 周期

## 坑与经验（L3 实证，第四层必读）

1. **特殊模块页相对路径**：`08-special-modules/` 内的链接必须 `../02-plugin-pages/{id}.html`，不是同目录 `{id}.html`（门控抓出 78 条断链的根因）
2. **seam referred_by 回填**：采集端 seam_referred_by 只覆盖本路插件；跨路引用需扫描全部 depends_on 累计（update-l3-seams.py 模式）
3. **native-command 去重**：R4/R5 重复采集，build-dag-l3.py 用"keep first + merge dependents"处理
4. **L3 插件多为叶子**：G34/G35 大量插件无下游，drawio 下游泳道用"无下游"占位块
5. **drawio 坐标语义**：子节点坐标为相对父容器坐标（coordtest 实证），非样本中的绝对值
