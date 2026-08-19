# dsh-llm-retry

- 包名: `@deepseek-ai/dsh-llm-retry`
- 分组: G06 LLM治理
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/llm/llm-retry`

## 为什么需要它（设计初衷）
按 provider 路由的 LLM 请求重试策略插件，为 LLM seam 注入容错。

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-llm-retry
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/llm/llm-retry

## 实现逻辑
Provider 路由的 LLM 请求重试策略插件(inject ['agents'])。apply() 订阅 agent/request-error 瀑布事件，按 ResolvedRetryPolicy 判定重试：retryableCodes 匹配、maxRetries 上限(经 session 事件日志查历史重试次数)、指数退避+抖动、providerRetryAfterMs 优先；每次重试先 agent.session.append('llm/retry') 持久化再等待。

## Provides
- agent/request-error 瀑布的 retry 恢复策略
- llm/retry、llm/retry-started 会话事件类型
- LlmRetryEventData 类型导出
- llm-retry-invariant

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - inject ['agents']；订阅 agent/request-error
  - 证据: `packages/llm/llm-retry/src/index.ts:21, 210-219`
- `dsh-llm` [编译依赖] - LlmFailure/ResolvedRetryPolicy 类型
  - 证据: `packages/llm/llm-retry/src/index.ts:12`
- `dsh-session` [运行时依赖] - agent.session.append('llm/retry')
  - 证据: `packages/llm/llm-retry/src/index.ts:13, 150, 182`

## Dependents (下游被依赖)
- `dsh-agent-spine-demo` - ctx.plugin(llmRetry) provider 路由重试
- `dsh-client-ui-conversation` - model-retry 节点事件类型
