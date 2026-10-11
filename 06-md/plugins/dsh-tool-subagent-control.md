# dsh-tool-subagent-control

- 包名: `@deepseek-ai/dsh-tool-subagent-control`
- 分组: G39 子代理
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/subagent/tool-subagent-control`

## 实现逻辑
提供全局命名的子代理控制工具，且自身不做生命周期路由：index.ts 注册 `send_message`（把调用 Agent 作为 sender 调 `ctx.subagents.sendMessage`，返回投递确认而非对方回答）与 `interrupt_agent`（以 `{ kind: 'ancestor', agent: caller }` 身份调 `ctx.subagents.interrupt`，不附加任何自有授权）(src/index.ts:27-111)。send_message 定义经 `markAdjacentAgentSendMessageTool` 标记，使相邻 Agent 投递语义可被内部识别 (src/index.ts:18、src/index.ts:28)。list-agents.ts 是独立可加载的第二个插件入口，注册 `list_agents`，按 scope 分派到 `listChildren` 或 `listDescendants`，把服务行投影为 child/diagnostic 两类条目并过滤不可续跑的一次性子代理 (src/list-agents.ts:19-20、src/list-agents.ts:152-176)。

## Provides
- ctx.tools 上的 `send_message` 工具（向直接父/直接可续跑子代理投递消息）
- ctx.tools 上的 `interrupt_agent` 工具（按祖先权限请求停止子代理当前工作）
- ctx.tools 上的 `list_agents` 工具（独立入口 `tool-subagent-control/list-agents`，列出子代理及诊断行）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 读取活跃 Agent 状态以区分 running/inactive
  - 证据: `src/list-agents.ts:12 import type { Agent } + src/list-agents.ts:55 statusOf(agents, id)`
- `dsh-llm` [编译依赖] - 构造要投递的消息内容
  - 证据: `src/index.ts:15 import type { ContentBlock } + src/index.ts:63 构造消息内容块`
- `dsh-session` [编译依赖] - 目标地址与会话身份类型
  - 证据: `src/index.ts:16 import type { SessionId } + src/index.ts:66 brandString<SessionId>`
- `dsh-subagent` [E1+E2] - 驻留、冷恢复与中断授权全部由子代理服务承担
  - 证据: `src/index.ts:17-18 import type {}/internal + src/index.ts:21 inject 'subagents' + src/index.ts:64 sendMessage / :108 interrupt`
- `dsh-tools` [E1+E2] - 三个模型可见工具都要注册进工具注册表
  - 证据: `src/index.ts:14 import defineTool + src/index.ts:21 inject 'tools' + src/index.ts:28/74/86 ctx.tools.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
