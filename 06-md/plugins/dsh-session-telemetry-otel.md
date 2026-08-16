# dsh-session-telemetry-otel

- 包名: `@deepseek-ai/dsh-session-telemetry-otel`
- 分组: G07 会话持久化
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/session/session-telemetry-otel`

## 实现逻辑
以 OpenTelemetrySessionBackend 类(extends SessionTelemetryBackend)默认导出，static inject=['sessions']。FULL 模式构造 LoggerProvider+BatchLogRecordProcessor+OTLPLogExporter 并 new SessionTelemetryCoordinator(ctx, backend, 'live') 全量跟随；FEEDBACK_ONLY 模式 coordinator 走 'on-demand' 并注册 feedback/record 监听；DISABLED 不建 SDK。记录映射为 logger.emit()，shutdown 带超时竞速。

## Provides
- ctx.sessionTelemetry 服务
- SessionTelemetryCoordinator 组合
- OTel 日志管道
- feedback/record 捕获监听

## Depends On (上游依赖)
- `dsh-llm` [组合依赖] - APP_IDENTITY
  - 证据: `packages/session/session-telemetry-otel/src/index.ts:27`
- `dsh-session` [编译依赖] - static inject sessions; feedback 校验
  - 证据: `packages/session/session-telemetry-otel/src/index.ts:148,247`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
