# dsh-llm-retry

- 包名: `@deepseek-ai/dsh-llm-retry`
- 分组: G22 LLM 适配
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/llm/llm-retry`

## 实现逻辑
在 agent/request-error 扩展点上执行 provider 自带的重试策略：按 provider + policyKey 从 llmRetry 会话投影读取已重试次数与 retryId，据此决定是否继续退避，normal 模式超过 maxRetries 即交回下游 (src/index.ts:194-241, src/index.ts:125-138)。每次重试先追加 llm/retry 事件（含模式、延迟与失败事实）使其在等待前即可持久化，可取消延迟成功后再追加 llm/retry-started 并返回 retry 决定 (src/index.ts:149-192, src/index.ts:83-96)。延迟取 provider 给出的 retryAfter（超过 maxDelayMs 时按模式回退本地退避），否则用本地指数退避加对称抖动 (src/index.ts:59-64, src/index.ts:226-238)。插件处置时中止 lifetime 并等待所有在途恢复结束，防止已捕获的旧回调进入下游策略 (src/index.ts:254-258, src/index.ts:243-252)。

## Provides
- agent/request-error waterfall 监听器（provider 路由重试策略执行器）
- Session 投影 llmRetry（按 provider + 策略的当前重试状态）
- Session 事件 llm/retry 与 llm/retry-started（可回放的重试时序）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 重试策略挂在 agent 循环的请求错误恢复扩展点上
  - 证据: `src/index.ts:12 import type { Agent, RequestErrorAction } + src/index.ts:22 inject ['agents'] + src/index.ts:243 ctx.on('agent/request-error')`
- `dsh-llm` [编译依赖] - 失败事实与解析后的重试策略类型由 LLM seam 定义
  - 证据: `src/index.ts:13 import type { LlmFailure, ResolvedRetryPolicy } + src/types.ts:1 dsh-llm/types`
- `dsh-session` [编译依赖] - 重试事件注册进会话事件映射并写入 agent.session
  - 证据: `package.json:37 peerDep + src/types.ts:6 declare module '@deepseek-ai/dsh-session/types'（llm/retry 事件声明）`
- `dsh-session-projection` [E1+E2] - 重试计数必须由会话日志投影恢复，重启后不重置
  - 证据: `src/index.ts:14 import type {} + src/index.ts:125 ctx.sessionProjections.register + src/index.ts:220 stateOf`

## Dependents (下游被依赖)
- `dsh-client-ui-chat` - 重试节点与轮次尾部类型
- `dsh-client-ui-conversation` - 重试记录类型
- `dsh-token-meter` - 识别 llm/retry-started 以正确区分一次 Turn 内的多次尝试
