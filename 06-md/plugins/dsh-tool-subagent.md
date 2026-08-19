# dsh-tool-subagent

- 包名: `@deepseek-ai/dsh-tool-subagent`
- 分组: G19 子代理
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/subagent/tool-subagent`

## 为什么需要它（设计初衷）
给模型提供基于 ctx.subagents seam 的委派工具，解耦传输与执行约定：更换提供方（spawn/fork/acp 等）只改传输不改变执行约定。支持前台等待与后台运行（one-shot 经通用 Task 接口收集、continuable 返回持久化 subagentId），并发安全（同级委派可并行重叠执行、结果按模型顺序提交），并支持 persona、toolFilter、maxDepth 等每子 agent 独立配置。子 agent 在各自会话中工作，一次运行绝不变更父会话。RC7 修正 AggregateError 取消判定、更新后台作业文案。

发展史：位于 packages/subagent/tool-subagent，随 DeepSeek Harness monorepo 于 2026-08-10 首版 0.0.1-rc.1，0.1.0-rc.6（2026-08-13）转 MIT 并公开发布。核心设计源自多个 Agent Note：后台子任务（2026-07-08）、可继续对话（2026-07-28）、后台优先委派（2026-08-11）。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/subagent/tool-subagent/README.zh.md
- https://registry.npmjs.org/@deepseek-ai/dsh-tool-subagent

## 实现逻辑
模型可见的 subagent 委派工具：apply 通过 ctx.tools.register 注册(config.toolName ?? 'subagent')。工具 mount 随 provider 生命周期动态挂载/卸载(监听 subagent/provider-added|removed)；execute 区分前台、one-shot 后台(jobs.start)与 continuable 后台(ctx.subagents.startContinuable)。RC7：后台取消判定修正——signal.aborted 且错误非 AggregateError(提供方聚合启动/回滚失败)才归为 killed，聚合错误保持 failed；后台作业文案改 started background subagent job <jobId>。

## Provides
- 模型工具 'subagent'
- systemPrompt section tool:subagent
- 后台委派作业路由(dsh-jobs + continuable)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - exec.agent 委派 parent
  - 证据: `packages/subagent/tool-subagent/src/index.ts:14,370`
- `dsh-subagent` [编译依赖] - start/startContinuable/getProvider
  - 证据: `packages/subagent/tool-subagent/src/index.ts:17,23,425`
- `dsh-system-prompt` [编译依赖] - systemPrompt.section 注册指引
  - 证据: `packages/subagent/tool-subagent/src/index.ts:20,459`
- `dsh-tools` [编译依赖] - defineTool + register
  - 证据: `packages/subagent/tool-subagent/src/index.ts:13,297`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
