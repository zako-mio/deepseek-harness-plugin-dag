# dsh-client-ui-goal

- 包名: `@deepseek-ai/dsh-client-ui-goal`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 17
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-goal`

## 实现逻辑
GoalBar 停靠条：apply 先在 ctx.uiConversation.events 注册 goal-command-input 定义、注册 goal 字典，再把 GoalCommandInputView 以 key 'command-input' 注册进 'conversation.chat.node' (src/client/index.ts:68-75)，并把 GoalDock 以 order 10 注册进 'conversation.input.dock' (src/client/index.ts:92-144)。注入面为每会话建 createGoalActivationSource（读 session.projections.faceOf('goal') 并订阅 goal/activation-changed 与 connection/reset），再经 ctx.remote.goals 暴露 edit/pause/resume/clear 四个携带投影 CAS ref 的改动动词 (src/client/index.ts:97-142; src/client/slots.ts:47-63)。宿主半为空 apply (src/index.ts:9)。

## Provides
- slot: conversation.chat.node#command-input (GoalCommandInputView)
- slot: conversation.input.dock#goal (order 10 的 GoalBar 停靠条)
- Locale 命名空间 goal
- 会话投影响应面 hooks.goalActivation 与改动动词 onEdit/onPause/onResume/onClear (GoalBarInjected)
- SessionReferenceSourceMap 键 goalActivation (等待初始历史与 RPC 结果的活跃读取)
- 上抛 GoalBar/GoalDock 组件与 GoalActionResult/GoalBarActions 类型

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 目标 Remote 读取与 CAS 改动
  - 证据: `src/client/index.ts:15 ctx.remote merge + src/client/index.ts:112-140 ctx.remote.goals.get/edit/pause/resume/clear`
- `dsh-api-session-controller` [运行时依赖] - 保留会话并在初始历史打开后访问 Host
  - 证据: `src/client/index.ts:17 merge + src/client/index.ts:98-107 sessions.binding/using`
- `dsh-client-locale` [E1+E2] - 注册 goal 字典
  - 证据: `src/client/index.ts:23 merge + src/client/index.ts:69 ctx.locale.register(NS)`
- `dsh-client-ui-chat` [运行时依赖] - 依赖 Chat 声明的 conversation.chat.node 槽
  - 证据: `src/client/index.ts:19 merge + src/client/index.ts:71 slots.inject('conversation.chat.node')`
- `dsh-client-ui-conversation` [运行时依赖] - 注册 goal 命令输入节点定义并占用 input.dock 槽
  - 证据: `src/client/index.ts:21 merge + src/client/index.ts:68 ctx.uiConversation.events.register`
- `dsh-client-ui-primitives` [编译依赖] - 命令输入视图基础组件
  - 证据: `src/client/GoalCommandInputView.tsx:2 import @deepseek-ai/dsh-client-ui-primitives`
- `dsh-client-ui-renderer` [编译依赖] - 引入 slots 服务声明
  - 证据: `src/client/index.ts:25 merge`
- `dsh-client-ui-session` [编译依赖] - 声明 Session 标准 useProjection 座位
  - 证据: `src/client/index.ts:27 merge (useProjection 标准位)`
- `dsh-commands` [编译依赖] - goal 命令输入节点类型
  - 证据: `src/client/goal-command-input.ts:2-3 import @deepseek-ai/dsh-commands`
- `dsh-goal` [编译依赖] - 目标投影与目标标识类型
  - 证据: `src/client/GoalBar.tsx:12 + src/client/slots.ts:12 import GoalProjection/GoalId from @deepseek-ai/dsh-goal/client`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/index.ts:12 import SessionId from @deepseek-ai/dsh-session/types`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
