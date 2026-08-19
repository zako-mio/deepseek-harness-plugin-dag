# 任务完成报告 · dsh DAG 知识库 RC5 → RC7 级联升级

> 任务日期：2026-08-19 ｜ 任务目录：`/home/zako-mio/opencode/archive/Mission-file/2026-08/0819-plugin-dag-rc7/`
> 源知识库：`0816-plugin-dag`（RC5 版本，保留原版）

---

## 一、当时情况

用户提出 DeepSeek Harness（dsh）已从 RC5 更新到 RC7，要求将插件级 DAG 知识库（`0816-plugin-dag`，基于 RC5）级联升级到 RC7：查阅官方更新文档、分析差异点、级联更新 DAG 图集合与被修改的对应插件页面和内容，并对比最新版源码验证确实正确（必须用纯官方版源码，不用魔改版）。

环境：WSL2 / Ubuntu，工作目录 `/home/zako-mio/opencode/`。本地 `dsh/` 为 RC5 快照（无 git），官方仓库 `deepseek-ai/deepseek-harness`。

## 二、制定计划

经 Grill-Me 收敛，确认以下方案：
1. **RC7 源码**：下载官方 tarball（`dsh-v0.1.0-rc.7.tar.gz`），存留档目录 `05-source/dsh-rc7/`
2. **更新深度**：增量更新受影响插件 + 全量质量门控（非全量重建）
3. **目录策略**：新建 `0819-plugin-dag-rc7`，保留 `0816-plugin-dag`（RC5）原版
4. **差异分析**：完整 diff（111 commits）+ release notes + packages 目录对比三路交叉验证，生成独立差异报告
5. **drawio**：仅受影响插件图（后改为**完全移除**，见执行情况）
6. **验证**：RC7 源码三依据重验 + headless/VLM
7. **上传**：整个目录 push 到 `zako-mio/deepseek-harness-plugin-dag` master

## 三、执行情况

**阶段0 前置**：复制 `0816-plugin-dag` → `0819-plugin-dag-rc7`（保留 RC5 原版）

**阶段1 差异分析**（委派 explore）：
- 官方 diff：RC5→RC7 共 **111 commits**
- packages 结构：219=219，**无新增/删除包**
- **26 个源码实质变化包** + 5 个仅 tests 变化包 + ~188 个仅版本号变化包
- **2 处依赖变化**：acp（+attachment+llm）、mcp-client（+attachment）
- cordis.patch.yml 三文件字节级一致，**装配位置零变化**
- 委派 explore 子Agent 对 26 包逐条提取变更要点（中文，含证据行引用）

**阶段2 RC7 源码**：wget/curl 下载官方 tarball（13.8MB，经 codeload 直连），解压验证 `0.1.0-rc.7`，复制到 `05-source/dsh-rc7/`（5319 文件）

**阶段3 数据更新**（委派 general）：
- external-seams.json：attachment referred_by 4→6（+acp、+mcp-client）
- webapp-dag.json：20 个节点内容按 RC7 更新 + 7 处版本标注 rc.5→rc.7
- 14 个 HTML/MD 文件版本标注 rc.5→rc.7

**阶段4 页面重生成**（委派 general）：
- 路径适配：46 个 07-checkpoint 脚本 Windows 路径 → Linux 路径
- 重跑 gen-html-l3 / gen-md-l3 / gen-plugin-dyn / gen-overview / inject-data-l3
- 221 插件页 + 38 组页 + 交互图 + 221 MD + 4 特殊模块全部生成

**阶段4d Chrome 代理**：drawio-worker 需 Chrome 导出 PNG，WSL2 缺 Chrome。注入 Linux Chrome 路径（`/home/zako-mio/.agent-browser/browsers/chrome-152.0.7977.42/chrome`）到 drawio-mcp export.js，实测导出成功。`app.diagrams.net` 直连可达，无需额外代理。

**阶段4e drawio 完全移除（用户中途决策）**：
- 用户明确"完全移除该项目的 drawio 绘制的图片本身，只需要 HTML 的动态图"
- 删除 `05-drawio/`（348 文件：174 drawio + 174 png）
- 同步更新 README.md、index.html、REPORT.md、L3-EXEC-REPORT.md 的 drawio 引用
- 同步移除 quality-gate-l3/l2/gate.py 的 drawio 校验步骤
- **修复交互图 2 个 bug**：
  1. gen-overview.py 模板漏引 cytoscape-dagre.min.js → 交互图无法渲染（"No such layout 'dagre'"）→ 已补
  2. 样式选择器 `node.plugin`（class）与实际 data.kind 不匹配 → 改为 `node[kind="plugin"]`（属性选择器），disabled 插入标记同步修正

**阶段5 质量门控**：`quality-gate-l3.py` **ALL PASS**（JSON/DAG无环173/HTML断链0/vendor/插件页覆盖/DATA校验/MD覆盖，0 错误 0 警告）

**阶段6 验证**（headless + VLM）：
- 交互图组级 38 节点渲染正常，右侧统计（173/49/37）完整，中文完整无截断
- 插件页 dsh-llm 内嵌动态 DAG 正常，RC7 内容（ReplayEnvelope、max-tokens）正确呈现
- 修复交互图选择器 bug 后重验：无 pageerror，canvas 1440x844，组级 38 节点

