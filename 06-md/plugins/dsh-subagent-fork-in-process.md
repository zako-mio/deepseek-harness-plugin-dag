# dsh-subagent-fork-in-process

- 包名: `@deepseek-ai/dsh-subagent-fork-in-process`
- 分组: G41 子代理
- 拓扑层: Layer 7
- 来源层: L1 核心集
- 源码路径: `packages/subagent/subagent-fork-in-process`

## 实现逻辑
以 ForkInProcessProvider 注册 in-process provider fork（默认名），支持全部启动能力且 inheritsParentContext=true (src/index.ts:63-83)。start() 取父会话最后一个 turn/end 之前的平衡前缀作为 seed，交给共享 in-process driver 执行 (src/index.ts:48-83)。prepareContinuable() 在创建时一次性捕获同一前缀，作为可续子代理的 seed，冷恢复时重放该前缀而非重新 fork (src/index.ts:85-91)。

## Provides
- ctx.subagents 注册的 provider `fork` (继承父会话已完成轮次的 in-process 子代理)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 从父 Agent 会话日志切取 seed
  - 证据: `src/index.ts:13 (import type Agent)`
- `dsh-session` [编译依赖] - seed 事件的会话事件类型
  - 证据: `src/index.ts:12 (import type SessionEvent)`
- `dsh-subagent` [E1+E2] - 实现并注册 fork provider
  - 证据: `src/index.ts:14-20 (import 类型) + src/index.ts:28 (static inject ['subagents']) + src/index.ts:95 (ctx.subagents.registerProvider)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
