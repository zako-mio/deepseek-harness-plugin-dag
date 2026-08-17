# dsh-agent

- 包名: `@deepseek-ai/dsh-agent`
- 分组: G03 核心服务
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/core/agent`

## 为什么需要它（设计初衷）
定义 Agent 接口、实时注册表、发起方(initiator)作用域与 agent/* 事件词汇，是产品 API 脊柱。所有插件（UI、钩子、编排器）面向此 Agent handle 编程而不依赖具体循环，因此循环(agent-loop)可整体替换，从根本上落实『一切皆插件』。

发展史：位于 packages/core/agent，随 2026-08-10 首批 rc 发布（BSD-3-Clause），后转 MIT，0.1.0-rc.6 转公开。保持稳定 API，注册表可复用稳定路由载体，为 dsh-agent-loop 等循环实现提供替换缝隙。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/core/agent/README.zh.md
- https://registry.npmjs.org/@deepseek-ai/dsh-agent
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md

## 实现逻辑
Agent 服务(ctx.agents)：live 注册表 + initiator scope(AsyncLocalStorage 因果归属) + 工厂委派。AgentRegistry 只跟踪/生命周期管理，具体 create/resume 由 dsh-agent-loop 实现 AgentFactory 通过 setFactory 注入。提供 agentEvents/emitAgentEvent 事件派发(agent/created、agent/disposed、agent/status、agent/request、agent/request-error 等主题事件词表)；model-selection.ts 将模型选择耦合到 system-prompt/assemble 与 agent/request 瀑布。

## Provides
- ctx.agents(AgentRegistry)
- ctx.agent(DX accessor)
- agent/created|disposed|status 事件
- agent/inbox/* 事件
- agent/session-start|pre-step|request|request-error|turn-stopping|error 事件词表
- AgentFactory 接口(由 agent-loop 实现)
- Inbox 类
- typert lookups: agent
- ModelSelection/installModelSelection

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - LlmCallConfig/ReasoningEffortId 类型
  - 证据: `packages/core/agent/package.json:41, packages/core/agent/src/model-selection.ts:7`
- `dsh-session` [运行时依赖] - Agent 以 SessionId 为 id
  - 证据: `packages/core/agent/src/index.ts:14, 268-280`
- `dsh-system-prompt` [运行时依赖] - 监听 system-prompt/assemble 注入模型变量
  - 证据: `packages/core/agent/src/model-selection.ts:40-53`
- `dsh-typert-registry` [运行时依赖] - ctx.inject(['typert']) 注册 agent 查找器
  - 证据: `packages/core/agent/src/index.ts:268-281`

## Dependents (下游被依赖)
- `dsh-agent-default-model` - ModelSelection 类型
- `dsh-agent-instructions` - 订阅 agent/pre-step waterfall
- `dsh-agent-loop` - static inject agents + setFactory
- `dsh-agent-presets` - Context merge（agent/created 事件）
- `dsh-agent-spine-demo` - ctx.plugin(AgentRegistry) agent 注册表
- `dsh-api-remotes` - Agent 类型与 ctx.agents.get/resume/isOwnedBy 服务（:70-71,128,162）
- `dsh-client-ui-conversation` - inbox/agent 事件类型契约（agent/inbox/spliced）
- `dsh-client-ui-trajectory` - agent/inbox/spliced 等事件类型
- `dsh-commands` - 命令执行目标 agent
- `dsh-compaction-basic` - 订阅 agent/pre-step|request-error|status
- `dsh-cordis-host-runner` - Agent 类型（会话所有权）
- `dsh-goal` - agent 身份与 goal/changed
- `dsh-goal-round-driver` - agent 事件与 followup
- `dsh-hooks-claude-code` - agent 类型与 pre-step 决策契约
- `dsh-hooks-codex` - agent 类型与决策契约
- `dsh-host-apiproxy` - installModelSelection/Agent 类型，模型切换实现
- `dsh-jobs-local` - job owner 生命周期
- `dsh-llm-retry` - inject ['agents']；订阅 agent/request-error
- `dsh-repeat-tool-reminder` - 监听 agent/pre-step
- `dsh-sandbox-policy` - 类型依赖
- `dsh-schedule` - root agent 生命周期与 owner 作用域
- `dsh-sdk-jsonrpc-server` - inject ['agents'] + Agent/AgentHandle 类型与 ctx.agents 工厂
- `dsh-session-checkpoint-policy` - PreStepDecision 类型
- `dsh-session-reference` - 目标 agent 身份与工作目录（cwd 亲和排序/排除自身）
- `dsh-subagent` - ctx.inject(['agents']) 建立 ContinuationManager
- `dsh-subagent-fork-in-process` - Agent 类型与 parent.session.header
- `dsh-subagent-spawn-in-process` - 子代理经 ctx.agents 工厂创建
- `dsh-terminal-bash` - owner 隔离与 agent 事件上下文
- `dsh-time-context` - agent/pre-step 事件词表与 PreStepDecision 注入契约
- `dsh-tmux-context` - agent/pre-step 事件词表与 PreStepDecision 注入契约
- `dsh-tool-ask-user` - agent 上下文透传
- `dsh-tool-bash` - Agent 类型与 job owner
- `dsh-tool-bash-persistent` - owner 隔离与 shell 生命周期
- `dsh-tool-cordis` - agent 类型与 pre-step 决策
- `dsh-tool-goal` - 调用者认证
- `dsh-tool-jobs` - completion 通知投递
- `dsh-tool-skill` - pre-step 注入钩子
- `dsh-tool-subagent` - exec.agent 委派 parent
- `dsh-tool-subagent-control` - list_agents inject agents
- `dsh-tool-subagent-report` - exec.agent 报告发送方
- `dsh-tool-terminal` - owner 隔离与 agent 上下文
- `dsh-tool-todo` - owning session 归属
- `dsh-tools` - ToolExecutionInput.agent 关联调用归属
- `dsh-user-approval` - 携带 live agent 路由 answerer
- `dsh-user-questions` - 调用者身份边界
- `dsh-web-search-deepseek` - currentInitiator 归属
- `dsh-workflow-worker-thread` - request.parent Agent
