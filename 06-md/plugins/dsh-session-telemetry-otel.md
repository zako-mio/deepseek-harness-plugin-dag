# dsh-session-telemetry-otel

- 包名: `@deepseek-ai/dsh-session-telemetry-otel`
- 分组: G33 会话核心
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/session/session-telemetry-otel`

## 实现逻辑
OpenTelemetrySessionBackend 继承 SessionTelemetryBackend（注册 ctx.sessionTelemetry），组合 OTel SDK 的 LoggerProvider + BatchLogRecordProcessor + OTLP/HTTP exporter，把协调器交来的记录映射到 logger.emit（src/index.ts:156-267，日志器构造 src/index.ts:204-237）。FEEDBACK_ONLY 模式仅在显式 feedback 提交时经 SessionTelemetryCoordinator 捕获会话历史，DISABLED 不构造 SDK 仅告警（src/index.ts:168-175,242-266）；shutdown() 以自有外部截止时间约束 SDK 完整关闭路径（src/index.ts:294-309）。

## Provides
- ctx.sessionTelemetry (OpenTelemetry 遥测后端实现，按 feedback 授权捕获会话历史)

## Depends On (上游依赖)
- `dsh-command-feedback` [编译依赖] - 声明 feedback/record 等事件类型以判定授权事件
  - 证据: `src/index.ts:18 type import`
- `dsh-llm` [编译依赖] - 以 APP_IDENTITY 作为 OTel Resource 的 service.name/version
  - 证据: `src/index.ts:29 import`
- `dsh-message-feedback` [编译依赖] - 声明 feedback/message-put/delete 事件类型以判定本会话反馈
  - 证据: `src/index.ts:19 type import`
- `dsh-session` [E1+E2] - 监听会话事件以判定 feedback 授权并捕获历史
  - 证据: `src/index.ts:20 import + src/index.ts:157 static inject (sessions) + src/index.ts:246 ctx.on session/event`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
