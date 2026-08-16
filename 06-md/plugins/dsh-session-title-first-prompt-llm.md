# dsh-session-title-first-prompt-llm

- 包名: `@deepseek-ai/dsh-session-title-first-prompt-llm`
- 分组: G08 会话展示
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/session/session-title-first-prompt-llm`

## 实现逻辑
首条人类消息的 LLM 标题 provider 薄插件。apply(ctx, config) 直接调用 @deepseek-ai/dsh-session-title-llm 的 registerSessionTitleLlmProvider，以 'first-prompt' 自动模式注册 provider，消息选择器取 messages[0]。

## Provides
- 向 ctx.sessionTitle 注册 first-prompt LLM provider
- Config schema(复用共享字段)

## Depends On (上游依赖)
- `dsh-llm` [运行时依赖] - LLM 服务调用
  - 证据: `packages/session/session-title-first-prompt-llm/src/index.ts:12`
- `dsh-session` [运行时依赖] - 会话服务访问
  - 证据: `packages/session/session-title-first-prompt-llm/src/index.ts:12`
- `dsh-session-title` [运行时依赖] - 注册进标题服务
  - 证据: `packages/session/session-title-first-prompt-llm/src/index.ts:12,35`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
