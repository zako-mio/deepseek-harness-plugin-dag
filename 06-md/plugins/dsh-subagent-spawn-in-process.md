# dsh-subagent-spawn-in-process

- 包名: `@deepseek-ai/dsh-subagent-spawn-in-process`
- 分组: G19 子代理
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/subagent/subagent-spawn-in-process`

## 实现逻辑
ctx.subagents 的 spawn provider 后端：apply 直接 ctx.subagents.registerProvider(new SpawnInProcessProvider(config.providerName))。声明全部 4 项能力(outputSchema/depthLimit/toolFilter/persona)，inheritsParentContext=false；start() 委托共享驱动 startInProcessRun 走 ctx.agents.create 全新子代理；prepareContinuable 返回空 spec。

## Provides
- ctx.subagents 命名 provider 'spawn'
- 子代理能力声明: outputSchema/depthLimit/toolFilter/persona

## Depends On (上游依赖)
- `dsh-agent` [组合依赖] - 子代理经 ctx.agents 工厂创建
  - 证据: `packages/subagent/subagent-spawn-in-process/package.json:45`
- `dsh-subagent` [编译依赖] - inject subagents 注册 provider
  - 证据: `packages/subagent/subagent-spawn-in-process/src/index.ts:22,63`
- `dsh-tools` [组合依赖] - 子代理工具链由 agents 工厂提供
  - 证据: `packages/subagent/subagent-spawn-in-process/src/index.ts:20-21`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
