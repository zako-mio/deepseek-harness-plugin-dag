# dsh-client-ui-dockkit

- 包名: `@deepseek-ai/dsh-client-ui-dockkit`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 1
- 来源层: L3 其余
- 源码路径: `packages/client/ui-dockkit`

## 实现逻辑
零 cordis 的停靠布局库：引擎层是纯 TS——applyOp/replay 与 Sequencer 记录可逆布局操作，DockController 每个方法都是 planner 调用加记录加一次通知，getSnapshot 的引用只在布局变化时改变 (src/engine/controller.ts:1-14, 54-80; src/index.ts:26-59)。组件层渲染布局快照并只回报每次手势的 settled intent，tab 的 kind 是不透明字符串，宿主概念（DockLabels/TabRenderer）全部由嵌入方注入 (src/index.ts:1-18, 62-70)。包内不注册任何槽位、没有 apply，只被其他客户端包以引擎/组件 API 消费。

## Provides
- 引擎 API：applyOp/replay、Sequencer/record/stepBack/stepForward/canStepBack/canStepForward、tree 查询 (getNode/getPane/findTabPane 等)
- 约束与几何：canSplit/clampSizes/DOCK_ZONES/MAX_DOCK_PANES、containsPoint/dividerSizes/floatRectAt/SPLIT_MINIMUMS
- 意图规划纯函数：planAddTab/planDropTab/planSplitPane/planResizeSplit/planFloatTab/planOpenContent 等
- DockController (每停靠面的状态化嵌入，subscribe+getSnapshot 可观察快照) 与 createIdMinter/createInitialState
- React 组件 DockSurface/DockLayout/FloatLayer 及外向契约 DockIntents/DockLabels/TabRenderer/TabMenuExtras
- 类型 LayoutState/LayoutOp/DockZone/PaneId/SplitId/TabId/LayoutNode 等

## Depends On (上游依赖)
- `dsh-client-ui-primitives` [编译依赖] - 菜单/面板等基础组件
  - 证据: `src/components/FloatLayer.tsx:19 + src/components/TabMenu.tsx:17-21 + src/components/TabPanel.tsx:26`

## Dependents (下游被依赖)
- `dsh-client-ui-deliverables` - review tab 的 TabId 类型
- `dsh-client-ui-sidebar-browser` - 复用 dock 标签/布局原语
- `dsh-client-ui-sidebar-documentpreview` - 标签生命周期与 dock 原语
- `dsh-client-ui-sidebar-files` - 标签/dock 原语
- `dsh-client-ui-sidebar-right` - dock 布局/标签 id 与纯规划器
- `dsh-client-web` - 种子静态模块表内联 dockkit 布局库
