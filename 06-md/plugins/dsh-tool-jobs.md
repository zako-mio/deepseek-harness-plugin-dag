# dsh-tool-jobs

- 包名: `@deepseek-ai/dsh-tool-jobs`
- 分组: G16 作业
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/jobs/tool-jobs`

## 为什么需要它（设计初衷）
给模型提供后台任务控制工具（job_output/job_list/job_kill），管理 ctx.jobs 注册表中的通用后台任务。

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-tool-jobs
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/jobs/tool-jobs/README.zh.md

## 实现逻辑
apply() 注册 job_output/job_list/job_kill 三个模型工具：attachController('tool-jobs') 使 producers 可 start；onJobDone 把未报告完成以 notice 注入 busy owner 或 followup 唤醒 idle owner(wakeup 默认，maxConsecutiveWakes 限界)；tools/pre-execute 捕获 outputLimitBytes；systemPrompt.section 给模型指导；agent/inbox/claimed 用户输入重置 wake 预算。

## Provides
- ctx.tools: job_output/job_list/job_kill
- jobs controller attachment('tool-jobs')
- completion notice 注入/唤醒
- systemPrompt section tool:jobs
- tools/pre-execute 输出限制监听

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - completion 通知投递
  - 证据: `packages/jobs/tool-jobs/src/index.ts:19,294-299`
- `dsh-jobs-local` [组合依赖] - controller 注册落地
  - 证据: `packages/jobs/tool-jobs/src/index.ts:260`
- `dsh-system-prompt` [组合依赖] - 模型跨调用指导
  - 证据: `packages/jobs/tool-jobs/src/index.ts:263`
- `dsh-tools` [组合依赖] - 工具注册与执行管道
  - 证据: `packages/jobs/tool-jobs/src/index.ts:14,233,302`

## Dependents (下游被依赖)
- `dsh-agent-spine-demo` - 可选 ctx.plugin(toolJobs) 模型面任务工具
