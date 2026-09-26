# dsh-subagent-spawn-in-process

- 包名: `@deepseek-ai/dsh-subagent-spawn-in-process`
- 分组: G41 子代理
- 拓扑层: Layer 7
- 来源层: L1 核心集
- 源码路径: `packages/subagent/subagent-spawn-in-process`

## 实现逻辑
以 SpawnInProcessProvider 注册 in-process provider spawn（默认名），支持全部启动能力且 inheritsParentContext=false (src/index.ts:41-59)。start() 不传 seed，直接调用共享 in-process driver 执行一个全新子代理 (src/index.ts:54-59)。prepareContinuable() 贡献空 spec（新子代理无继承历史），其后的生命周期全部由 continuation 管理器接管 (src/index.ts:61-65)。

## Provides
- ctx.subagents 注册的 provider `spawn` (全新 in-process 子代理)

## Depends On (上游依赖)
- `dsh-subagent` [E1+E2] - 实现并注册 spawn provider
  - 证据: `src/index.ts:14-16 (import 类型) + src/index.ts:22 (static inject ['subagents']) + src/index.ts:69 (ctx.subagents.registerProvider)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
