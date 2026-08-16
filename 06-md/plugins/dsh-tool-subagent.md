# dsh-tool-subagent

- 包名: `@deepseek-ai/dsh-tool-subagent`
- 分组: G19 子代理
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/subagent/tool-subagent`

## 实现逻辑
模型可见的 subagent 委派工具：apply 通过 ctx.tools.register 注册(config.toolName ?? 'subagent')。工具 mount 随 provider 生命周期动态挂载/卸载(监听 subagent/provider-added|removed)；execute 区分前台、one-shot 后台(jobs.start)与 continuable 后台(ctx.subagents.startContinuable)。

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
