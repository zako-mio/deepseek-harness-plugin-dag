# dsh-agent-instructions

- 包名: `@deepseek-ai/dsh-agent-instructions`
- 分组: G22 上下文注入
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/context/agent-instructions`

## 实现逻辑
纯 apply(ctx, config) 函数插件。agent/pre-step 里先 next() 委托，等投影队列排空后 compose 基线+作用域指令并 syncInbox(inbox.prepend/replace/remove)；session/event 跟踪 step/turn 判定 openStep；tools/result 收集 read/write/edit 触碰路径，step 关闭后 queueProjection 串行重算指令版本并注入 inbox。ctx.get('fs') 可选。

## Provides
- agent/pre-step 指令上下文 compose/inbox 同步
- session/event step/turn 跟踪
- tools/result 文件触碰投影触发
- agent-instructions 源 user/message 注入

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - 订阅 agent/pre-step waterfall
  - 证据: `packages/context/agent-instructions/src/index.ts:322`
- `dsh-llm` [组合依赖] - createUserMessage
  - 证据: `packages/context/agent-instructions/src/index.ts:15`
- `dsh-session` [运行时依赖] - 订阅 session/event step 判定
  - 证据: `packages/context/agent-instructions/src/index.ts:305-314`
- `dsh-tools` [运行时依赖] - 订阅 tools/result 捕获触碰
  - 证据: `packages/context/agent-instructions/src/index.ts:350`

## Dependents (下游被依赖)
- `dsh-agent-spine-demo` - 可选 ctx.plugin(workspaceContext) 工作区上下文
