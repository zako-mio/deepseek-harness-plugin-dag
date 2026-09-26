# dsh-client-ui-sidebar-right

- 包名: `@deepseek-ai/dsh-client-ui-sidebar-right`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-sidebar-right`

## 实现逻辑
浏览器半在 apply 顶层构造 SidebarRightTabRegistry，并分别经 `ctx.reflect.provide('sidebarRightTabs')` 与 `ctx.reflect.provide('sidebarRight')` 暴露 tab 类型注册表与导航面（src/client/index.ts:109、122-123），使其它包可注册而本包 effect 不作为其宿主。它声明 `rightbar` 槽（含 rightbar.session 及 keyed `sidebar.right.pane.tab`/`title` 与 list `sidebar.right.tab.menu.item` 子槽，src/client/index.ts:177-205），并在会话代际间对同一 store 做 adopt/forget（src/client/index.ts:140-159）。同一 store 还供 `conversation.session.header.corner` 展开按钮使用（src/client/index.ts:210-215），内建 `guide` tab 类型经同一公共两级路径注册（src/client/index.ts:176、224-240）。node half 为空 apply（src/index.ts:4）。

## Provides
- sidebarRight locale 命名空间字典
- ctx.sidebarRightTabs（右侧边栏 tab 类型注册表，任何包第二阶段注册的入口）
- ctx.sidebarRight（右侧边栏导航/展示面：openTab/openTabFromTarget/bind/splitPane/toggleFullscreen/commandTarget 等）
- rightbar 槽位占用者，声明 rightbar.session 及 sidebar.right.pane.tab（keyed）/ sidebar.right.pane.tab.title（keyed）/ sidebar.right.tab.menu.item（list）子槽
- conversation.session.header.corner 槽的展开按钮
- sidebarRightTabs 注册内建 'guide' tab 类型（含 sidebar.right.tab.guide.entry / sidebar.right.tab.guide 子槽）

## Depends On (上游依赖)
- `dsh-api-session-controller` [编译依赖] - 会话视图类型（SidebarSessionViews 消费 SessionManager）
  - 证据: `src/client/session-view.ts:2 import (client)`
- `dsh-client-locale` [E1+E2] - 注册并绑定本包文案
  - 证据: `src/client/contract/slots.ts:28 import + src/client/index.ts:134 ctx.locale.register`
- `dsh-client-resources` [E1+E2] - 把 tab 资源登记/固定到资源模型
  - 证据: `src/client/index.ts:27 import (client) + src/client/index.ts:120 ctx.resources.pin`
- `dsh-client-shortcuts` [E1+E2] - 注册右栏快捷键并读取快捷键目录
  - 证据: `src/client/contract/slots.ts:23 import (client) + src/client/index.ts:135 registerSidebarShortcuts(ctx.shortcuts, ...)`
- `dsh-client-ui-conversation` [编译依赖] - 注册会话头部角槽需要其槽声明合并
  - 证据: `src/client/index.ts:32 import (client)`
- `dsh-client-ui-dockkit` [编译依赖] - dock 布局/标签 id 与纯规划器
  - 证据: `src/client/contract/slots.ts:29 import (client) + src/client/index.ts:47 import type TabId`
- `dsh-client-ui-layout` [E1+E2] - 经布局服务开合/全屏右栏面板
  - 证据: `src/client/contract/slots.ts:25 import (client) + src/client/index.ts:160 const layout: ILayout = ctx.layout`
- `dsh-client-ui-primitives` [编译依赖] - 复用共享 UI 原语
  - 证据: `src/client/shell/ExpandButton.tsx:19 import`
- `dsh-client-ui-renderer` [编译依赖] - 引入 ctx.slots 合并
  - 证据: `src/client/index.ts:28 type-only import`
- `dsh-client-ui-session` [编译依赖] - 引入会话标准 props 合并
  - 证据: `src/client/index.ts:29 type-only import`
- `dsh-session` [编译依赖] - SessionId 等类型
  - 证据: `src/client/focus.ts:3 import (/types)`

## Dependents (下游被依赖)
- `dsh-client-ui-chat` - 文件与外链送入右侧栏
- `dsh-client-ui-deliverables` - 打开 changes-review 资源 tab
- `dsh-client-ui-plan` - 打开计划资源与注册预览页型
- `dsh-client-ui-reference` - 在右侧栏打开被引用的文件
- `dsh-client-ui-schedule` - 注册任务详情页型并打开详情 tab
- `dsh-client-ui-sidebar-browser` - 把 tab 类型与 body/title 注册进右侧边栏的两级公共路径
- `dsh-client-ui-sidebar-documentpreview` - 经两级公共路径把预览类型、body 与标题注册进右侧边栏
- `dsh-client-ui-sidebar-files` - 把 tab 类型、body 与标题注册进右侧边栏
- `dsh-client-ui-sidebar-terminal` - 注册终端标签类型、读取 occurrence 参数并注册关闭处理器
- `dsh-client-ui-skill` - 点击 skill 引用时在侧栏打开其文件资源
- `dsh-client-ui-subagent` - 打开子代理侧栏资源并注册 subagentchat 标签类型
