# dsh-jobs-local

- 包名: `@deepseek-ai/dsh-jobs-local`
- 分组: G22 作业调度
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/jobs/jobs-local`

## 实现逻辑
以进程内内存实现 ctx.jobs 后台作业 seam：LocalJobRegistry 继承 JobRegistry 并用 Map 保存每条作业记录，OutputRing 提供 UTF-8 安全的有界输出环形缓冲与绝对偏移非消耗式读取 (src/ring.ts:38-113)，startPump 以有限轮询把作业的 pull 源排入环并在结算后做最终排空 (src/pump.ts:53-106)。JobEventHub 按注册 scope 分层路由注册/输出/进度/结算事件 (src/events.ts:43-93)。start/settle/kill/wait 处理 owner-session 隔离、每 owner 并发上限、首写胜出的结算与 teardown 级联取消 (src/index.ts:206-304, 577-607)。

## Provides
- ctx.jobs (进程内后台作业注册表实现，落实 dsh-jobs 定义的能力 seam，供 tool-jobs 等消费)
- ctx.jobs.events 事件流 (jobs.events.subscribe 按 scope/owner 过滤的 registered/output/progress/settled/removed 事件)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 把作业 owner 会话解析为活 Agent 实例并挂接其 scope 清理，实现按 owner 归属与生命周期取消
  - 证据: `src/index.ts:15 import type Agent + src/index.ts:359 ctx.get('agents')`
- `dsh-scope` [编译依赖] - 用 scope 分层存放控制器与订阅，使每 owner 的读与通知相对化
  - 证据: `src/events.ts:9 import ScopedLayers/scopeOf`
- `dsh-session` [编译依赖] - 以会话 id 做作业访问隔离鉴权（assertAccess 越权拒绝）
  - 证据: `src/index.ts:17 import type SessionId`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
