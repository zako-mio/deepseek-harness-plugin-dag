# dsh-client-ui-goal

- 包名: `@deepseek-ai/dsh-client-ui-goal`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-goal`

## 实现逻辑
浏览器半在 conversation.input.dock 注册 GoalBar 条目、在 conversation.chat.node 注册 command-input 渲染器，并把 goalCommandInputDefinition 注册进 ctx.uiConversation.events（src/client/index.ts:67-75）。注入面从 Session 的 goal 投影读当前 CAS ref，经 ctx.remote.goals 暴露 edit/pause/resume/clear 四个变更动词，并用 registrant-private 的 goalActivation 源承载 Remote 读取与 goal/activation-changed、connection/reset 订阅（src/client/index.ts:79-144）。

## Provides

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 调用 goals Remote 并订阅激活变更
  - 证据: `src/client/activation-source.ts:3 import + src/client/index.ts:115 ctx.remote.$on('goal/activation-changed')`
- `dsh-api-session-controller` [E1+E2] - 按会话取投影并用 using 保留引用
  - 证据: `src/client/index.ts:17 import type + src/client/index.ts:81 sessions.binding(sessionId)`
- `dsh-client-locale` [E1+E2] - 注册 goal 字典
  - 证据: `src/client/index.ts:23 import type + src/client/index.ts:69 ctx.locale.register(NS)`
- `dsh-client-ui-chat` [编译依赖] - 占用 chat 节点槽位声明
  - 证据: `src/client/index.ts:19 import type`
- `dsh-client-ui-conversation` [E1+E2] - 注册命令输入事件定义
  - 证据: `src/client/index.ts:21 import type + src/client/index.ts:68 ctx.uiConversation.events.register`
- `dsh-client-ui-primitives` [编译依赖] - 复用基础控件渲染命令输入
  - 证据: `src/client/GoalCommandInputView.tsx:2 import`
- `dsh-client-ui-renderer` [编译依赖] - 渲染器槽位服务类型
  - 证据: `src/client/index.ts:25 import type`
- `dsh-client-ui-session` [编译依赖] - 会话标准 seat 类型
  - 证据: `src/client/index.ts:27 import type`
- `dsh-commands` [编译依赖] - 命令输入事件类型
  - 证据: `src/client/goal-command-input.ts:2 import + src/client/goal-command-input.ts:3 import`
- `dsh-goal` [编译依赖] - 复用 goal 投影与 Remote 契约类型
  - 证据: `src/client/GoalBar.tsx:12 import + src/client/index.ts:29 import type`
- `dsh-session` [编译依赖] - SessionId 与事件类型
  - 证据: `src/client/goal-command-input.ts:1 import + src/client/index.ts:12 import type`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
