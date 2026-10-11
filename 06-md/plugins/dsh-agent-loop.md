# dsh-agent-loop

- 包名: `@deepseek-ai/dsh-agent-loop`
- 分组: G09 核心运行时
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/core/agent-loop`

## 实现逻辑
以 AgentLoop 服务实现 AgentFactory 与具体驱动。构造期注册 turnBoundary 与 inbox 两个会话投影、把自身登记为 agents 工厂、注册 provider/model 提示变量，并按配置启动/恢复声明式 agent（src/index.ts:377-390、src/index.ts:392-421）。createAgent/resume 走 prepare→setupAndPublish 的可回滚事务：先取会话写入句柄，再在未发布状态运行 setup 与其同步 commit，最后 enter+announce 两个注册表，逆序 teardown 收敛到 quiescence（src/index.ts:497-676、src/index.ts:750-816）。ReactLoopAgent 驱动 turn/step 边界：preStep 组装系统提示并跑 agent/pre-step 瀑布（src/agent.ts:267-288），step 内渲染提示、投影 runtime-context、流式消费 assistant 输出并在失败时走 agent/request-error（src/agent.ts:400-561）；工具调用交给 executeToolCalls 按 executionMode 做串行屏障或有界并行池调度，结果始终按模型顺序提交（src/tool-calls.ts:60-102、src/tool-calls.ts:122-247）。

## Provides
- ctx.agentLoop（具体 agent 驱动与 AgentFactory 实现，src/index.ts:341-342、src/index.ts:365-366）
- sessionProjections 'turnBoundary' 与 'inbox' 投影定义（src/index.ts:57-95、src/inbox.ts:27-65）
- agent-loop/config-start-failed 事件（声明式 agent 启动失败上报，src/index.ts:239-250）
- 可配置 agent 身份注入键 CONFIGURED_AGENT_IDENTITIES_KEY 与 DEFAULT_MAX_PARALLEL_TOOL_CALLS（src/index.ts:277、src/constants.ts:6）
- 工具调用调度器 executeToolCalls 与 durable inbox 实现 ReactLoopInbox（src/tool-calls.ts:60、src/inbox.ts:74）
- 运行时上下文投影 SystemPromptProjection/RuntimeContextProjection 与 assistant 流式帧累积器（src/runtime-context.ts:65、src/runtime-context.ts:114、src/assistant-stream.ts:18）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 实现 AgentFactory 并向 agents 注册表登记，同时复用其 agent 事件与 inbox 契约驱动生命周期
  - 证据: `src/index.ts:14 import type { Agent, AgentFactory, AgentHandle } from '@deepseek-ai/dsh-agent' + src/index.ts:388 ctx.effect(() => ctx.agents.setFactory(this), ...)`
- `dsh-llm` [E1+E2] - 调用模型流式接口、构造 assistant/tool-result 消息并复用 LlmError 与失败分类
  - 证据: `src/agent.ts:19 import type { GenerateOptions, LlmCallConfig } + src/agent.ts:453 this.loopCtx.llm.stream(request)`
- `dsh-session` [E1+E2] - 创建/准备/进入会话、追加 turn/step/assistant/tool 事件，并对中断 turn 做语义修复
  - 证据: `src/index.ts:26 import { interruptedTurnClosers, SessionPreparation, SessionSeq } + src/index.ts:689 SessionPreparation.create(this.runtime.ctx.sessions.prepare(id, { meta }))`
- `dsh-session-projection` [E1+E2] - 注册 turnBoundary 与 inbox 投影，使步边界与待处理输入可从会话日志重放
  - 证据: `src/index.ts:31 import type { ProjectionDefinition } + src/index.ts:378 ctx.sessionProjections.register(turnBoundaryProjectionDefinition)`
- `dsh-system-prompt` [E1+E2] - 组装每步系统提示与运行时上下文快照，并注册 provider/model 提示变量
  - 证据: `src/agent.ts:32 import { joinContextSections, renderContextSections, renderPrompt } + src/index.ts:389 ctx.systemPrompt.variable('provider', context => context.agent?.options.provider)`
- `dsh-tools` [E1+E2] - 经内部调度器符号准备/派发/收尾工具调用，并按 executionMode 决定串行或并行
  - 证据: `src/tool-calls.ts:17 import { TOOL_RUNTIME_SCHEDULER, ... } from '@deepseek-ai/dsh-tools' + src/tool-calls.ts:170 await ctx.tools[TOOL_RUNTIME_SCHEDULER].prepare(call.exec)`

## Dependents (下游被依赖)
- `dsh-session-title` - 读 turnBoundary 判断主请求是否已开始本回合
