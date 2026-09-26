# dsh-session-log-deepseek

- 包名: `@deepseek-ai/dsh-session-log-deepseek`
- 分组: G33 会话核心
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/session/session-log-deepseek`

## 实现逻辑
向 DeepSeek 官方 LLM API 请求贡献增量 dsh_session_log 字段：acceptedThrough() 折叠本会话的 delivery-accepted 事件得到已确认水位（src/index.ts:141-175），prepare 从该水位起按 maxBytes 打包最长可容纳的事件前缀，并把 header/事件翻译为线格式（src/index.ts:182-243）。接受时追加 session-log-deepseek/delivery-accepted 事件记录水位，使重启后能保守重发不确定尾部（src/index.ts:233-240）。invariant.ts 校验水位字段与所在事件/会话的一致性（src/invariant.ts:17-57）。

## Provides
- DeepSeek 官方请求的 dsh_session_log 增量会话日志扩展（注册于 ctx.deepseekLlmApiExtensions）

## Depends On (上游依赖)
- `dsh-deepseek-llm-api-extensions` [运行时依赖] - 把 dsh_session_log 字段注册到官方 DeepSeek 请求扩展点
  - 证据: `src/index.ts:12 type import + src/index.ts:36 static inject + src/index.ts:186 ctx.deepseekLlmApiExtensions.register`
- `dsh-invariants` [E1+E2] - 注册水位字段的运行时不变式
  - 证据: `src/invariant.ts:6 import + src/invariant.ts:75 ctx.invariants.register`
- `dsh-session` [E1+E2] - 从会话日志读取待上传事件并追加接受水位事件
  - 证据: `src/index.ts:13 import + src/index.ts:36 static inject (sessions) + src/index.ts:190 ctx.sessions.get`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
