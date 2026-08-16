# dsh-session-checkpoint-policy

- 包名: `@deepseek-ai/dsh-session-checkpoint-policy`
- 分组: G07 会话持久化
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/session/session-checkpoint-policy`

## 实现逻辑
纯 apply(ctx) 函数插件，inject=['llm','sessionPersistence','sessions','tools']。在三处语义边界前强制 ctx.sessions.flush：llm/stream 包装器在延迟构造模型流之前 flush(失败即阻止 adapter dispatch)；tools/execute 在顶层工具分发前 flush；agent/pre-step 在每步请求前 flush。

## Provides
- ctx.on('llm/stream') 前置 flush 包装
- ctx.on('tools/execute') 顶层工具 flush 屏障
- ctx.on('agent/pre-step') 每步 flush

## Depends On (上游依赖)
- `dsh-agent` [组合依赖] - PreStepDecision 类型
  - 证据: `packages/session/session-checkpoint-policy/src/index.ts:11`
- `dsh-llm` [组合依赖] - StreamChunk 类型
  - 证据: `packages/session/session-checkpoint-policy/src/index.ts:9`
- `dsh-session` [编译依赖] - ctx.sessions.flush 强制持久化屏障
  - 证据: `packages/session/session-checkpoint-policy/src/index.ts:18,35,72,80`
- `dsh-tools` [组合依赖] - ToolExecutionResult 类型
  - 证据: `packages/session/session-checkpoint-policy/src/index.ts:10`

## Dependents (下游被依赖)
- `dsh-acp-demo` - ctx.plugin(sessionCheckpointPolicy) 强制 flush 屏障
