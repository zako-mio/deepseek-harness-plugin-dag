# dsh-subagent-fork-in-process

- 包名: `@deepseek-ai/dsh-subagent-fork-in-process`
- 分组: G19 子代理
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/subagent/subagent-fork-in-process`

## 实现逻辑
ctx.subagents 的 fork provider 后端：apply 注册 ForkInProcessProvider。start() 通过 completedTurnPrefix(parent) 截取父会话截至最后 turn/end 的完整事件前缀作为种子，再调 startInProcessRun(request, {seed}) 创建继承父上下文的子代理；inheritsParentContext=true。

## Provides
- ctx.subagents 命名 provider 'fork'
- 继承父上下文能力声明

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - Agent 类型与 parent.session.header
  - 证据: `packages/subagent/subagent-fork-in-process/src/index.ts:13,49`
- `dsh-session` [编译依赖] - parent.session.events 截取种子
  - 证据: `packages/subagent/subagent-fork-in-process/src/index.ts:12,49`
- `dsh-subagent` [编译依赖] - inject subagents 注册 provider
  - 证据: `packages/subagent/subagent-fork-in-process/src/index.ts:28,93`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
