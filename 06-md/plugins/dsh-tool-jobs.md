# dsh-tool-jobs

- 包名: `@deepseek-ai/dsh-tool-jobs`
- 分组: G22 作业调度
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/jobs/tool-jobs`

## 实现逻辑
在 ctx.jobs 之上注册模型可见的 job_output/job_list/job_kill 三个工具 (src/index.ts:310-414)，并在加载时 attachController('tool-jobs') 让生产者可启动作业 (src/index.ts:247)。订阅 jobs 事件把未被模型取回的完成通知注入忙碌 owner 的下一步、或唤醒空闲 owner（受 maxConsecutiveWakes 约束）(src/index.ts:271-308)。按 job 的 outputLimitBytes 截断 job_output/job_kill 的模型可见内容 (src/index.ts:225-244)，render.ts 负责把读取增量渲染为 stdout/stderr 分区与 [status] 行 (src/render.ts:75-84)。

## Provides

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 把完成通知投递到 owner Agent（inject/followup）并据其 input 重置唤醒预算
  - 证据: `src/index.ts:20 import type Agent + src/index.ts:212 ctx.on('agent/inbox/claimed')`
- `dsh-llm` [编译依赖] - 构造带来源标记的用户消息作为完成通知并做长度约束
  - 证据: `src/index.ts:13 import createUserMessage/boundContextSummary`
- `dsh-system-prompt` [运行时依赖] - 注入 tool:jobs 段系统提示，指导模型跟踪/收集后台作业
  - 证据: `src/index.ts:31 inject systemPrompt + src/index.ts:250 ctx.systemPrompt.section`
- `dsh-tools` [E1+E2] - 以上游工具定义注册三个作业控制工具并挂接 tools/pre-execute 拦截
  - 证据: `src/index.ts:16 import defineTool + src/index.ts:31 inject tools + src/index.ts:310 ctx.tools.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
