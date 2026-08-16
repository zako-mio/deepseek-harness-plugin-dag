# dsh-jobs-local

- 包名: `@deepseek-ai/dsh-jobs-local`
- 分组: G16 作业
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/jobs/jobs-local`

## 实现逻辑
实现 JobRegistry 抽象(默认导出)的进程内版本：TrackedTask 全内存、snapshot 永不外泄 live state。start() 校验 owner controller 可达与 maxConcurrentJobsPerOwner 限额，创建 job 并挂 hooks.done settle；list/get/read/kill/wait 按 owner session-id 鉴权；onJobDone/onJobsChanged/attachController 经 ScopedLayers 分层注册，disposeAll 在 ctx teardown 时 cancel。

## Provides
- ctx.jobs(LocalJobRegistry)
- start/list/get/read/kill/wait
- onJobDone/onJobsChanged/attachController
- TASK_WAIT_TIMEOUT

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - job owner 生命周期
  - 证据: `packages/jobs/jobs-local/src/index.ts:14,46`

## Dependents (下游被依赖)
- `dsh-agent-spine-demo` - ctx.plugin(LocalJobRegistry) 进程内后台任务
- `dsh-tool-jobs` - controller 注册落地
