# dsh-tool-subagent-control

- 包名: `@deepseek-ai/dsh-tool-subagent-control`
- 分组: G19 子代理
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/subagent/tool-subagent-control`

## 实现逻辑
全局命名控制工具：apply 注册 send_message(ctx.subagents.followup 转发)与 interrupt_agent(ctx.subagents.interrupt 转发)；list-agents 子入口注册 list_agents(listChildren/listDescendants + agents 实时状态)。工具名全局唯一。

## Provides
- 模型工具 send_message/interrupt_agent
- 可独立加载的 list_agents

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - list_agents inject agents
  - 证据: `packages/subagent/tool-subagent-control/src/list-agents.ts:18,60`
- `dsh-llm` [编译依赖] - assertNever
  - 证据: `packages/subagent/tool-subagent-control/src/list-agents.ts:14`
- `dsh-session` [编译依赖] - SessionId 品牌化入参
  - 证据: `packages/subagent/tool-subagent-control/src/index.ts:15,68`
- `dsh-subagent` [编译依赖] - followup/interrupt
  - 证据: `packages/subagent/tool-subagent-control/src/index.ts:19,66`
- `dsh-tools` [编译依赖] - defineTool + register
  - 证据: `packages/subagent/tool-subagent-control/src/index.ts:13,26`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
