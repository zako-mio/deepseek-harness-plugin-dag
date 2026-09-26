# dsh-api-job-controller

- 包名: `@deepseek-ai/dsh-api-job-controller`
- 分组: G02 API 网关与控制器
- 拓扑层: Layer 4
- 来源层: L2 web-app
- 源码路径: `packages/api/job-controller`

## 实现逻辑
JobController 继承 TypertRemoteService，以 namespace 'job' 注册并注入 jobs/typert (src/index.ts:43-65)。list 与 follow 两个 stream 方法分别委托 streamJobRows / observeJobOutput，把 ctx.jobs 的可见任务集合与单个任务的保留输出投影成帧 (src/index.ts:75-96)。两个生成器都在首次读取前订阅 registry.events，先产出 opened/rows 基线，之后在唤醒后按 flushMs 合并突发；输出按 maxFrameBytes 软预算切分，任务到终态或收到 removed 时产出 status 后收尾 (src/observe.ts:41-93, src/rows.ts:26-52)。kill 先以 sessionId 做所有权查询再同步调用 jobs.kill，未知/越权统一映射为 job/not-found (src/index.ts:109-127)。

## Provides
- ctx.remote.job（job 命名空间流式 Remote：list 任务名单、follow 单任务输出与终态、kill 人工终止）
- jobController（Host 侧后台任务观测服务，含 observeFlushMs / observeMaxFrameBytes 配置）

## Depends On (上游依赖)
- `dsh-api-gateway` [编译依赖] - 客户端 Remote 载体
  - 证据: `src/client/service.ts:11 import + src/client/model.ts:5 import`
- `dsh-session` [编译依赖] - 客户端会话身份类型
  - 证据: `src/client/model.ts:12 import type SessionId`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配 job 命名空间
- `dsh-client-ui-jobs` - 作业注册表、观察流与 kill 的客户端服务
