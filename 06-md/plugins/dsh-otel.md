# dsh-otel

- 包名: `@deepseek-ai/dsh-otel`
- 分组: G41 遥测与可观测性
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/telemetry/otel`

## 实现逻辑
OTel extends Service 以 'otel' 名注册 ctx.otel，本身不建队列/身份/连接，只暴露两个工厂方法 createEventReporter 与 createSessionLogReporter，每个通道各自独立 (src/index.ts:13-31)。普通事件通道用 SDK BatchLogRecordProcessor 做按条数批量，并把导出包在 got 实现的可取消 HTTP 传输上，shutdown 时销毁自有 agent (src/event-log.ts:40-93, src/event-transport.ts:16-56)。Session 日志通道自实现 SessionLogProcessor：入队前用 JsonLogsSerializer 实测字节，超 maxRequestBytes 整条拒绝而非截断，按字节/条数上限分批且同一时刻只允许一个在途请求 (src/session-log.ts:72-181)。传输层通过 createOtlpHttpExportDelegate + JsonLogsSerializer 构造显式 OTLP JSON exporter，不继承其它 collector 的 header/TLS 身份 (src/transport.ts:26-29, src/transport.ts:45-60)。

## Provides
- ctx.otel (独立 OTLP 日志通道工厂：普通事件按条数批量上报 + Session 日志按字节上限批量上报，两者队列与传输互不共享)

## Depends On (上游依赖)
- `dsh-session` [编译依赖] - Session 日志记录以 Session 事件信封与 SessionId 作为内容与身份载体（sessionId 与 content 由 reporter 强制赋值）
  - 证据: `package.json:41 peerDep + src/session-log.ts:2 import type { SessionEvent, SessionId }`

## Dependents (下游被依赖)
- `dsh-host-product-telemetry-otel` - 由共享 OTel 服务创建事件日志 reporter，本包只做产品分析策略适配
- `dsh-session-telemetry-otel` - 创建字节受限的 OTel 会话日志上报器
