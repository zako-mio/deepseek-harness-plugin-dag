# dsh-llm-retry

- 包名: `@deepseek-ai/dsh-llm-retry`
- 分组: G23 LLM 适配
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/llm/llm-retry`

## 实现逻辑
在 agent loop 的 agent/request-error 恢复扩展点上实现按 provider 路由的模型请求重试：按 ResolvedRetryPolicy 的 normal/always 模式与可重试错误码判定是否重试，计算指数退避加抖动并做可取消等待 (src/index.ts:194-241, 59-64)。每次调度先 append 持久的 llm/retry 事件、等待成功后再记 llm/retry-started，并把每 provider/policy 的重试计数保存在 sessionProjections 的 llmRetry 状态中 (src/index.ts:125-138, 188-191)。invariant.ts 的 companion 校验这些持久记录与当前打开的 turn/step、路由 provider 与策略链一致 (src/invariant.ts:45-146)。

## Provides
- agent/request-error 恢复策略执行器 (按 provider 路由的退避重试，normal/always 两种模式)
- llm/retry 与 llm/retry-started 持久会话事件，以及 llmRetry session projection 状态

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 在 agent 请求错误恢复点上裁决是否重试，并把重试写入 agent.session
  - 证据: `src/index.ts:12 import type Agent/RequestErrorAction + src/index.ts:22 inject agents`
- `dsh-invariants` [E1+E2] - 注册包拥有的重试持久事件不变量 companion
  - 证据: `src/invariant.ts:7 import type InvariantInstaller + src/invariant.ts:178 ctx.invariants.register`
- `dsh-llm` [编译依赖] - 消费 provider 中立失败事实与已解析的重试策略类型
  - 证据: `src/index.ts:13 import type LlmFailure/ResolvedRetryPolicy + src/types.ts:1 import from dsh-llm/types`
- `dsh-session` [E1+E2] - 向会话日志追加持久重试事件并回放校验既有记录
  - 证据: `src/history.ts:3 import type SessionEvent + src/invariant.ts:160 ctx.sessions.list`
- `dsh-session-projection` [E1+E2] - 注册 llmRetry projection 以在重试间保持每 provider/策略的尝试计数
  - 证据: `src/index.ts:14 import type {} + src/index.ts:125 ctx.sessionProjections.register`

## Dependents (下游被依赖)
- `dsh-client-ui-chat` - 模型重试节点与 turn 过程融合
- `dsh-client-ui-conversation` - 重试记录节点类型
- `dsh-token-meter` - 识别 llm/retry-started 以正确区分一次 Turn 内的多次尝试
