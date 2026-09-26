# dsh-experimental-tool-agent-team

- 包名: `@deepseek-ai/dsh-experimental-tool-agent-team`
- 分组: G13 实验特性
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/experimental/tool-agent-team`

## 实现逻辑
为 Agent Teams 在 member 的 Agent scope 内注册整套模型可见工具：spawn_teammate/send_message/list_agents/wait_agent/interrupt_agent 与 team_task_create/list/get/update（src/index.ts:164-391），并注册 `team:policy` systemPrompt 段（src/index.ts:169-173）。`apply()` 对已存在与后续 `agent/created` 的 Agent 用 `ctx.agentTeams.tryMembership` 幂等安装、`agent/disposed` 时卸载（src/index.ts:402-421）。wait_agent 在无 active peer 时短路返回 noProgress 以免空等（src/index.ts:252-274）。

## Provides
- Agent Teams 模型可见工具集 (spawn/list/send/wait/interrupt + 共享任务 CRUD)
- systemPrompt 段 team:policy

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 枚举/跟踪 Agent 并在其 scope 内注册工具
  - 证据: `src/index.ts:5 import type { Agent } + src/index.ts:14 inject 'agents' + src/index.ts:412 ctx.agents.list`
- `dsh-system-prompt` [运行时依赖] - 注入 Team 协作策略段落
  - 证据: `src/index.ts:14 inject ['agents','agentTeams','tools','systemPrompt'] + src/index.ts:169 systemPrompt.section`
- `dsh-tools` [E1+E2] - 注册模型可见工具并声明输出 schema
  - 证据: `src/index.ts:8-9 import defineTool/InferValue + src/index.ts:14 inject 'tools' + src/index.ts:175 tools.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
