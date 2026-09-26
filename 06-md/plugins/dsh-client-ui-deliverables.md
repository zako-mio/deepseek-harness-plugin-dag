# dsh-client-ui-deliverables

- 包名: `@deepseek-ai/dsh-client-ui-deliverables`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 17
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-deliverables`

## 实现逻辑
浏览器半把交付物三面装进既有洞：在 'conversation.chat.turnTail' 注册 DeliverablesTail（变更文件卡与交付卡，子槽 deliverables.file.actions）(src/client/index.ts:61-81)，在 'tool.call.toolview' 以 key 'present' 注册 PresentRow (src/client/index.ts:82-84)，再在 sidebarRight 注册 changes-review tab 类型、在 'sidebar.right.pane.tab' 注册 ReviewTab（子槽 deliverables.review.file.actions）(src/client/index.ts:86-100)。最后 ctx.provide('chatFileMentions') 提供终版回复中对产出/交付文件的 inline-code 提及链接 (src/client/index.ts:101-112)。宿主半在 system-prompt 注册 Web 文件引用指引节，并由 present-open 提供已声明文件的鉴权 native open (src/index.ts:29-36)。

## Provides
- slot: conversation.chat.turnTail#dsh-client-ui-deliverables (变更文件卡与交付卡；子槽 deliverables.file.actions list/session)
- slot: tool.call.toolview#present (present 工具行 PresentRow)
- sidebarRightTabs 类型 changes-review + slot: sidebar.right.pane.tab#changes-review (ReviewTab；子槽 deliverables.review.file.actions list/session)
- 服务 chatFileMentions (ctx.provide：终版 prose 的文件提及链接，Chat 视图经 ctx.get 消费，缺省即关断)
- Locale 命名空间 deliverables
- 上抛 changesReviewAddress/parseChangesReviewAddress/CHANGES_REVIEW_ADDRESS 与 ChangesSummary/ChangesDiff 类型
- 宿主侧 system-prompt 节 ui:deliverable-file-references (FILE_REFERENCE_PROMPT)

## Depends On (上游依赖)
- `dsh-api-remotes` [编译依赖] - 引入 ctx.remote 与事件声明
  - 证据: `src/client/index.ts:13 import @deepseek-ai/dsh-api-remotes/client`
- `dsh-api-session-controller` [运行时依赖] - 解析会话与其工作目录以做原生打开
  - 证据: `src/present-open.ts:23 ctx.sessionController`
- `dsh-api-workspace-files` [运行时依赖] - 读取工作区文件内容
  - 证据: `src/present-open.ts:119 ctx.workspaceFiles`
- `dsh-client-connection` [E1+E2] - 原生打开请求经连接层发送
  - 证据: `src/client/index.ts:14 + src/present-open.ts:21 ctx.connection`
- `dsh-client-locale` [E1+E2] - 注册 deliverables 字典
  - 证据: `src/client/index.ts:16 + src/client/index.ts:60 ctx.locale.register(NS)`
- `dsh-client-ui-chat` [E1+E2] - 依赖 Chat 声明的 conversation.chat.turnTail 与 assistant-actions 槽
  - 证据: `src/client/Deliverables.tsx:3 ChatFileMentions 类型 + src/client/index.ts:15 import ChatFileMentions`
- `dsh-client-ui-conversation` [运行时依赖] - 注册交付物 ConversationNode 定义
  - 证据: `src/client/index.ts:17 + src/client/index.ts:59 ctx.uiConversation.events.register`
- `dsh-client-ui-dockkit` [编译依赖] - review tab 的 TabId 类型
  - 证据: `src/client/review-store.ts:8 import type TabId from @deepseek-ai/dsh-client-ui-dockkit`
- `dsh-client-ui-primitives` [编译依赖] - 卡片与 diff 视图基础组件
  - 证据: `src/client/Deliverables.tsx:4 + src/client/FileDiff.tsx:4-5`
- `dsh-client-ui-renderer` [编译依赖] - 引入 slots 服务声明
  - 证据: `src/client/index.ts:18 merge`
- `dsh-client-ui-settings` [运行时依赖] - 开发者工具开关控制 diff 展示
  - 证据: `src/client/index.ts:20 + src/client/index.ts:70 ctx.configForms.developerTools`
- `dsh-client-ui-sidebar-right` [运行时依赖] - 打开 changes-review 资源 tab
  - 证据: `src/client/index.ts:19 + src/client/index.ts:77 ctx.sidebarRight.openResource`
- `dsh-client-ui-tool` [运行时依赖] - present 工具行视图
  - 证据: `src/client/PresentRow.tsx:4 + src/client/index.ts:82 ctx.slots.inject('tool.call.toolview')`
- `dsh-llm` [编译依赖] - presented 结果的消息类型
  - 证据: `src/presented.ts:4 import @deepseek-ai/dsh-llm`
- `dsh-sandbox-policy` [运行时依赖] - native open 前校验沙箱策略
  - 证据: `src/present-open.ts:121 ctx.sandboxPolicy`
- `dsh-session` [编译依赖] - 会话标识与事件类型
  - 证据: `src/changes.ts:2 import SessionId + src/client/turn-deliverables.ts:7`
- `dsh-system-prompt` [E1+E2] - 注册 Web 文件引用指引节
  - 证据: `src/index.ts:9 import @deepseek-ai/dsh-system-prompt + src/index.ts:31 ctx.systemPrompt.section`
- `dsh-tool-present` [编译依赖] - present 工具结果数据
  - 证据: `src/client/turn-deliverables.ts:11 + src/presented.ts:2`
- `dsh-workspace-changes` [编译依赖] - 工作区变更记录/差异类型
  - 证据: `src/changes.ts:3 import @deepseek-ai/dsh-workspace-changes/types + src/index.ts:10`

## Dependents (下游被依赖)
- `dsh-client-ui-open-in-app` - 使用 deliverables 声明的文件动作槽
