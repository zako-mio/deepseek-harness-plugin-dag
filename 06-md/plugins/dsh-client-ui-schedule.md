# dsh-client-ui-schedule

- 包名: `@deepseek-ai/dsh-client-ui-schedule`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-schedule`

## 实现逻辑
以一份 Host 任务目录 CatalogSource 为中心：manager 读 remote.schedule.catalog / delete 并订阅 schedule/changed 与 connection/reset（src/client/index.ts:96-104），删除结果经 shell.overlay 的全局 toast 播报（index.ts:112）。apply 注册日程任务 tab 页型与侧栏 detail 页（index.ts:155-166）、main 面板 'schedules' 与侧栏入口（index.ts:168/178），并注册 scheduleTurnDefinition 让 schedule_create 的产物在 Turn 末尾以卡片呈现（index.ts:188-205）。会话头部 utilities 用每 Session 的独立 source 列活跃提醒（index.ts:208-229），sidebar.session.row.leading/hover 则投影共享目录给工作区行标记与悬浮列表（index.ts:231-241）。任务创建卡另经 schedule_create 结果与右栏 detail 绑定（schedule-turn.ts / task-tab-bindings.ts）。

## Provides
- main 面板 'schedules'（TaskManagerPage 任务管理页）+ sidebar.panellist 条目 TaskManagerIcon
- ctx.sidebarRightTabs 的日程任务页型 + sidebar.right.pane.tab / pane.tab.title 的任务详情页与标题
- conversation.session.header.utilities 条目 'schedule-catalog'（会话头部提醒目录与删除）
- conversation.chat.turnTail 条目 'schedule-created'（schedule_create 结果卡）
- sidebar.session.row.leading 条目 'schedule-mark' 与 sidebar.session.row.hover 条目 'schedule-tasks'（会话行任务标记与悬浮列表）
- shell.overlay 条目 'schedule.delete-toast'（全局删除结果提示）

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - ctx.remote 与 Remote 事件面
  - 证据: `src/client/index.ts:41 import + src/client/index.ts:93 ctx.remote`
- `dsh-api-session-controller` [E1+E2] - 会话定位与打开状态判定
  - 证据: `src/client/session-link.ts:2 import + src/client/index.ts:136 ctx.sessions`
- `dsh-api-workspace-controller` [编译依赖] - 工作区状态以判定会话是否可跳转
  - 证据: `src/client/session-link.ts:3 import`
- `dsh-client-connection` [编译依赖] - 连接世代相关类型面
  - 证据: `src/client/index.ts:42 import type {}`
- `dsh-client-locale` [运行时依赖] - 注册 schedule.catalog 与 schedule.manager 文案
  - 证据: `src/client/index.ts:32 import + src/client/index.ts:89-90 ctx.locale.register`
- `dsh-client-ui-conversation` [运行时依赖] - 注册 Turn 级日程定义并渲染 Turn 末尾卡
  - 证据: `src/client/index.ts:33 import type + src/client/index.ts:188 ctx.uiConversation.events.register`
- `dsh-client-ui-layout` [E1+E2] - 读主面板选择并复用布局类型
  - 证据: `src/client/index.ts:40 import type + src/client/DeleteToast.tsx:13`
- `dsh-client-ui-primitives` [编译依赖] - 复用按钮/图标/toast 等控件
  - 证据: `src/client/CatalogFeedback.tsx:3 import + src/client/DeleteToast.tsx:11`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 槽注册表
  - 证据: `src/client/index.ts:34 import type + src/client/index.ts:87 inject 'slots'`
- `dsh-client-ui-session` [编译依赖] - Session 标准来源类型面
  - 证据: `src/client/index.ts:35 import type {}`
- `dsh-client-ui-sidebar` [运行时依赖] - 向侧栏面板列表注册任务入口
  - 证据: `src/client/index.ts:36 import type + src/client/index.ts:178 slots.inject('sidebar.panellist')`
- `dsh-client-ui-sidebar-right` [运行时依赖] - 注册任务详情页型并打开详情 tab
  - 证据: `src/client/index.ts:37 import type + src/client/index.ts:153 ctx.sidebarRight.tabsIn`
- `dsh-client-ui-tool` [编译依赖] - 复用工具视图类型/卡片
  - 证据: `src/client/index.ts:38 import type + src/client/ScheduleCreateCard.tsx:3`
- `dsh-client-ui-workspace` [运行时依赖] - 从任务卡跳转到原始会话
  - 证据: `src/client/index.ts:39 import type + src/client/index.ts:137 ctx.uiWorkspace.openSession`
- `dsh-schedule` [E1+E2] - 读/写/删 Host 日程任务与投递历史
  - 证据: `src/client/index.ts:44 import + src/client/index.ts:97 ctx.remote.schedule.catalog()`
- `dsh-session` [编译依赖] - 会话身份与 surface 类型
  - 证据: `src/client/index.ts:43 import type + src/client/schedule-turn.ts:12 import surface`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
