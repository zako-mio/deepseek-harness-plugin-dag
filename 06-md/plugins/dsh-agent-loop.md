# dsh-agent-loop

- 包名: `@deepseek-ai/dsh-agent-loop`
- 分组: G09 核心运行时
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/core/agent-loop`

## 实现逻辑
具体 agent 循环插件：`AgentLoop`（服务名 `agentLoop`）继承 Service 并实现 `AgentFactory`，构造时加载 declarative agents、注册 turnBoundary 与 inbox 两个会话投影、把自身注册为 `ctx.agents` 工厂，并注册 provider/model/cwd 三个 system-prompt 变量 (src/index.ts:330-404)。`create/createAgent/resume/resumeWith` 经 `SessionPreparation` 与持久化写句柄在单一事务内构造 session 与 `ReactLoopAgent`，`prepare()` 建立 memo 化反向拆卸，setup 后 `publish()` 进入两个注册表并 announce (src/index.ts:479-640,714-780,807-890)。`ReactLoopAgent` 以 Phase 状态机驱动 turn/step 边界，所有请求由会话日志派生 (src/agent.ts:98-160)；inbox.ts 提供 inbox 投影与命令门面 (src/inbox.ts:27-74)；tool-calls.ts/assistant-stream.ts/runtime-context.ts 处理工具调用调度、流式发布与运行时上下文投影；invariant.ts 校验 loop 构造的 llm 请求可从会话日志重建 (src/invariant.ts:19-57)。

## Provides
- ctx.agentLoop (具体 Agent 工厂与驱动器服务，实现 AgentFactory)
- turnBoundary 会话投影定义
- inbox 会话投影定义
- agent-loop/config-start-failed 事件
- ReactLoopAgent/ReactLoopInbox 驱动实现与 DEFAULT_MAX_PARALLEL_TOOL_CALLS

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 实现 AgentFactory 并经 ctx.agents 工厂/注册表发布与登记 agent
  - 证据: `src/agent.ts:18 import + src/index.ts:24 + src/index.ts:331 inject(['agents'])`
- `dsh-invariants` [E1+E2] - 注册 loop 请求可重建性不变量
  - 证据: `src/invariant.ts:8 import + src/invariant.ts:16 inject(['invariants']) + src/invariant.ts:65 register`
- `dsh-llm` [E1+E2] - 构造并执行模型请求，复用 LlmCallConfig/PreparedLlmCall 等
  - 证据: `src/agent.ts:19 import + src/index.ts:25 + src/index.ts:331 inject(['llm'])`
- `dsh-scope` [E1+E2] - 为每个 agent 铸造作用域上下文
  - 证据: `src/agent.ts:28-29 import createScope + src/agent.ts:130 createScope(loopCtx, this)`
- `dsh-session` [E1+E2] - 创建/恢复会话并把 agent 会话登记进 SessionStore
  - 证据: `src/index.ts:26-27 import + src/index.ts:331 inject(['sessions']) + src/index.ts:618-622 ctx.sessions.enter/announce`
- `dsh-session-projection` [E1+E2] - 注册 turnBoundary 与 inbox 投影定义
  - 证据: `src/index.ts:30-31 import + src/index.ts:364-365 ctx.sessionProjections.register + src/index.ts:331 inject(['sessionProjections'])`
- `dsh-system-prompt` [E1+E2] - 注册 provider/model/cwd 提示变量并驱动提示装配
  - 证据: `src/agent.ts:32-33 import + src/index.ts:370-372 ctx.systemPrompt.variable + src/index.ts:331 inject(['systemPrompt'])`
- `dsh-tools` [E1+E2] - 调度工具调用执行流水线
  - 证据: `src/index.ts:29 import + src/tool-calls.ts:17 + src/index.ts:331 inject(['tools'])`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
