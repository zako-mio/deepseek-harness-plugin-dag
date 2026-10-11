# dsh-client-ui-conversation

- 包名: `@deepseek-ai/dsh-client-ui-conversation`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 13
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-conversation`

## 实现逻辑
会话外壳装配点：apply 构造 UiConversation（ctx.uiConversation，目标中立的会话注册表与按会话装配）与 ConversationController（ctx.conversation，作用域寻址的会话动作与输入注册表）（src/client/apply.ts:142-146、src/client/conversation/assembly.ts:201、src/client/service.ts:185）。它注册 shell/输入/队列/待办等槽位与设置行，管理草稿、附件上传（maxConcurrentFileUploads 配置）与提交策略，并把 Remote 会话流接入 ConversationNodeAssembler（src/client/apply.ts:56-69、src/client/index.ts:2-14）。Host 半只投影 busyEnter 偏好并关闭自动设置文档（src/index.ts:23-32）。

## Provides
- ctx.conversation (作用域寻址的会话动作与每会话输入注册表)
- ctx.uiConversation (目标中立的会话注册表、节点/视图装配与按会话快照)
- 会话输入/队列/待办等槽位声明 (src/client/apply.ts:154-169)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - Agent 类型
  - 证据: `src/client/input/facade.ts:12 import + src/client/input/hub.ts:17 import`
- `dsh-api-session-controller` [E1+E2] - 会话绑定、作用域与事件流
  - 证据: `src/client/apply.ts:5 import type + src/client/apply.ts:153 ctx.sessions`
- `dsh-api-workspace-controller` [编译依赖] - 工作区控制器类型与状态
  - 证据: `src/client/contract/slots.ts:6 import + src/client/skeleton/ConversationContent.tsx:4 import`
- `dsh-client-file-upload` [E1+E2] - 草稿文件上传走 fileUpload 服务
  - 证据: `src/client/contract/slots.ts:5 import + src/client/service.ts:19 import`
- `dsh-client-locale` [E1+E2] - 注册 conversation 字典
  - 证据: `src/client/apply.ts:11 import type + src/client/apply.ts:160 ctx.locale`
- `dsh-client-product-analytics` [E1+E2] - 提交行为埋点
  - 证据: `src/client/apply.ts:2 import type + src/client/input/submission-analytics.ts:3 import`
- `dsh-client-shortcuts` [E1+E2] - 注册停止/提交快捷键
  - 证据: `src/client/apply.ts:15 import type + src/client/stop-shortcut.ts:3 import`
- `dsh-client-ui-layout` [编译依赖] - 布局槽位类型
  - 证据: `src/client/contract/slots.ts:15 import`
- `dsh-client-ui-primitives` [编译依赖] - 复用基础控件与图标
  - 证据: `src/client/apply.ts:6 import + src/client/input/editor/ReferenceChip.tsx:8 import`
- `dsh-client-ui-renderer` [编译依赖] - 渲染器槽位服务类型
  - 证据: `src/client/apply.ts:12 import type`
- `dsh-client-ui-session` [E1+E2] - 提供会话标准 hooks/seat
  - 证据: `src/client/apply.ts:13 import type + src/client/apply.ts:284 ctx.uiSession.provide`
- `dsh-client-ui-settings` [编译依赖] - 注册提交行为设置行
  - 证据: `src/client/apply.ts:14 import type + src/client/input/submission-policy.ts:9 import`
- `dsh-commands` [编译依赖] - 命令记录类型
  - 证据: `src/client/contract/records.ts:5 import`
- `dsh-goal` [编译依赖] - 目标投影类型
  - 证据: `src/client/input/hub.ts:10 import + src/client/skeleton/InputBar.tsx:26 import`
- `dsh-llm` [编译依赖] - 助手记录与请求检查类型
  - 证据: `src/client/contract/records.ts:6 import + src/client/service.ts:28 import`
- `dsh-llm-retry` [编译依赖] - 重试记录类型
  - 证据: `src/client/contract/records.ts:9 import`
- `dsh-plan-mode` [编译依赖] - 计划模式投影类型
  - 证据: `src/client/input/hub.ts:9 import + src/client/skeleton/InputBar.tsx:24 import`
- `dsh-session` [编译依赖] - 会话事件与快照类型
  - 证据: `src/client/apply.ts:9 import type + src/client/service.ts:20 import`
- `dsh-settings` [E1+E2] - 关闭该服务的自动设置文档
  - 证据: `src/index.ts:2 import type + src/index.ts:31 ctx.inject(['settings'])`
- `dsh-token-meter` [编译依赖] - 上下文占用展示
  - 证据: `src/client/context-occupancy.ts:1 import + src/client/skeleton/ContextMeter.tsx:11 import`
- `dsh-tool-todo` [编译依赖] - 待办记录类型与面板
  - 证据: `src/client/contract/records.ts:10 import + src/client/skeleton/TodoPanel.tsx:8 import`
- `dsh-workspace` [编译依赖] - 工作区实体类型
  - 证据: `src/client/contract/slots.ts:17 import + src/client/skeleton/ConversationContent.tsx:3 import`

## Dependents (下游被依赖)
- `dsh-client-ui-agent-preset` - 占用 conversation.hero 与 header 槽位声明
- `dsh-client-ui-approval` - 占用会话编辑器槽位以接管审批
- `dsh-client-ui-attachment` - 占据 composer/message/trajectory 图片槽位
- `dsh-client-ui-chat` - 注册 chat 目标、节点与视图槽位
- `dsh-client-ui-commands` - 占用输入覆盖层槽位渲染 popup
- `dsh-client-ui-deliverables` - 注册 deliverables 事件定义
- `dsh-client-ui-goal` - 注册命令输入事件定义
- `dsh-client-ui-input-trigger` - 依赖 Conversation 声明的输入浮层槽
- `dsh-client-ui-jobs` - 占用 header actions 槽位声明
- `dsh-client-ui-message-feedback` - 使用 ui-conversation 声明的 assistant-actions 与 input.overlay 槽
- `dsh-client-ui-model-selection` - 占用 conversation.input.model 槽位声明
- `dsh-client-ui-open-in-app` - 占用会话头槽位声明
- `dsh-client-ui-permission-presets` - 占用 conversation.input.permission 槽位声明
- `dsh-client-ui-plan` - 注册会话事件定义与输入槽位
- `dsh-client-ui-schedule` - Turn 级卡片需向 conversation 的事件注册表登记 Definition，并复用其节点类型
- `dsh-client-ui-sidebar-right` - 扩展按钮注册进 conversation.session.header.corner，需该槽已声明
- `dsh-client-ui-sidebar-terminal` - （已停用分支）恢复入口原注册进会话头部动作槽
- `dsh-client-ui-subagent` - composer 链与会话视图契约由 ui-conversation 声明
- `dsh-client-ui-tool` - conversation.chat.node 槽与图片加载契约由 ui-conversation 声明
- `dsh-client-ui-trajectory` - 会话视图槽、事件定义注册表与 trajectory 目标快照均由 ui-conversation 提供
- `dsh-client-ui-user-questions` - composer 链、会话节点注册表与 conversation.chat.node 槽由 ui-conversation 提供
- `dsh-client-ui-workflow-run` - 节点定义注册表与 conversation.chat.node 槽由 ui-conversation 提供
- `dsh-client-ui-workspace` - conversation.hero.workspace 槽由 ui-conversation 声明
- `dsh-experimental-client-ui-agent-team` - 在会话头部动作区渲染 Team 入口
- `dsh-experimental-client-ui-claude-code-mods` - 类型面需要会话 UI 声明以定位输入区槽位
- `dsh-experimental-client-ui-voice-input` - 输入区活动槽位与转写文本插入会话输入框需要会话 UI 的类型面
- `dsh-experimental-session-inspector` - 聊天侧节点与分组来自会话 UI 的绑定与快照
- `dsh-session-log-export` - 声明会话头部工具插槽的运行时 props 类型
