# dsh-session-log-deepseek

- 包名: `@deepseek-ai/dsh-session-log-deepseek`
- 分组: G31 会话核心
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/session/session-log-deepseek`

## 实现逻辑
向官方 DeepSeek 请求注册增量会话日志字段 dsh_session_log：apply 在 deepseekLlmApiExtensions.register 的 prepare 钩子内按水位取待上传事件前缀，逐条累加 JSON 字节数直到超过 maxBytes，产出带 version/sessionFormatVersion/session/afterSeq/throughSeq/events 的信封 (src/index.ts:184-246)。水位由日志中 session-log-deepseek/delivery-accepted 事件的 throughSeq 折叠得出，并用 WeakMap 缓存已扫描偏移与阻塞告警位置，避免重复扫描与重复告警 (src/index.ts:143-177, src/index.ts:61-63)。请求被接受时 accept() 追加投递确认事件，使重启后能保守重发不确定的尾部而不另建存储 (src/index.ts:236-243)。类型层把会话 header/event 收敛为原始 JSON 原语，并通过 declare module 把投递确认事件并入 SessionEventMap (src/types.ts:30-56, src/types.ts:78-89)。

## Provides
- deepseekLlmApiExtensions 注册项 dsh_session_log (官方 DeepSeek 请求携带的增量会话日志字段与投递确认水位)

## Depends On (上游依赖)
- `dsh-deepseek-llm-api-extensions` [E1+E2] - 注册并参与构建 DeepSeek 请求的扩展字段
  - 证据: `package.json:41 peerDep + src/index.ts:12 import type {}；src/index.ts:187 ctx.deepseekLlmApiExtensions.register`
- `dsh-session` [E1+E2] - 按 sessionId 取会话、读日志事件并追加投递确认
  - 证据: `package.json:42 peerDep + src/index.ts:13 import SessionLogOffset/SessionSeq；src/index.ts:192 ctx.sessions.get`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
