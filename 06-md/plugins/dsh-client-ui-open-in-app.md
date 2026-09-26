# dsh-client-ui-open-in-app

- 包名: `@deepseek-ai/dsh-client-ui-open-in-app`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 18
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-open-in-app`

## 实现逻辑
apply 构造 OpenInAppController（加载 Host 应用列表/持久化选择）与 OpenInAppPathController（经 Session Remote 判定桌面可用性、查关联应用、执行 open/reveal），并把二者分发到五处槽（src/client/index.ts:123-125）。会话头部 utilities 槽注册「Open In...」分体按钮，注入应用列表/选择/启动进度 hooks 与图标 URL（src/client/index.ts:80-99）；侧栏文档预览的两个槽与 deliverables 两个槽注册路径动作，失败经 Toast 播报（src/client/open-failure-toast.tsx:4）。另注册 workspace.openLocal 快捷键，busy/无目标时给出阻塞原因（src/client/index.ts:59-77）。

## Provides
- conversation.session.header.utilities 条目 'open-in-app'（会话头部「在应用中打开」分体按钮）
- sidebar.right.tab.document.actions / sidebar.right.tab.document.unpreviewable 条目（文档预览的打开/定位路径动作）
- deliverables.file.actions / deliverables.review.file.actions 条目（交付与变更文件卡的路径动作）
- ctx.shortcuts 命令 workspace.openLocal（在本地应用中打开当前工作区）

## Depends On (上游依赖)
- `dsh-api-gateway` [编译依赖] - 引入 gateway 客户端的 ctx.remote 声明合并
  - 证据: `src/client/index.ts:14 import type {}`
- `dsh-api-remotes` [E1+E2] - ctx.remote 与 Remote 结果类型
  - 证据: `src/client/index.ts:15 import type + src/client/open-path.ts:6 import`
- `dsh-api-session-controller` [E1+E2] - 调用 session Remote 打开工作区路径/查询关联应用
  - 证据: `src/client/index.ts:16 import remote + src/client/open-path.ts:7 import types`
- `dsh-client-locale` [运行时依赖] - 注册 open-in-app 文案
  - 证据: `src/client/index.ts:9 import + src/client/index.ts:50 ctx.locale.register(NS)`
- `dsh-client-shortcuts` [运行时依赖] - 注册 workspace.openLocal 快捷键命令
  - 证据: `src/client/index.ts:7 import + src/client/index.ts:59 ctx.shortcuts.register`
- `dsh-client-ui-conversation` [运行时依赖] - 使用 ui-conversation 声明的会话头部槽
  - 证据: `src/client/OpenInAppAction.tsx:3 import + src/client/index.ts:80 slots.inject('conversation.session.header.utilities')`
- `dsh-client-ui-deliverables` [运行时依赖] - 使用 deliverables 声明的文件动作槽
  - 证据: `src/client/FileRouteAction.tsx:3 import type + src/client/index.ts:116/index.ts:119 slots.inject`
- `dsh-client-ui-layout` [E1+E2] - 读主面板选择以判断当前无全局面板时才有打开目标
  - 证据: `src/client/index.ts:11 import type + src/client/index.ts:53 ctx.layout.panelInfo`
- `dsh-client-ui-primitives` [编译依赖] - 复用 Toast/图标/按钮控件
  - 证据: `src/client/open-failure-toast.tsx:4 import + src/client/OpenTargetButton.tsx:6`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 槽注册表
  - 证据: `src/client/index.ts:10 import type + src/client/index.ts:39 inject 'slots'`
- `dsh-client-ui-session` [编译依赖] - Session 标准来源类型面
  - 证据: `src/client/index.ts:12 import type {}`
- `dsh-client-ui-sidebar-documentpreview` [运行时依赖] - 使用文档预览声明的路径动作槽
  - 证据: `src/client/index.ts:13 import type + src/client/index.ts:104 slots.inject('sidebar.right.tab.document.actions')`
- `dsh-host-open-in-app` [编译依赖] - 复用 Host 侧共用的图标路由前缀常量
  - 证据: `src/client/index.ts:17 import { OPEN_IN_APP_ICON_PREFIX_ROUTE }`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
