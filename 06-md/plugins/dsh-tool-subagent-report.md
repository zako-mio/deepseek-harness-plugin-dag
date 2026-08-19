# dsh-tool-subagent-report

- 包名: `@deepseek-ai/dsh-tool-subagent-report`
- 分组: G19 子代理
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/subagent/tool-subagent-report`

## 为什么需要它（设计初衷）
面向子 agent 的 report 工具，基于 ctx.subagents 可继续会话提供子作用域报告通道，支撑后台可继续子 agent 的结算/汇报。

发展史：RC8 reportDelivery 语义变更 wakeup→next-step(更及时唤醒父任务)

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-tool-subagent-report
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/subagent/tool-subagent-report/README.zh.md

## 实现逻辑
index.ts:29-37 reportDelivery 取值由 'quiet'/'wakeup' 改为 'quiet'/'next-step'(默认next-step): 'next-step' 在最近步骤边界唤醒父代理并注入上下文，比旧wakeup更及时地让父任务在步骤边界继续。

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
