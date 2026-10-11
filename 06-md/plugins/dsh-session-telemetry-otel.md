# dsh-session-telemetry-otel

- 包名: `@deepseek-ai/dsh-session-telemetry-otel`
- 分组: G31 会话核心
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/session/session-telemetry-otel`

## 实现逻辑
实现会话遥测 seam 的 OpenTelemetry 后端：构造时按 mode 分 FEEDBACK_ONLY 与 DISABLED，DISABLED 只对本地反馈告警，FEEDBACK_ONLY 则校验 exporter.url 为 http(s) 与 shutdownTimeoutMillis 上界后创建 SessionLogReporter (src/index.ts:152-202)。捕获是 on-demand 且带历史：仅当事件属于本会话的 feedback/record 或指向本会话的 feedback/message-*，且确为日志中已追加的那一条，才授权 coordinator.captureSession 回放该前缀 (src/index.ts:43-51, src/index.ts:223-232)。feedback/committed 提交面会先 detached 克隆 inspection、用 Session.fromRestore 重建会话，再走同一授权路径 (src/index.ts:233-243)。emit 直接丢弃直投记录，shutdown 用外层 deadline 与 provider.shutdown() 竞争，超时则 stopPending 并拒绝 (src/index.ts:251-275)。

## Provides
- ctx.sessionTelemetry (OpenTelemetry 会话遥测后端实现：反馈授权的日志上报、shutdown 截止期与共享策略)
- SessionTelemetryMode / DEFAULT_TELEMETRY_MODE (FEEDBACK_ONLY 与 DISABLED 的共享策略枚举)

## Depends On (上游依赖)
- `dsh-command-feedback` [编译依赖] - 识别命令反馈事件类型以判定捕获授权
  - 证据: `package.json:34 peerDep + src/index.ts:14 import type {}；src/index.ts:46 case 'feedback/record'`
- `dsh-llm` [编译依赖] - 取产品身份写入 OTel resource 属性
  - 证据: `package.json:36 peerDep + src/index.ts:25 import APP_IDENTITY`
- `dsh-message-feedback` [E1+E2] - 在消息反馈提交时授权捕获该前缀
  - 证据: `package.json:35 peerDep + src/index.ts:15 import type {}；src/index.ts:233 ctx.on('feedback/committed')（packages/feedback/message-feedback/src/index.ts:58 声明、:271 触发）`
- `dsh-otel` [E1+E2] - 创建字节受限的 OTel 会话日志上报器
  - 证据: `package.json:41 peerDep + src/index.ts:27 import type LogExporterOptions/SessionLogReporter；src/index.ts:145 static inject 'otel'、src/index.ts:190 ctx.otel.createSessionLogReporter`
- `dsh-session` [E1+E2] - 订阅会话事件做反馈授权，并核对事件是否为日志中的那一条
  - 证据: `package.json:37 peerDep + src/index.ts:16 import Session/SessionEvent；src/index.ts:159 与 src/index.ts:223 ctx.on('session/event')`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
