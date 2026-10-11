# dsh-client-ui-sidebar-right

- 包名: `@deepseek-ai/dsh-client-ui-sidebar-right`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-sidebar-right`

## 实现逻辑
右侧边栏宿主插件：client/index.ts:110-111 在 apply 顶层构造 SidebarRightTabRegistry 与 SidebarSessionViews，:150-151 用 ctx.reflect.provide 提供 ctx.sidebarRightTabs 与 ctx.sidebarRight 两个服务（顶层构造是为了让其他插件的 register 不落在 effect 作用域内，见 :102-108 注释）。:204-233 把 RightbarRoot/RightbarSeat 注册进 rightbar 与 rightbar.session 槽，并声明 sidebar.right.pane.tab、.title、sidebar.right.tab.menu.item 子槽；:238-268 注册会话头部角落的 ExpandButton 与内置 guide 类型（走与其他类型相同的两段式路径）。布局联动经 ctx.layout.openRightbar/closeRightbar 同步（:189-192），标签域与导航由 service.ts 的 createSidebarRightController 与 tab-domain 实现。

## Provides
- ctx.sidebarRight (右侧边栏导航与呈现服务：openTab/openResource/closeHandler/commandTarget)
- ctx.sidebarRightTabs (标签类型注册表，两段式注册的第一段)
- 槽位 rightbar / rightbar.session / sidebar.right.pane.tab / sidebar.right.pane.tab.title / sidebar.right.tab.menu.item
- 快捷键组（切换/关闭/展开右侧边栏）

## Depends On (上游依赖)
- `dsh-api-session-controller` [E1+E2] - 保留已打开会话的视图，标签按会话作用域存活
  - 证据: `src/client/session-view.ts:2 import type { ISessions, SessionReference } from '@deepseek-ai/dsh-api-session-controller/client'; src/client/index.ts:111 new SidebarSessionViews(ctx.sessions)`
- `dsh-client-locale` [E1+E2] - 标签标签、guide 与菜单文案本地化
  - 证据: `src/client/labels.ts:10 import type {} from '@deepseek-ai/dsh-client-locale/client'; src/client/index.ts:162 ctx.locale.register(NS, { zh, en })`
- `dsh-client-resources` [E1+E2] - 资源型标签打开时对资源加引用钉住
  - 证据: `src/client/index.ts:27 import type {} from '@deepseek-ai/dsh-client-resources/client'; src/client/index.ts:125 ctx.resources.pin(address, signal)`
- `dsh-client-shortcuts` [E1+E2] - 注册侧栏切换/关闭等命令并读取按键目录
  - 证据: `src/client/shortcuts.ts:2 import type {} from '@deepseek-ai/dsh-client-shortcuts/client'; src/client/index.ts:163 registerSidebarShortcuts(ctx.shortcuts, ...)`
- `dsh-client-ui-conversation` [编译依赖] - 扩展按钮注册进 conversation.session.header.corner，需该槽已声明
  - 证据: `src/client/index.ts:32 import type {} from '@deepseek-ai/dsh-client-ui-conversation/client'; src/client/shell/ExpandButton.tsx:21 import ...`
- `dsh-client-ui-dockkit` [编译依赖] - 标签停靠、拆分面板与历史记录由 dockkit 纯规划函数计算
  - 证据: `src/client/service.ts:39-40 import { FloatRect, PaneId, TabId, TabRecord } + activeDockPaneId/canSplit/findTabPane`
- `dsh-client-ui-layout` [E1+E2] - 面板显隐与轨道宽度由 frame 的 layout 服务决定，本插件只上报事实
  - 证据: `src/client/index.ts:30 import type { ILayout } from '@deepseek-ai/dsh-client-ui-layout/client'; src/client/index.ts:189-192 layout.openRightbar/closeRightbar`
- `dsh-client-ui-primitives` [编译依赖] - 面板控件与图标复用共享原语
  - 证据: `src/client/shell/SidebarRight.tsx:33 import ... from '@deepseek-ai/dsh-client-ui-primitives'`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 服务由 renderer 提供
  - 证据: `src/client/index.ts:28 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-session` [E1+E2] - 跟踪当前屏上会话以切换侧栏呈现
  - 证据: `src/client/index.ts:29 import type {} from '@deepseek-ai/dsh-client-ui-session/client'; src/client/index.ts:113 ctx.uiSession.adapter.current`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/session-view.ts:3 import type { SessionId } from '@deepseek-ai/dsh-session/types'`

## Dependents (下游被依赖)
- `dsh-client-ui-chat` - 打开文件与浏览器资源
- `dsh-client-ui-deliverables` - 打开变更比较资源
- `dsh-client-ui-plan` - 打开计划预览资源
- `dsh-client-ui-reference` - 在右侧栏打开被引用的文件
- `dsh-client-ui-schedule` - 任务页类型与打开动作都走右侧栏的页类型注册表与 openTab 服务
- `dsh-client-ui-sidebar-browser` - 标签类型与键控槽由 sidebar-right 声明并提供 ctx.sidebarRight/ctx.sidebarRightTabs，browser 只能在其中注册
- `dsh-client-ui-sidebar-documentpreview` - 预览类型与键控槽均由 sidebar-right 声明
- `dsh-client-ui-sidebar-files` - 文件树类型与键控槽由 sidebar-right 声明
- `dsh-client-ui-sidebar-terminal` - 标签类型与键控槽、关闭处理器均挂在 sidebar-right 提供的服务上
- `dsh-client-ui-skill` - 引用预览在右侧边栏打开 skill 文件资源
- `dsh-client-ui-subagent` - 侧栏标签类型与资源打开能力由 sidebar-right 提供
- `dsh-experimental-session-inspector` - tab 的注册与右侧栏容器由该包提供
