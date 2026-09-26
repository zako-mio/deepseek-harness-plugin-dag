# dsh-subagent-dsh-sdk

- 包名: `@deepseek-ai/dsh-subagent-dsh-sdk`
- 分组: G41 子代理
- 拓扑层: Layer 7
- 来源层: L3 其余
- 源码路径: `packages/subagent/subagent-dsh-sdk`

## 实现逻辑
以 SdkSubagentProvider 注册 provider dsh-sdk，仅支持 agentOptions 能力（provider/model/reasoning/maxTokens）(src/index.ts:110-175)。start() 经 @deepseek-ai/dsh-sdk-client 的 DeepSeekHarness 以 stdio JSON-RPC 启动带独立 profile/patch/dshHome 的嵌套 DSH 运行时，并用 scrubbedParentEnv 清洗环境 (src/run.ts:233-254)。握手成功后驱动 session.run，按子运行时的 turn/end 理由映射 stopReason，dispose 通过 harness.close() 关闭并回收 (src/run.ts:147-182, 307-358)。

## Provides
- ctx.subagents 注册的 provider `dsh-sdk` (嵌套 DSH 运行时进程外子代理)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 解析并合并子代理 route 选项
  - 证据: `src/index.ts:18 (import type AgentOptions)`
- `dsh-llm` [编译依赖] - 内容块与推理强度类型
  - 证据: `src/run.ts:23 (import type ContentBlock, ReasoningEffortId)`
- `dsh-session` [编译依赖] - 读取子会话事件与终态理由
  - 证据: `src/run.ts:24 (import type SessionEvent, SessionId, TurnEndReason)`
- `dsh-subagent` [E1+E2] - 复用 seam 契约与共享辅助并注册 provider
  - 证据: `src/index.ts:19-20 (import NO_START_CAPABILITIES, resolveChildCwd, validateConfiguredCwd, 类型) + src/index.ts:31 (inject ['subagents']) + src/index.ts:199 (ctx.subagents.registerProvider)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