**阶段7f 交互图重构（用户反馈卡顿）**：
- 用户指出：主 DAG 应始终是组级视图，点进去是单独的组内视图；且原实现缩放切换导致卡顿
- 原实现缺陷：`modeFromZoom(k)` 靠滚轮缩放 k≥0.9 切到插件级（173 节点全渲染）+ `cy.on('zoom')` 每次缩放触发重建 → 卡顿
- 重构：**始终组级视图**（38 组），点击组节点进入**独立组内视图**（该组插件 + 上下游 stub 灰显），提供"← 返回组级视图"按钮；移除 zoom 事件触发的视图切换
- 暴露 `window.__cy` 便于调试
- headless 验证：组级 38 节点 → 点击 G01 → 组内视图 4 节点（hmr/include/loader/timer）+ 依赖边 → 返回组级正常，无 pageerror 无卡顿

**阶段7g 删除过时遗留计划文档（用户要求）**：
- 删除 9 个过时遗留文档：PLAN-layer2-prompt.md、PLAN-layer2-webapp.md、PLAN-layer3.md、PLAN-layer4.md、L3-DYN-DAG-REPORT.md、L3-EXEC-REPORT.md、L3-MD-COMPLETION-REPORT.md、REPORT.md、执行报告-0817经验迁移优化.md
- 保留当前有效文档：README.md、index.html、RC5-RC7-DIFF-REPORT.md、report.md、report.html

**子Agent 委派**：explore（差异分析）×1 + general（数据更新）×1 + general（页面重生成）×1 + drawio-worker（drawio，后取消）+ 多轮验证脚本

## 四、完成情况

**交付物清单**（`0819-plugin-dag-rc7/`）：
| 交付物 | 数量 | 说明 |
|--------|------|------|
| 02-plugin-pages/ | 221 页 | 173 插件 + 49 seam - 1 双身份，含内嵌动态 DAG |
| 03-groups/ | 38 页 | 37 组 + 目录 |
| 04-interactive/index.html | 1 | cytoscape 交互图（组级+下钻+disabled 标注） |
| 06-md/ | 221 MD | AI 友好镜像 |
| 08-special-modules/ | 4 页 | base/headless/app-boot/cmdline |
| 01-dag-data/ | 3 JSON | webapp-dag + external-seams + core-dag |
| 05-source/dsh-rc7/ | 5319 文件 | 纯官方 RC7 源码 |
| RC5-RC7-DIFF-REPORT.md | 1 | 差异分析报告（本任务新增） |
| 07-checkpoint/ | — | 生成脚本（路径已适配 Linux） |
| ~~05-drawio/~~ | ~~348~~ | **已完全移除**（用户决策） |

**验证结果**：
- 质量门控 ALL PASS
- headless + VLM：交互图 + 插件页动态 DAG 渲染正常
- RC7 源码三依据重验通过（26 包逐条核对官方源码）

**改动明细**：
- 数据：external-seams.json、webapp-dag.json
- 页面：02-plugin-pages/、03-groups/、04-interactive/、06-md/、08-special-modules/ 全量重生成
- 脚本：46 个 07-checkpoint 脚本路径适配；gen-overview.py + inject-data-l3.py 修复选择器 bug；quality-gate*.py 移除 drawio 校验
- 文档：README.md、index.html、REPORT.md、L3-EXEC-REPORT.md 更新 drawio 移除；新增 RC5-RC7-DIFF-REPORT.md

## 五、反思/分析/建议

1. **版本升级方法论**：RC5→RC7 虽 111 commits，但真正的源码变化集中在 26 包（12%），其余为批量版本号升级。先做 packages 目录结构 diff（快速排除 188 包）+ 源码文件 diff（定位 26 包），再深入分析，避免全量重建的无效消耗。此方法可复用于后续 RC8+ 升级。
2. **版本标注 vs 历史记录**：知识库中 `0.1.0-rc.5` 是"当前版本"标注（需更新为 rc.7），而 `0.0.1-rc.1/rc.3/rc.6` 是各包历史演进记录（保留）。更新时需区分"当前版本"与"历史版本"，不能一刀切全局替换。
3. **drawio 完全移除**：用户最终决策只需 HTML 动态图。交互图（cytoscape）+ 插件页内嵌动态 DAG 已完全自包含（数据内嵌 DATA），不依赖外部图片文件。移除 drawio 后需同步更新 README/index/门控/报告，避免残留引用。
4. **选择器 bug 教训**：交互图 gen-overview.py 用 `node.plugin`（class 选择器）但节点 data 是 `kind:'plugin'`，二者不匹配导致样式不生效且门控"样式选择器缺失"。headless 验证是唯一能发现此渲染 bug 的手段（静态检查看不出来）。验证交互图必须 headless 渲染 + DOM 检查 + VLM 三重确认。
5. **WSL2 Chrome 导出**：drawio-mcp 的 findSystemBrowser 只查 Windows 路径，WSL2 下找不到 Chrome。注入 Linux Chrome for Testing 路径即可复用既有导出链路，`app.diagrams.net` 直连可达无需代理。
6. **残留清理**：任务完成需清理 /tmp 及临时目录残留（MEMORY 原则）。
