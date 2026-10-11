# dsh-client-ui-dockkit

- 包名: `@deepseek-ai/dsh-client-ui-dockkit`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 1
- 来源层: L3 其余
- 源码路径: `packages/client/ui-dockkit`

## 实现逻辑
零 cordis 的停靠布局套件（静态库，非插件）：engine 层是纯 TypeScript 的拆分树模型与可逆操作（applyOp/replay、Sequencer、DockController）以及约束、几何与意图规划函数（src/index.ts:26-59）；组件层只渲染布局快照并上报每次手势的最终意图，使嵌入方的序列保持单一真相源（src/index.ts:1-18、src/index.ts:64-70）。包内不含宿主概念，渲染字符串经 DockLabels、标签体经 TabRenderer 注入，标签 kind 由调用方解释（src/index.ts:13-16）。

## Provides
- DockSurface/FloatLayer 等停靠布局 React 组件 (src/index.ts:65-70)
- 纯 TS 布局引擎导出（applyOp/replay、Sequencer、DockController、planner 函数）(src/index.ts:26-59)

## Depends On (上游依赖)
- `dsh-client-ui-primitives` [编译依赖] - 复用菜单、图标与工具提示等基础控件
  - 证据: `src/components/TabPanel.tsx:26 import + src/components/TabMenu.tsx:17 import`

## Dependents (下游被依赖)
- `dsh-client-ui-deliverables` - 复用停靠布局控件渲染比较视图
- `dsh-client-ui-sidebar-browser` - 标签身份与停靠面板 id 使用 dockkit 的 TabId 类型
- `dsh-client-ui-sidebar-documentpreview` - 标签生命周期与 TabId 身份来自 dockkit
- `dsh-client-ui-sidebar-files` - 标签身份与停靠面板 id
- `dsh-client-ui-sidebar-right` - 标签停靠、拆分面板与历史记录由 dockkit 纯规划函数计算
- `dsh-client-web` - 种子静态模块表内联 dockkit 布局库
