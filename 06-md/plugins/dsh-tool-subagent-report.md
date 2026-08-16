# dsh-tool-subagent-report

- 包名: `@deepseek-ai/dsh-tool-subagent-report`
- 分组: G19 子代理
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/subagent/tool-subagent-report`

## 实现逻辑
子作用域 report 工具：apply 通过 ctx.subagents.registerContinuableSetup(childCtx => installReportTool(childCtx, ctx, reportDelivery)) 将 report 工具与 prompt 指引装入每个可续聊子代理的未发布 childCtx。installReportTool 注册 childCtx.tools 的 'report' 工具(调 ctx.subagents.reportFrom)，仅对 continuable in-process 子代理可见。

## Provides
- 子代理作用域模型工具 'report'
- 子代理 systemPrompt section tool:report
- 父调度策略 reportDelivery: quiet|wakeup

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - exec.agent 报告发送方
  - 证据: `packages/subagent/tool-subagent-report/src/index.ts:11,98`
- `dsh-subagent` [编译依赖] - registerContinuableSetup + reportFrom
  - 证据: `packages/subagent/tool-subagent-report/src/index.ts:21,140`
- `dsh-system-prompt` [编译依赖] - childCtx.systemPrompt.section
  - 证据: `packages/subagent/tool-subagent-report/src/index.ts:14,54`
- `dsh-tools` [编译依赖] - childCtx.tools.register
  - 证据: `packages/subagent/tool-subagent-report/src/index.ts:15,65`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
