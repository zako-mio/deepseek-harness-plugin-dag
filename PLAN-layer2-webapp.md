# PLAN · 第二层：web-app bundle（宿主层 + 前端 runtime + ui-* 包）

> 本文件为**落盘接力文件**：第一层核心集（0816-plugin-dag）已完成，新窗口打开本文件即可续跑第二层。
> 生成日期：2026-08-16

## 任务背景

deepseek-harness 基于 cordis 插件机制 + 单向依赖 DAG 拼接。用户要以**官方基础插件为最小分析单元**，理解插件如何一步一步拼接成完整 harness。分三层执行，每层一个上下文窗口：
- L1 核心集（base bundle）✅ 已完成 → 本任务目录 `0816-plugin-dag/`
- **L2 web-app bundle（本计划）**
- L3 其余插件（examples/hooks/web 变体/e2b/lsp/mcp）

## L2 范围

web-app bundle（`packages/bundle/web-app/cordis.patch.yml`）在 base 之上追加装配的插件：

**宿主层 + 服务（约 15）**：
dsh-code-runtime-worker-thread, dsh-storage, dsh-storage-json, dsh-storage-domain, dsh-message-feedback, dsh-session-log-export, dsh-workspace, dsh-session-projection-cache, dsh-session-stats, dsh-host-directory-picker-auto, dsh-host-plugin-inventory, dsh-host-apiproxy, dsh-cordis-host-runner, dsh-host-webserver, dsh-web-app

**客户端 runtime（约 10）**：
dsh-client-hmr, dsh-client-modules, dsh-client-connection, dsh-api-remotes, dsh-client-runtime, dsh-cordis-client-runner, dsh-client-locale, dsh-client-web, dsh-client-web-react, dsh-agent-presets

**UI 包（30+）**：
dsh-client-ui-theme, ui-layout, ui-sidebar, ui-settings, ui-settings-general, ui-settings-models, ui-settings-plugin-inventory, ui-conversation, ui-tool, ui-cordis, ui-workflow-run, ui-deliverables, ui-workspace, ui-input-trigger, ui-commands, ui-skill, ui-subagent, ui-jobs, ui-goal, ui-message-feedback, ui-model-selection, ui-permission-presets, ui-agent-preset, ui-settings-plugins, ui-plan, ui-user-questions, ui-trajectory, ui-directory-picker-browse, ui-directory-picker-native, ui-attachment, ui-primitives, ui-slots, schema-form, ui-tool...

## 复用上一轮资产（关键！）

### 数据接口
- `01-dag-data/core-dag.json`：76 节点 / 194 边 / 8 拓扑层 / 24 组。schema：`nodes[{id,name,group,group_name,layer,implementation,provides,path}]` + `edges[{from,to,mechanism,evidence,purpose}]` + `groups[{id,name,plugins[]}]` + `layers{"0":[ids],...}`
- `01-dag-data/external-seams.json`：36 外部 seam 包（path/description/ref_count/referred_by/mechanisms）
- 第二层插件若引用 L1 已分析的插件（如 ui-conversation 依赖 dsh-session/dsh-llm），直接链接到 `../02-plugin-pages/{id}.html`，**不要重复采集**

### 生成管线（可直接复用）
- `07-checkpoint/build-dag.py`：DAG 建模（无环校验 + 层次遍历拓扑分层）
- `07-checkpoint/gen-html.py`：插件页 + 组索引页生成（DAG 链式双导航）
- `07-checkpoint/gen-overview.py`：交互总览页生成
- `07-checkpoint/gen-md.py`：MD 镜像生成
- `07-checkpoint/quality-gate.py`：质量门控（JSON/DAG 无环/HTML div/断链/drawio/vendor/覆盖）
- `04-interactive/vendor/`：cytoscape.min.js + **cytoscape-dagre.min.js**（⚠️ dagre 必须加载，否则布局抛错节点 0）

## 执行步骤

### S0 清单
- 从 `packages/bundle/web-app/cordis.patch.yml` 提取装配行（grep `name: '@deepseek-ai/`）
- 与 PACKAGE-MAP.json 交叉核验路径
- 按域分组（宿主服务 / 客户端 runtime / UI 域）

