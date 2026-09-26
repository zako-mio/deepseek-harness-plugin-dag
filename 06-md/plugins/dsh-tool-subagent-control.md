# dsh-tool-subagent-control

- 包名: `@deepseek-ai/dsh-tool-subagent-control`
- 分组: G41 子代理
- 拓扑层: Layer 7
- 来源层: L1 核心集
- 源码路径: `packages/subagent/tool-subagent-control`

## 实现逻辑
注册 model 可见控制工具 send_message 与 interrupt_agent，二者是 ctx.subagents.sendMessage()/interrupt() 的薄适配层，不含自身的生命周期路由 (src/index.ts:27-111)。send_message 用 markAdjacentAgentSendMessageTool 标注标准工具身份并投递消息 (src/index.ts:28-72)；interrupt_agent 以 {kind:'ancestor',agent:caller} 授权中断 (src/index.ts:74-111)。list-agents.ts 另注册 list_agents，将 children/descendants 投影为模型可见行，省略一次性子项并保留诊断 (src/list-agents.ts:59-177)。

## Provides
- model 可见工具 `send_message` / `interrupt_agent` (子代理控制薄适配)
- model 可见工具 `list_agents` (子代理发现，children/descendants)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 读取活跃 Agent 状态用于发现结果
  - 证据: `src/list-agents.ts:12 (import type Agent) + src/list-agents.ts:20 (inject ['tools','subagents','agents']) + src/list-agents.ts:163 (ctx.agents)`
- `dsh-llm` [编译依赖] - 构造模型可见消息内容块
  - 证据: `src/index.ts:15 (import type ContentBlock)`
- `dsh-session` [编译依赖] - 子代理会话 id 类型
  - 证据: `src/index.ts:16 (import type SessionId) + src/list-agents.ts:13 (import type SessionId)`
- `dsh-subagent` [E1+E2] - 转发消息/中断并复用相邻 Agent 工具标记
  - 证据: `src/index.ts:17-18 (import 类型与 markAdjacentAgentSendMessageTool) + src/index.ts:21 (inject ['tools','subagents']) + src/index.ts:64 (ctx.subagents.sendMessage) + src/index.ts:108 (ctx.subagents.interrupt)`
- `dsh-tools` [E1+E2] - 注册控制与发现工具
  - 证据: `src/index.ts:14 (import defineTool) + src/index.ts:21 (inject ['tools','subagents']) + src/index.ts:28 (ctx.tools.register) + src/list-agents.ts:86 (ctx.tools.register)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
