# dsh-client-ui-deliverables

- 包名: `@deepseek-ai/dsh-client-ui-deliverables`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-deliverables`

## 实现逻辑
浏览器半注册变更文件/交付卡片到 conversation.chat.turnTail、present 工具的 tool.call.toolview 视图、以及 sidebar.right 的 changes-review 比较标签类型，并提供 ctx.chatFileMentions 把收尾散文里的行内代码提及链接到产物文件（src/client/index.ts:61-113）。connection/reset 时清空 summary/diff/presented 三个 store（src/client/index.ts:54-58）。Host 半注册 present 原生打开路由，并向系统提示注册交付文件引用段（src/index.ts:29-35）。

## Provides
- ctx.chatFileMentions (把收尾散文中的文件提及解析为可打开链接) (src/client/index.ts:113)
- conversation.chat.turnTail / tool.call.toolview / sidebar.right.pane.tab 槽位贡献 (src/client/index.ts:61-100)

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - Remote 会话与文件访问调用
  - 证据: `src/client/index.ts:13 import type + src/client/present-open.ts:3 import`
- `dsh-api-session-controller` [编译依赖] - 会话控制器类型
  - 证据: `src/present-open.ts:3 import`
- `dsh-api-workspace-files` [E1+E2] - 访问工作区文件
  - 证据: `src/present-open.ts:4 import + src/present-open.ts:181 ctx.workspaceFiles`
- `dsh-client-connection` [E1+E2] - 读取连接世代并对原生打开做认证
  - 证据: `src/client/index.ts:14 import type + src/present-open.ts:21 ctx.connection`
- `dsh-client-locale` [E1+E2] - 注册 deliverables 字典
  - 证据: `src/client/index.ts:16 import + src/client/index.ts:60 ctx.locale.register(NS)`
- `dsh-client-ui-chat` [编译依赖] - 复用 chat 的 turn-tail 槽位与 ChatFileMentions 契约
  - 证据: `src/client/Deliverables.tsx:3 import + src/client/index.ts:15 import type`
- `dsh-client-ui-conversation` [E1+E2] - 注册 deliverables 事件定义
  - 证据: `src/client/index.ts:17 import type + src/client/index.ts:59 ctx.uiConversation.events.register`
- `dsh-client-ui-dockkit` [编译依赖] - 复用停靠布局控件渲染比较视图
  - 证据: `src/client/review-store.ts:8 import`
- `dsh-client-ui-primitives` [编译依赖] - 复用基础控件渲染文件行
  - 证据: `src/client/ChangedFiles.tsx:4 import + src/client/FileDiff.tsx:4 import`
- `dsh-client-ui-renderer` [编译依赖] - 渲染器槽位服务类型
  - 证据: `src/client/index.ts:18 import type`
- `dsh-client-ui-settings` [编译依赖] - 设置槽位类型
  - 证据: `src/client/index.ts:20 import type`
- `dsh-client-ui-sidebar-right` [E1+E2] - 打开变更比较资源
  - 证据: `src/client/index.ts:19 import type + src/client/index.ts:77 ctx.sidebarRight.openResource`
- `dsh-client-ui-tool` [编译依赖] - 工具视图基础类型
  - 证据: `src/client/PresentRow.tsx:4 import`
- `dsh-llm` [编译依赖] - 助手消息标识类型
  - 证据: `src/presented.ts:4 import`
- `dsh-sandbox-policy` [E1+E2] - 按沙箱策略校验可打开路径
  - 证据: `src/present-open.ts:6 import + src/present-open.ts:121 ctx.sandboxPolicy`
- `dsh-session` [编译依赖] - 会话标识与事件类型
  - 证据: `src/changes.ts:2 import + src/present-open.ts:10 import`
- `dsh-system-prompt` [E1+E2] - 注册交付文件引用提示段
  - 证据: `src/index.ts:9 import type + src/index.ts:31 ctx.systemPrompt.section`
- `dsh-tool-present` [编译依赖] - present 工具结果类型
  - 证据: `src/client/turn-deliverables.ts:13 import + src/presented.ts:2 import`
- `dsh-workspace-changes` [E1+E2] - 读取工作区变更与差异
  - 证据: `src/changes.ts:3 import + src/present-open.ts:158 ctx.workspaceChanges`

## Dependents (下游被依赖)
- `dsh-client-ui-open-in-app` - 接入交付文件动作槽位
