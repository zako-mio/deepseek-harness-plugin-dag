# dsh-client-ui-conversation

- 包名: `@deepseek-ai/dsh-client-ui-conversation`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 13
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-conversation`

## 实现逻辑
目标中立会话装配与输入核心：apply 建 UiConversation 与 InputHub，用 ctx.uiSession.provide 为每会话解析出 conversation/input hooks 与 inputActions (src/client/apply.ts:283-299)。骨架经 slots.registerFactory('conversation.content') 与 register('conversation.session'/'conversation.header'/'conversation.session.header'/'conversation.composer.bar') 声明整棵会话树及子槽 (src/client/apply.ts:308-529)。输入侧实现 Enter/Shift+Enter 等固定快捷键与停转快捷键 (src/client/apply.ts:236-265)，并实现文件选择/拖入的 addFiles 与 draft 上传（含 Desktop 桥 __DSH_HOST_PATHS__）(src/client/apply.ts:100-108, 459-497)。最后 ctx.plugin(ConversationController) 与 todoDockEntry/queueDockEntry (src/client/apply.ts:545-551)；宿主半暴露 busyEnter 设置字段 (src/index.ts:17-32)。

## Provides
- ctx.conversation (IConversation：按 session scope 寻址的会话动作与输入注册表)
- ctx.uiConversation (UiConversation：目标中立的会话注册表与每会话装配)
- 槽位骨架：main#conversation、conversation.content(factory)、conversation.session、conversation.header、conversation.session.header、conversation.composer.bar
- 子槽声明：conversation.view(list)、conversation.composer(chain)、conversation.input.attachments/overlay/permission/left/plan/right/model/activity、conversation.input.dock(list)、conversation.composer.dock(list)、conversation.hero.*
- ctx.uiSession 标准 hooks conversation/input 与 props inputActions
- settings.general.item#composer-enter (Enter 行为偏好)
- Locale 命名空间 conversation
- 上抛 ConversationNodeDefinition/ConversationViewDefinition/ConversationStore/UiConversation/ConversationController 等公开类型与 createConversationStore/inspectRequestPrompt

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - agent/initiator 类型
  - 证据: `src/client/contract/input.ts:10 + src/client/input/hub.ts:16`
- `dsh-api-session-controller` [E1+E2] - 按会话解析 scope 与 conversation 服务
  - 证据: `src/client/apply.ts:4 + src/client/apply.ts:130-137 scopedConversation(sessions, id)`
- `dsh-api-workspace-controller` [编译依赖] - 工作区状态以渲染工作区标题
  - 证据: `src/client/contract/slots.ts:6 + src/client/skeleton/ConversationContent.tsx:4`
- `dsh-client-file-upload` [运行时依赖] - 浏览器 Worker 文件上传服务
  - 证据: `src/client/contract/slots.ts:5 + src/client/service.ts:19`
- `dsh-client-locale` [E1+E2] - 注册 conversation 字典
  - 证据: `src/client/apply.ts:10 merge + src/client/apply.ts:159 ctx.locale.register(NS)`
- `dsh-client-shortcuts` [E1+E2] - 注册输入与停转固定快捷键
  - 证据: `src/client/apply.ts:14 ShortcutCommandId + src/client/apply.ts:236 ctx.inject(['shortcuts'])`
- `dsh-client-ui-layout` [编译依赖] - 会话内容布局约束
  - 证据: `src/client/contract/slots.ts:15 import @deepseek-ai/dsh-client-ui-layout/client`
- `dsh-client-ui-primitives` [编译依赖] - composer 图标与基础组件
  - 证据: `src/client/apply.ts:5 IconPaperclipOutlineRegular`
- `dsh-client-ui-renderer` [编译依赖] - 引入 slots 服务声明
  - 证据: `src/client/apply.ts:11 merge`
- `dsh-client-ui-session` [E1+E2] - 向会话 UI provide 会话/输入 hooks
  - 证据: `src/client/apply.ts:12 merge + src/client/apply.ts:283 ctx.uiSession.provide`
- `dsh-client-ui-settings` [E1+E2] - 读取 Enter 行为等运行时设置
  - 证据: `src/client/apply.ts:13 merge + src/client/input/submission-policy.ts:9 configForms`
- `dsh-commands` [编译依赖] - 命令记录节点类型
  - 证据: `src/client/contract/records.ts:5 import @deepseek-ai/dsh-commands`
- `dsh-goal` [编译依赖] - 目标模式输入提示
  - 证据: `src/client/skeleton/InputBar.tsx:26 import @deepseek-ai/dsh-goal`
- `dsh-llm` [编译依赖] - LLM 消息/请求检查类型
  - 证据: `src/client/contract/records.ts:6-7 + src/client/conversation/assembler.ts:4`
- `dsh-llm-retry` [编译依赖] - 重试记录节点类型
  - 证据: `src/client/contract/records.ts:9 import @deepseek-ai/dsh-llm-retry`
- `dsh-plan-mode` [编译依赖] - 计划模式输入提示
  - 证据: `src/client/skeleton/InputBar.tsx:24 import @deepseek-ai/dsh-plan-mode`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/apply.ts:8 SessionId`
