# dsh-client-ui-chat

- 包名: `@deepseek-ai/dsh-client-ui-chat`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-chat`

## 实现逻辑
Chat 目标插件：apply 先 registerConversationNodes 注册约 14 个 ConversationNodeDefinition 与 process 分组 (src/client/conversation-nodes/register.ts:22-38)，再由 registerChatNodeRenderers 把 'conversation.chat.node' 的 15 个 key（user/steering/context/turn-trigger/system-prompt/assistant-step/command/manual-compaction/compaction/model-retry/turn-error/turn-max-tokens/turn-process/turn-tail/unknown）注册为渲染器 (src/client/chat/register-node-renderers.ts:30-75)。apply 通过 ctx.uiSession.provide 暴露 chat hook 源 (src/client/apply.ts:111-114)，以 order 0 注册 'conversation.view#chat'（携 chatStore 与 conversation.chat.node/turnTail/assistant-actions 子槽）(src/client/apply.ts:177-258)，并在 shell.overlay 挂配额通知宿主、settings.general.item 挂 3 个偏好行、conversation.composer.dock 挂 StatsPills、conversation.approval.detail 挂 ApprovalCommand (src/client/apply.ts:263-286)。宿主半经 schemastery 暴露 transcriptView/performanceUsage/linkOpening 三个设置字段 (src/index.ts:18-39)。

## Provides
- conversation.view#chat (Chat 对话视图，order 0，label view.chat)
- conversation.chat.node 的 15 个 keyed 渲染器，及子槽 conversation.chat.turnTail / conversation.chat.assistant-actions / conversation.chat.commandview
- ctx.uiSession 标准 hooks.chat (框架 provide：Chat 快照源，EMPTY_CHAT_SNAPSHOT 兜底)
- slot: shell.overlay#chat.quota-notice (配额失败通知宿主，子槽 shell.quota-notice chain/root)
- slot: conversation.composer.dock#stats (StatsPills 用量统计)
- slot: conversation.approval.detail (ApprovalCommand：解析关联工具调用的命令)
- settings.general.item 三项：transcript-view / link-opening / performance-usage
- Locale 命名空间 chat (zh/en)
- 上抛 ChatNodeDataMap/ChatNodeStore/ChatSnapshot/ChatFileMentions 等公开类型与 createChatStore/EMPTY_CHAT_SNAPSHOT/isRunningTool/isSettledTool

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - agent 相关类型
  - 证据: `src/client/chat/ChatView.tsx:8 import @deepseek-ai/dsh-agent/types`
- `dsh-api-remotes` [编译依赖] - 引入 ctx.remote 与转发事件声明
  - 证据: `src/client/apply.ts:4 import @deepseek-ai/dsh-api-remotes/client`
- `dsh-api-session-controller` [E1+E2] - 按会话解析 binding 与事件源
  - 证据: `src/client/apply.ts:5 SessionBinding + src/client/apply.ts:190 ctx.sessions.binding(sessionId)`
- `dsh-client-locale` [E1+E2] - 注册 chat 字典并绑定 t
  - 证据: `src/client/apply.ts:16 merge + src/client/apply.ts:116 ctx.locale.register(NS)`
- `dsh-client-ui-approval` [编译依赖] - 消费 conversation.approval.detail 槽的 owner 契约
  - 证据: `src/client/chat/ApprovalCommand.tsx:3 import type @deepseek-ai/dsh-client-ui-approval/client`
- `dsh-client-ui-conversation` [E1+E2] - 消耗 conversation 视图与节点注册表，注册 Chat 视图
  - 证据: `src/client/apply.ts:6 ctx.uiConversation + src/client/apply.ts:177 ctx.slots.inject('conversation.view')`
- `dsh-client-ui-input-trigger` [编译依赖] - 技能引用经触发管线打开
  - 证据: `src/client/apply.ts:11 merge + src/client/apply.ts:225 ctx.get('inputTriggers')`
- `dsh-client-ui-layout` [编译依赖] - Chat 面板布局约束
  - 证据: `src/client/apply.ts:18 merge + src/client/contract/slots.ts:15`
- `dsh-client-ui-primitives` [编译依赖] - 聊天行/卡片的基础组件
  - 证据: `src/client/chat/AssistantMarkdown.tsx:4-5 + src/client/chat/ContextBody.tsx:8`
- `dsh-client-ui-renderer` [编译依赖] - 引入 slots 服务声明
  - 证据: `src/client/apply.ts:19 merge`
- `dsh-client-ui-session` [E1+E2] - 向会话 UI 提供 chat hooks 标准位
  - 证据: `src/client/apply.ts:20 merge + src/client/apply.ts:111 ctx.uiSession.provide`
- `dsh-client-ui-settings` [E1+E2] - 注册 Chat 三项 General 设置行
  - 证据: `src/client/apply.ts:21 merge + src/client/apply.ts:132 slots.inject('settings.general.item')`
- `dsh-client-ui-sidebar-browser` [编译依赖] - 浏览器 tab 类型声明
  - 证据: `src/client/apply.ts:10 merge`
- `dsh-client-ui-sidebar-documentpreview` [E1+E2] - 文件行号导航参数类型
  - 证据: `src/client/apply.ts:13 file 路由参数类型 + src/client/apply.ts:218 openResource`
- `dsh-client-ui-sidebar-right` [运行时依赖] - 文件与外链送入右侧栏
  - 证据: `src/client/apply.ts:9 + src/client/apply.ts:218-229 ctx.sidebarRight.openResource/openTab`
- `dsh-client-ui-workspace` [运行时依赖] - 分叉后打开新会话
  - 证据: `src/client/apply.ts:22 + src/client/apply.ts:249 ctx.uiWorkspace.openSession`
- `dsh-commands` [编译依赖] - 命令节点数据
  - 证据: `src/client/conversation-nodes/command.ts:7 import @deepseek-ai/dsh-commands/types`
- `dsh-llm` [编译依赖] - assistant 消息/品牌类型
  - 证据: `src/client/conversation-nodes/assistant.ts:6 + src/client/contract/slots.ts:2`
- `dsh-llm-retry` [编译依赖] - 模型重试节点与 turn 过程融合
  - 证据: `src/client/conversation-nodes/assistant.ts:7 + retry.ts:5`
- `dsh-session` [编译依赖] - 会话事件与标识类型
  - 证据: `src/client/apply.ts:8 SessionId + src/client/contract/slots.ts:3`
- `dsh-session-stats` [编译依赖] - 统计胶囊数据源
  - 证据: `src/client/chat/StatsPills.tsx:13 import @deepseek-ai/dsh-session-stats/client`
- `dsh-session-turn-outline` [编译依赖] - 轮次导航轨条目
  - 证据: `src/client/chat/turn-rail-items.ts:9 import @deepseek-ai/dsh-session-turn-outline/client`
- `dsh-settings` [E1+E2] - 宿主侧投影 Chat 偏好为设置表单字段
  - 证据: `src/index.ts:2 import @deepseek-ai/dsh-settings + src/index.ts:38 ctx.inject(['settings'])`
- `dsh-token-meter` [编译依赖] - token 计量显示
  - 证据: `src/client/chat/StatsPills.tsx:14 + src/client/conversation-nodes/turn-tail.ts:7`
- `dsh-tools` [编译依赖] - 工具调用节点与调用树
  - 证据: `src/client/conversation-nodes/tool.ts:7 + src/client/model/tool-call-tree.ts:2`

## Dependents (下游被依赖)
- `dsh-client-ui-attachment` - 依赖 Chat 视图声明的 conversation.message.images 槽
- `dsh-client-ui-deliverables` - 依赖 Chat 声明的 conversation.chat.turnTail 与 assistant-actions 槽
- `dsh-client-ui-goal` - 依赖 Chat 声明的 conversation.chat.node 槽
- `dsh-client-ui-message-feedback` - 引入 ui-chat 的类型面（对话内容与标准来源）
- `dsh-client-ui-plan` - Chat 节点类型与标准来源面
- `dsh-client-ui-settings-account` - 复用 chat 的类型面并写 ui-chat 设置（transcriptView/performanceUsage）
- `dsh-client-ui-subagent` - 引入 ChatConversationViewNode 等聊天节点类型
- `dsh-client-ui-tool` - 复用 AssistantChatData/ToolResultNode 等工具视图数据契约
- `dsh-client-ui-workflow-run` - 引入 keyed Chat 节点渲染契约
