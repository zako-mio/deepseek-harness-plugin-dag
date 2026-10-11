# dsh-client-ui-chat

- 包名: `@deepseek-ai/dsh-client-ui-chat`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-chat`

## 实现逻辑
Chat 视图插件：registerConversationNodes 注册各 ConversationNodeDefinition（assistant/tool/command/compaction/retry 等），registerChatNodeRenderers 把节点 key 映射到 React 渲染器（src/client/apply.ts:128、src/client/apply.ts:171）。它向 conversation.view 注册 chat 目标、向 conversation.chat.flow 声明会话级 keyed 子槽，并通过 ctx.uiSession.provide 把 chat 快照 hooks 投影给渲染器（src/client/apply.ts:129-132、src/client/apply.ts:210-221、src/client/apply.ts:223-301）。此外贡献配额提示宿主、composer dock 的 activity/usage 药丸与三条 settings.general.item 设置行（src/client/apply.ts:150-194、src/client/apply.ts:306-331）。Host 半只投影三个 volatile Chat 偏好并关闭自动设置文档（src/index.ts:28-38）。

## Provides
- conversation.view 'chat' 目标与 conversation.chat.flow / conversation.chat.node 槽位声明 (src/client/apply.ts:210-301)
- uiSession 的 chat hooks 投影 (src/client/apply.ts:129-132)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - Agent 类型
  - 证据: `src/client/chat/ChatView.tsx:8 import type + src/client/model/steering-history.ts:4 import`
- `dsh-api-remotes` [编译依赖] - Remote 调用与转发事件面
  - 证据: `src/client/apply.ts:5 import type`
- `dsh-api-session-controller` [E1+E2] - 会话绑定、事件流与分叉
  - 证据: `src/client/apply.ts:6 import type + src/client/apply.ts:217 ctx.sessions.binding(sessionId)`
- `dsh-client-locale` [E1+E2] - 注册 Chat 字典
  - 证据: `src/client/apply.ts:17 import type + src/client/apply.ts:134 ctx.locale.register(NS)`
- `dsh-client-product-analytics` [E1+E2] - 分支会话等交互埋点
  - 证据: `src/client/apply.ts:2 import type + src/client/apply.ts:290 ctx.get('productAnalytics')?.track`
- `dsh-client-ui-approval` [编译依赖] - 审批详情渲染
  - 证据: `src/client/chat/ApprovalCommand.tsx:3 import`
- `dsh-client-ui-conversation` [E1+E2] - 注册 chat 目标、节点与视图槽位
  - 证据: `src/client/apply.ts:7 import type + src/client/apply.ts:119 ctx.uiConversation.binding(binding)`
- `dsh-client-ui-input-trigger` [E1+E2] - 打开 skill 引用
  - 证据: `src/client/apply.ts:12 import type + src/client/apply.ts:264 ctx.get('inputTriggers')?.sessionOf(scope)`
- `dsh-client-ui-layout` [编译依赖] - 布局槽位类型
  - 证据: `src/client/apply.ts:19 import type + src/client/contract/slots.ts:18 import`
- `dsh-client-ui-primitives` [编译依赖] - 复用基础控件与 markdown 渲染
  - 证据: `src/client/chat/AssistantMarkdown.tsx:5 import + src/client/chat/StatsPills.tsx:9 import`
- `dsh-client-ui-renderer` [编译依赖] - 渲染器槽位服务类型
  - 证据: `src/client/apply.ts:20 import type`
- `dsh-client-ui-session` [E1+E2] - 把 chat hooks 投影为标准会话 seat
  - 证据: `src/client/apply.ts:21 import type + src/client/apply.ts:129 ctx.uiSession.provide`
- `dsh-client-ui-settings` [E1+E2] - 注册三条通用设置行
  - 证据: `src/client/apply.ts:22 import type + src/client/apply.ts:150 scope.slots.inject('settings.general.item')`
- `dsh-client-ui-sidebar-browser` [编译依赖] - 浏览器标签类型
  - 证据: `src/client/apply.ts:11 import type`
- `dsh-client-ui-sidebar-documentpreview` [编译依赖] - 文件预览参数类型
  - 证据: `src/client/apply.ts:14 import type`
- `dsh-client-ui-sidebar-right` [E1+E2] - 打开文件与浏览器资源
  - 证据: `src/client/apply.ts:10 import type + src/client/apply.ts:257 ctx.sidebarRight.openResource(url)`
- `dsh-client-ui-workspace` [编译依赖] - 打开会话所属工作区
  - 证据: `src/client/apply.ts:23 import type`
- `dsh-commands` [编译依赖] - 命令节点类型
  - 证据: `src/client/conversation-nodes/command.ts:7 import`
- `dsh-llm` [编译依赖] - LLM 品牌与消息类型
  - 证据: `src/client/contract/slots.ts:3 import + src/client/conversation-nodes/assistant.ts:6 import`
- `dsh-llm-retry` [编译依赖] - 重试节点与轮次尾部类型
  - 证据: `src/client/conversation-nodes/assistant.ts:7 import + src/client/conversation-nodes/retry.ts:5 import`
- `dsh-session` [编译依赖] - 会话事件与快照类型
  - 证据: `src/client/apply.ts:9 import type + src/client/conversation-nodes/tool.ts:6 import`
- `dsh-session-stats` [编译依赖] - 读取会话统计投影
  - 证据: `src/client/chat/StatsPills.tsx:13 import`
- `dsh-session-turn-outline` [编译依赖] - 轮次导航大纲
  - 证据: `src/client/chat/turn-rail-items.ts:9 import`
- `dsh-settings` [E1+E2] - 关闭该服务的自动设置文档
  - 证据: `src/index.ts:2 import type + src/index.ts:38 ctx.inject(['settings'])`
- `dsh-token-meter` [编译依赖] - token 计量展示
  - 证据: `src/client/chat/StatsPills.tsx:14 import + src/client/conversation-nodes/turn-tail.ts:7 import`
- `dsh-tools` [编译依赖] - 工具调用与结果类型
  - 证据: `src/client/conversation-nodes/tool.ts:7 import + src/client/model/tool-call-tree.ts:2 import`

## Dependents (下游被依赖)
- `dsh-client-ui-attachment` - 依赖 Chat 视图声明的 conversation.message.images 槽
- `dsh-client-ui-deliverables` - 复用 chat 的 turn-tail 槽位与 ChatFileMentions 契约
- `dsh-client-ui-goal` - 占用 chat 节点槽位声明
- `dsh-client-ui-message-feedback` - 引入 ui-chat 的类型面（对话内容与标准来源）
- `dsh-client-ui-plan` - 读取 chat 目标的 turn 数据源
- `dsh-client-ui-settings-account` - 配额通知注册进 chat 声明的 shell.quota-notice 并复用其 owner props 类型；引导写入 chat 的 transcriptView 偏好
- `dsh-client-ui-subagent` - 复用 chat 侧的会话节点/视图类型
- `dsh-client-ui-tool` - 工具视图消费 chat 侧的工具调用阶段/结果节点类型
- `dsh-client-ui-user-questions` - 回复视图复用 chat 侧会话节点类型
- `dsh-client-ui-workflow-run` - 节点定义返回 chat 侧会话视图节点类型
- `dsh-experimental-client-ui-cot-translation` - 译文挂在推理正文槽位，需要 chat 侧的槽位与类型声明
- `dsh-experimental-session-inspector` - 聊天节点模型与揭示目标解析建立在 chat 侧类型面之上