- `dsh-settings` [E1+E2] - 宿主侧投影 busyEnter 为设置字段
  - 证据: `src/index.ts:2 import @deepseek-ai/dsh-settings + src/index.ts:31 settings.configure`
- `dsh-token-meter` [编译依赖] - 上下文占用计量显示
  - 证据: `src/client/context-occupancy.ts:1 import @deepseek-ai/dsh-token-meter/client`
- `dsh-tool-todo` [E1+E2] - Todo 记录与 Todo 停靠面板
  - 证据: `src/client/contract/records.ts:10 + src/client/apply.ts:550 ctx.plugin(todoDockEntry)`
- `dsh-workspace` [编译依赖] - 工作区实体类型
  - 证据: `src/client/contract/slots.ts:17 + src/client/skeleton/ConversationContent.tsx:3`

## Dependents (下游被依赖)
- `dsh-client-ui-agent-preset` - 获取 conversation.hero.*/session.header.actions 槽声明与 conversation 作用域
- `dsh-client-ui-approval` - 占用会话编辑器槽位以接管审批
- `dsh-client-ui-attachment` - 占据 composer/message/trajectory 图片槽位
- `dsh-client-ui-chat` - 消耗 conversation 视图与节点注册表，注册 Chat 视图
- `dsh-client-ui-commands` - 占据输入浮层槽位
- `dsh-client-ui-deliverables` - 注册交付物 ConversationNode 定义
- `dsh-client-ui-goal` - 注册 goal 命令输入节点定义并占用 input.dock 槽
- `dsh-client-ui-input-trigger` - 依赖 Conversation 声明的输入浮层槽
- `dsh-client-ui-jobs` - 依赖 Conversation 声明的会话头动作槽
- `dsh-client-ui-message-feedback` - 使用 ui-conversation 声明的 assistant-actions 与 input.overlay 槽
- `dsh-client-ui-model-selection` - 使用 ui-conversation 声明的 input.model 座位
- `dsh-client-ui-open-in-app` - 使用 ui-conversation 声明的会话头部槽
- `dsh-client-ui-permission-presets` - 使用 ui-conversation 声明的权限座位
- `dsh-client-ui-plan` - 使用会话 UI 的 Turn 末尾槽与 uiConversation 事件注册面
- `dsh-client-ui-schedule` - 注册 Turn 级日程定义并渲染 Turn 末尾卡
- `dsh-client-ui-sidebar-right` - 注册会话头部角槽需要其槽声明合并
- `dsh-client-ui-sidebar-terminal` - 引入会话头部动作槽类型，用于终端恢复入口（当前 index 中已注释）
- `dsh-client-ui-subagent` - 复用 ComposerChainProps/ConversationViewsProps 与内嵌 conversation slot
- `dsh-client-ui-tool` - 引入 MessageImageLoader/OpenFileOptions 与 conversation 节点类型
- `dsh-client-ui-trajectory` - 读取 trajectory target 并注册 conversation view Definition
- `dsh-client-ui-user-questions` - 接入 conversation.composer 链与 matched 货币
- `dsh-client-ui-workflow-run` - 注册会话节点定义并读取 ConversationNodeContext
- `dsh-client-ui-workspace` - 引入 conversation.hero.workspace 槽声明类型
- `dsh-experimental-client-ui-agent-team` - 在会话头部动作区渲染 Team 入口
- `dsh-experimental-client-ui-voice-input` - 在输入区渲染麦克风控件
- `dsh-session-log-export` - 声明会话头部工具插槽的运行时 props 类型
