# dsh-jobs-local

- 包名: `@deepseek-ai/dsh-jobs-local`
- 分组: G16 作业
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/jobs/jobs-local`

## 为什么需要它（设计初衷）
解决 agent 后台任务（jobs）的进程内注册表实现：提供 LocalJobRegistry，按所属者(owner)管理并发上限（默认 10），任务归属 owner/后端而非执行光纤，使生产者与控制器重载后任务不中断，为模型提供 job_kill/等待/重试等容错语义。

发展史：定位为 @deepseek-ai/dsh-jobs 注册契约的进程本地方案。已知局限：任务随进程死亡，跨重启的持久化需独立后端实现同一 seam。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/jobs/jobs-local/README.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-jobs-local

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