### S1 采集
- 委派 3-4 路 explore 子Agent（宿主层 / 客户端 runtime / UI 大包 / UI 小包），三依据分析
- **UI 包注意**：多为 React 组件注册（ConversationEventRegistry/SlotRegistry keyed renderer），依赖方向是「UI 依赖 host 的服务与事件契约」，证据以 import + ctx 远程调用为主

### S2 建模
- 复用 build-dag.py：L2 插件 + L1 已有节点合并成**扩展 DAG**（L2 插件指向 L1 插件的前驱边保留）
- 新增外部 seam 若已存在不重复
- 层次遍历重算拓扑层（L2 大多在高层）

### S3 交互图
- 直接改 `04-interactive/index.html` 的 DATA 注入（或重新 inject-data.py），节点增至 76+L2
- **新交互方案（2026-08-16 定稿）**：已放弃缩放倍率动态切换细粒度（性能差），改为**固定两级视图 + 点击下钻**：
  - 组级总览（默认，25 节点：24 组 + EXT）→ 点击组节点 → 组内插件 DAG（组内边 + 跨组 stub 节点灰显可跳转）
  - 面包屑返回 + hash 路由（`#G03`）+ query param（`?drill=G03`）
  - 侧栏组配色可点击下钻
  - 验证：headless Chrome 截图确认（组级 25 节点 / `?drill=G03` 下钻节点 62）
- L2 扩展时：DATA 注入用 `07-checkpoint/inject-data.py`（从 core-dag.json + external-seams.json + L2 数据生成完整 DATA）
- ⚠️ 布局注意：cytoscape 渲染在 canvas，headless `--dump-dom` 只能验证 DOM 文本（zmode/zcount），真实渲染验证用 `--screenshot` + VLM 看图

### S4 插件页
- 复用 gen-html.py：L2 插件页 + 更新总览
- UI 包路径用 `packages/client/ui-xxx`

### S5 drawio
- 委派 drawio-worker 分 2 批（宿主+client runtime / UI 包），drawio-reference 强制加载

### S6 门控
- quality-gate.py 必须 ALL PASS

### S7 接力
- 更新 README + 生成 PLAN-layer3.md

## 坑与经验（来自 L1 + 交互图重构）

1. **cytoscape-dagre 必须 vendor**：cytoscape 核心不内置 dagre 布局，缺它 `layout:{name:'dagre'}` 抛错 → 节点 0。已 vendor 到 `04-interactive/vendor/cytoscape-dagre.min.js`
2. **交互图性能**：不要用 zoom 事件做模式切换（每次缩放都重建全图，卡顿）。**点击下钻两级视图**最稳（组级 → 组内子图，仅构建当前组 ~60 节点）
3. **重复 showGroupView 陷阱**：重构时文件末尾遗留的无条件 `showGroupView()` 会覆盖 query/hash 下钻（下钻永远不生效）。改动后务必检查是否有重复的初始化调用
4. **cytoscape 类选择器 vs 数据属性选择器**：`node.plugin` 类选择器要求节点元素带 `classes` 字段（构建时只给 `data` 会全部不命中 → 节点退化为默认白色，无配色）。**必须用数据属性选择器** `node[kind="plugin"]` / `edge[kind="seam"]` 等。配色函数 `DATA.groupColor[ele.data('group')]` 不变（2026-08-16 修复配色）
5. **组合引用规范化**：depends_on 里 `"a / b / c"` 或 `"a + b"` 组合引用必须拆分成多条，否则产生带空格的伪节点
6. **python -c 被禁**：所有分析脚本写成独立 .py 文件执行
7. **$PID 是 PowerShell 只读变量**：脚本内避免用作变量名
8. **质量门控排除 `../index.html`**：根入口由 README 阶段生成
9. **headless 验证方法**：`--dump-dom` 看 DOM 文本（zmode/zcount），`--screenshot` 看真实渲染（canvas）；截图字节大小变化可快速判断视图是否切换
10. drawio 导出 scale=2 而非 4（避免 Chromium 视口上限截断）；MCP drawio_export 可能挂起，用同源 exportDiagram() 直调
