# dsh-client-ui-goal

- 包名: `@deepseek-ai/dsh-client-ui-goal`
- 分组: G27 会话交互UI
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-goal`

## 实现逻辑
GoalBar 输入坞。投影模式 surface：goal 实时值经 session.projections.faceOf('goal') 读取（不持 store/事件监听）；goalCommandInputDefinition（match command/run name=goal）注册进 conversationEvents，以 keyed 'command-input' 渲染 /goal 命令行输入；GoalDock 注册进 conversation.input.dock（id=goal, order=10），inject 封装四个 mutation verb——onEdit/onPause/onResume/onClear 经 ctx.remote.goals.edit/pause/resume/clear（携带 CAS ref：goal.id+revision，由 host 对账）。

## Provides
- conversation.input.dock id=goal(GoalDock/GoalBar)
- conversation.chat.node keyed 'command-input'(GoalCommandInputView)
- ConversationNodeDefinition 'goal-command-input'
- ChatNodeDataMap 'command-input' 合并

## Depends On (上游依赖)
- `dsh-api-remotes` [运行时依赖] - goal 域 Remote 端点（host goals 服务）
  - 证据: `index.ts:13 type-only + index.ts:41 inject remote.goals + index.ts:81/86/91/96 ctx.remote.goals.edit/pause/resume/clear`
- `dsh-client-locale` [编译依赖] - goal 命名空间字典
  - 证据: `index.ts:17 type-only + index.ts:49 locale.register`
- `dsh-client-runtime` [编译依赖] - 会话绑定与投影 face
  - 证据: `index.ts:11 ClientContext,SessionId`
- `dsh-client-ui-conversation` [编译依赖] - 消费 input.dock 座位与 conversationEvents 注册表
  - 证据: `index.ts:15 type-only + index.ts:51-55/72-99 注册 input.dock 与 chat.node + package.json:52`
- `dsh-client-ui-primitives` [编译依赖] - UI atoms
  - 证据: `GoalBar.tsx:13-16 图标 + Tooltip`
- `dsh-commands` [编译依赖] - command/run 事件与 CommandId 契约
  - 证据: `goal-command-input.ts:2-3 dsh-commands/brand,types + package.json:55`
- `dsh-goal` [编译依赖] - goal 投影 key 类型与 GoalRef 契约
  - 证据: `index.ts:19 dsh-goal/client + package.json:56 peerDependencies`
- `dsh-session` [编译依赖] - SessionEvent<'command/run'> 类型
  - 证据: `goal-command-input.ts:1 dsh-session/types`
- `dsh-session-projection` [运行时依赖] - goal 会话投影读取（CAS ref 来源）
  - 证据: `index.ts:19 GoalProjection/GoalRef 类型 + index.ts:61-65 sessions.binding(sessionId).session.projections.faceOf('goal')`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
