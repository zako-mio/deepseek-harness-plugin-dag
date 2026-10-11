# dsh-client-ui-schedule

- 包名: `@deepseek-ai/dsh-client-ui-schedule`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-schedule`

## 实现逻辑
浏览器侧计划任务插件。createCatalogSource 把 remote.schedule 的 catalog/list/delete 与 schedule/changed、connection/reset 收敛成一个可订阅目录源，并用 readRequest/readSettled 序号避免陈旧读被当作删除证据 (src/client/catalog-source.ts:3-51)。apply 先经 ctx.sidebarRightTabs.register 声明 scheduleTask 页类型 (src/client/index.ts:155, src/client/definition.ts:34-41)，再把任务管理主面板、侧栏面板图标、右侧栏任务页/标题、Turn 级卡片与删除 Toast 注册进各自槽 (src/client/index.ts:112-201)。会话头部条目持有 per-Session 的 schedule/list 源，而侧栏行标记与悬停卡共用同一 Host 目录源，使 N 个可见行只发一次查询 (src/client/index.ts:206-244, src/client/session-schedule-state.ts:31-41)。schedule_create 的结算结果由 Turn 级 Definition 从持久化结果 JSON 收窄后发布，经 conversation.chat.turnTail 渲染在收尾正文之下 (src/client/schedule-turn.ts:12-20, src/client/index.ts:188-201)。

## Provides
- 在 ctx.sidebarRightTabs 注册 scheduleTask 页类型（kind=scheduleTask，供 sidebarRight.openTab 打开单个任务详情）
- 右侧栏任务页的 key 契约 '@deepseek-ai/dsh-client-ui-schedule/task'（body 与 chip title 两个 seat 的 key）

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 目录与任务详情的一切读写都经 Remote 命名空间，并订阅其推送失效事件
  - 证据: `src/client/catalog-source.ts:3 import RemoteResult + src/client/index.ts:93 ctx.remote.schedule.catalog() + src/client/index.ts:99 ctx.remote.$on('schedule/changed')`
- `dsh-api-session-controller` [E1+E2] - 判断任务所属会话是否仍可打开（可用性判定读会话列表快照）
  - 证据: `src/client/session-link.ts:2 import SessionListState + src/client/index.ts:136 ctx.sessions.list.getSnapshot()`
- `dsh-api-workspace-controller` [E1+E2] - 同上，会话可用性还需工作区快照参与判定
  - 证据: `src/client/session-link.ts:3 import WorkspaceSnapshot + src/client/index.ts:136 ctx.workspaces.list.getSnapshot()`
- `dsh-client-connection` [E1+E2] - 连接代际重置时使目录源失效重读
  - 证据: `src/client/index.ts:42 import type {} from '@deepseek-ai/dsh-client-connection/client' + src/client/index.ts:100 ctx.on('connection/reset', listener)`
- `dsh-client-locale` [E1+E2] - 两套字典（schedule.catalog / schedule.manager）由 locale 服务注册并按命名空间绑定翻译
  - 证据: `src/client/definition.ts:8 import TranslateNS + src/client/index.ts:89-90 ctx.locale.register(NS, ...)`
- `dsh-client-ui-conversation` [E1+E2] - Turn 级卡片需向 conversation 的事件注册表登记 Definition，并复用其节点类型
  - 证据: `src/client/ScheduleTurnCard.tsx:2 import ToolResultNode + src/client/index.ts:188 ctx.uiConversation.events.register(scheduleTurnDefinition)`
- `dsh-client-ui-layout` [编译依赖] - 删除 Toast 注册进 layout 声明的 shell.overlay，任务管理面板 id 取自 layout 的 MainPanelId
  - 证据: `src/client/DeleteToast.tsx:13 import type {} from '@deepseek-ai/dsh-client-ui-layout/client' + src/client/index.ts:40 import MainPanelId`
- `dsh-client-ui-primitives` [编译依赖] - 任务卡片、目录反馈与锚定弹层复用共享原子控件
  - 证据: `src/client/CatalogFeedback.tsx:3 import Button/StateDot + src/client/ScheduleTaskTab.tsx:20 import IconClockOutlineRegular`
- `dsh-client-ui-renderer` [编译依赖] - 拉入 SlotRegistry 服务合并，使 ctx.slots.inject/register 在此编译单元可用
  - 证据: `src/client/index.ts:34 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-session` [编译依赖] - 拉入会话根标准 props 合并，供会话头部 seat 的注入签名
  - 证据: `src/client/index.ts:35 import type {} from '@deepseek-ai/dsh-client-ui-session/client'`
- `dsh-client-ui-sidebar` [编译依赖] - 面板图标注册进 ui-sidebar 声明的 sidebar.panellist 列表槽
  - 证据: `src/client/TaskManagerIcon.tsx:4 import type {} from '@deepseek-ai/dsh-client-ui-sidebar/client'`
- `dsh-client-ui-sidebar-right` [E1+E2] - 任务页类型与打开动作都走右侧栏的页类型注册表与 openTab 服务
  - 证据: `src/client/definition.ts:9 import SidebarRightTabDefinition + src/client/index.ts:155 ctx.sidebarRightTabs.register(...) + src/client/index.ts:198 ctx.sidebarRight.openTab(...)`
- `dsh-client-ui-tool` [编译依赖] - 创建卡复用 ui-tool 的 Tool 调用视图 props 类型，但不在 tool.call.toolview 注册条目
  - 证据: `src/client/ScheduleCreateCard.tsx:3 import ToolCallViewProps + src/client/schedule-create-card.ts:11 import ToolCallViewProps`
- `dsh-client-ui-workspace` [E1+E2] - 向 ui-workspace 声明的会话行 seat 注册标记与悬停卡，并用其 openSession 跳回原会话
  - 证据: `src/client/SessionScheduleHover.tsx:13 import type {} from '@deepseek-ai/dsh-client-ui-workspace/client' + src/client/index.ts:137 ctx.uiWorkspace.openSession(id)`
- `dsh-schedule` [E1+E2] - 任务记录、删除结果与更新请求的类型契约由 schedule 包持有
  - 证据: `src/client/catalog-source.ts:5 import ScheduleRecord/ScheduleId + src/client/index.ts:44 import ScheduleCatalogEntry/ScheduleUpdateRequest`
- `dsh-session` [编译依赖] - 会话标识与会话日志事件面类型由 session 包持有
  - 证据: `src/client/TaskDetail.tsx:17 import SessionId + src/client/schedule-turn.ts:12 import isAppendSurfaceEvent`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
