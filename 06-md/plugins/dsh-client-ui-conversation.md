# dsh-client-ui-conversation

- 包名: `@deepseek-ai/dsh-client-ui-conversation`
- 分组: G27 会话交互UI
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-conversation`

## 为什么需要它（设计初衷）
Web 对话域核心 UI：会话骨架（skeleton）、有序聊天流、Host 支持的 busy-Enter 偏好作曲家与详情宿主。它把 SessionEvent 日志投影为可交互的 Chat 节点（助手/工具/重试/压缩/队列/规划条），解决'用户如何在浏览器中阅读并驱动一次 Agent 会话'的展示层问题，并作为 conversation.chat.node / details.tool 等 slot 的宿主与分发者。

发展史：dsh 客户端三大件之一，属于 conversation 域 base 层。经历了 thinking-tail 滚动、重试节点稳定状态行、用户气泡去分支操作、Host-backed 偏好持久化等多个迭代决策（2026-07~08 Agent Notes），slot 化渲染体系随 web bundle 一起成型。版本 0.1.0-rc.5。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-conversation/README.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-conversation/package.json

## 实现逻辑
会话交互核心大包（70 ts）。apply() 先 registerConversationNodes+registerChatNodeRenderers，然后向 slots 注册：conversation（ConversationRoot，声明 session/header/composer/input.dock/hero 等 11 个 child slot）、conversation.session（ConversationSession，持 chatStore + views ring）、conversation.session.header、conversation.composer.bar（InputBar，注入 shell/inputTriggers/command/stop/submissionPolicy）、conversation.composer 的 ApprovalPanel（selector 路由）、conversation.view id=chat（ChatView + keyed conversation.chat.node 座位）、details（DetailsPanel）、settings.general.item 的 EnterBehaviorRow。以 ConversationController 提供 ctx.conversation（scope 寻址 send/cancel/updateQueue/loadOlder，input hub + composer blocks 注册表），并注册 11 个 Chat 业务 Definition（assistant/tool/command/compaction/retry/turn-error/turn-max-tokens/turn-tail/inbox/message）到 ConversationEventRegistry。composer 标准输入 kit（hooks:input + inputActions）经 sessions.provide 发布。依赖 host 的 slots/layout/sessions/workspaces/locale/connection/remote/settingsScope/conversationEvents/conversationViews。

## Provides
- ctx.conversation（ConversationController: send/cancel/updateQueue/loadOlder/input/blocks）
- slot 声明: conversation, conversation.session, conversation.session.header, conversation.composer, conversation.composer.bar, conversation.view, conversation.details, conversation.chat.node(keyed), conversation.chat.turnTail(chain), conversation.chat.assistant-actions(list), conversation.input.dock, conversation.input.left/right/overlay, conversation.hero.workspace/hero.agentPreset, conversation.session.header.actions/utilities, conversation.input.plan/model
- chatStore(per-session, persist 'dsh.conversation.chat')
- composer 标准输入 provide 通道(input/inputActions)
- CONVERSATION_SETTINGS_NAMESPACE settings 注册
- locale 命名空间 'conversation'
- ChatNodeDataMap: tool-call/assistant-step/command/manual-compaction/compaction/model-retry/turn-error/turn-max-tokens/turn-tail/command-input

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - inbox/agent 事件类型契约（agent/inbox/spliced）
  - 证据: `conversation-nodes/inbox.ts:5 InboxTarget + package.json peerDependencies:57`
- `dsh-api-remotes` [运行时依赖] - ctx.remote 远程调用底座（conversation 事件经 connection 传输）
  - 证据: `apply.ts:52 inject 'remote'`
- `dsh-client-connection` [运行时依赖] - wire 连接句柄/事件总线（connection/reset 等）
  - 证据: `apply.ts:52 inject 'connection' + src/index.ts package.json dsh.client.inject:35`
- `dsh-client-locale` [编译依赖] - 命名空间字典注册与 t 座位
  - 证据: `apply.ts:12 type-only + apply.ts:124 ctx.locale.register(NS)`
- `dsh-client-runtime` [编译依赖] - SessionRuntime 会话/工作区服务、EventDefinition+View 注册表、useProjection/defineStore 运行时
  - 证据: `package.json:34-41(dsh.client.inject runtime/api-remotes/connection) + apply.ts:5-6 resolveWorkspacePath,ISessions + apply.ts:52-53 inject sessions/workspaces/conversationEvents/conversationViews`
- `dsh-client-ui-attachment` [编译依赖] - 图片 draft rail/lightbox/overlay 渲染 atoms
  - 证据: `InputBar.tsx:15-16 AttachmentRail,DropOverlay,ImageLightbox + AssistantMarkdown.tsx:17 ImageGallery`
- `dsh-client-ui-input-trigger` [编译依赖] - '/'|'@' 输入触发控制器与 slash 事件契约（bail 监听）
  - 证据: `input/hub.ts:12 InputTriggerController + input/machine.ts:16 + input/contract.ts:13 + input/facade.ts:14`
- `dsh-client-ui-layout` [编译依赖] - 三栏框架提供 conversation/details 父 slot + ctx.layout 面板动作
  - 证据: `apply.ts:10 type-only import + apply.ts:118 layout + apply.ts:392/452 layout.openDetails/closeDetails`
- `dsh-client-ui-primitives` [编译依赖] - 通用 UI atoms/图标/Markdown 渲染底座
  - 证据: `多文件 import（InputBar.tsx:12-14, MessageItem.tsx:11, ChatView.tsx:17 等）`
- `dsh-client-ui-settings` [运行时依赖] - settingsScope 服务承载 busy-Enter 设置绑定
  - 证据: `apply.ts:9 type-only + apply.ts:133-135 ctx.settingsScope.bind(ConversationSettings)`
- `dsh-client-ui-slots` [编译依赖] - SlotRegistry 注册/dispatch 与四份 props 类型底座
  - 证据: `apply.ts:3 resolveSlotLabel,BoundActions + contract/slots.ts:5-7`
- `dsh-commands` [编译依赖] - command/run 事件与命令 surface 契约
  - 证据: `conversation-nodes/command.ts:9 dsh-commands/types`
- `dsh-goal` [编译依赖] - goal 投影 key 类型合并（hasGoal 开关）
  - 证据: `InputBar.tsx:21 dsh-goal/client（goal projection key 合并）`
- `dsh-llm-retry` [编译依赖] - model-retry 节点事件类型
  - 证据: `conversation-nodes/assistant.ts:9 dsh-llm-retry/types + package.json:72`
- `dsh-permission-presets` [编译依赖] - permissions 投影与 PermissionSelect 值类型
  - 证据: `skeleton/PermissionSelect.tsx:4 dsh-permission-presets/client`
- `dsh-session-projection` [运行时依赖] - 会话投影数据源：plan/goal/permissions/tokenUsage/sessionStats 渲染输入
  - 证据: `InputBar.tsx:64/66/90/123 useProjection('plan'|'goal'|'imageLimits'|'permissions') + StatsLine.tsx:165-170 useProjection('tokenUsage'|'sessionStats') + ContextMeter.tsx:41-42`
- `dsh-session-stats` [编译依赖] - sessionStats 投影 key 类型合并
  - 证据: `StatsLine.tsx:10 dsh-session-stats/client（sessionStats projection key 合并）+ package.json:73`
- `dsh-token-meter` [编译依赖] - tokenUsage/contextPressure/contextBreakdown 投影类型
  - 证据: `StatsLine.tsx:11 + ContextMeter.tsx:10 dsh-token-meter/client + package.json:74`
- `dsh-tool-todo` [编译依赖] - todos 投影类型（todo dock 数据）
  - 证据: `skeleton/TodoPanel.tsx:15 dsh-tool-todo/client`
- `dsh-tools` [编译依赖] - Tool 调用 wire 类型契约（tool/call、tool/result）
  - 证据: `conversation-nodes/tool.ts:7 dsh-tools/types + package.json:75`

## Dependents (下游被依赖)
- `dsh-client-ui-agent-preset` - 新会话 chip、header label 槽与 session flow
- `dsh-client-ui-commands` - overlay 槽声明 typecheck
- `dsh-client-ui-deliverables` - 消费 turnTail 链座位与 TurnTailOwnerProps 载体（turn.data 读 deliverables）
- `dsh-client-ui-goal` - 消费 input.dock 座位与 conversationEvents 注册表
- `dsh-client-ui-jobs` - 消费 header actions 座位声明
- `dsh-client-ui-message-feedback` - 消费 assistant-actions 座位声明
- `dsh-client-ui-model-selection` - composer model 槽声明
- `dsh-client-ui-plan` - composer plan 槽声明
- `dsh-client-ui-subagent` - 会话头与 composer 槽声明
- `dsh-client-ui-tool` - 消费 conversation.chat.node/details.tool 座位声明与 ChatNodeDataMap 'tool-call' 数据契约
- `dsh-client-ui-trajectory` - 消费 conversation.view 视图环座位与 ConvViewProps
- `dsh-client-ui-user-questions` - 消费 composer 链座位与 ComposerChainProps（interactions 载体）
- `dsh-client-ui-workflow-run` - 消费 conversation.chat.node 座位与 ChatNodeDataMap 合并面
- `dsh-client-ui-workspace` - 消费 conversation.hero.workspace 座位
