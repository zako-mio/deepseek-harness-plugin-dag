# dsh-host-product-telemetry-otel

- 包名: `@deepseek-ai/dsh-host-product-telemetry-otel`
- 分组: G19 宿主服务
- 拓扑层: Layer 1
- 来源层: L2 web-app
- 源码路径: `packages/host/product-telemetry-otel`

## 实现逻辑
把产品分析事件接到共享 OTel 服务上：默认导出 ProductTelemetry 继承 cordis Service，以 static inject ['otel'] 与 super(ctx,'productTelemetry') 注册服务 (src/index.ts:61-84)。构造期校验 endpoint 为合法 HTTP(S) URL、channel 是合法 header 值、maxExportBatchSize 不超过 maxQueueSize，再经 ctx.otel.createEventReporter 建立批量导出 reporter（resource / scope / processor 均由配置驱动） (src/index.ts:66-97)。emit(record) 只做入队、不等待网络投递；ctx.effect 注册的 disposer 在 shutdownTimeoutMillis 内 drain，超时则 abort 并告警 (src/index.ts:99-120)。

## Provides
- ctx.productTelemetry（ProductTelemetry 服务：emit(record) 入队一条产品分析事件）
- ProductTelemetryRecord / ProductTelemetryScalar 类型与 Config（endpoint / channel / serviceName / serviceVersion 等）

## Depends On (上游依赖)
- `dsh-otel` [E1+E2] - 由共享 OTel 服务创建事件日志 reporter，本包只做产品分析策略适配
  - 证据: `src/index.ts:6 import type EventLogReporter / OTelEventRecord + src/index.ts:62 static inject ['otel'] + src/index.ts:85 ctx.otel.createEventReporter`

## Dependents (下游被依赖)
- `dsh-client-product-analytics` - 把产品事件交给 OTel 遥测出口
