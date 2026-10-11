# dsh-goal-round-driver

- 包名: `@deepseek-ai/dsh-goal-round-driver`
- 分组: G17 目标与计划
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/goal/goal-round-driver`

## 实现逻辑
实现同会话目标轮次的自动续跑驱动：apply 为每个 Agent 维护串行化的 DriverState，在 agent/status 变 idle、goal/changed、inbox 插入/认领/丢弃、session/event 等触发点收敛到一次 requestDrive，再由 drive 在真正静默时用 renderGoalRoundPrompt 生成带 goal 来源标记的用户消息并 agent.followup 入队 (src/index.ts:138-205, src/index.ts:286-346)。轮次进入模型步之前经 agent/pre-step 复核 validReservation（阶段、ref、round 三者必须与实时目标严格一致），不通过即 reject 并把被误配的下一轮消息恢复回队列 (src/index.ts:348-429)。达到 maxGoalRounds 或入队失败时调用 ctx.goals.block 记录 round-limit / queue-failed 原因 (src/index.ts:166-171, src/index.ts:196-203)。

## Provides

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 在 Agent 生命周期与 inbox 事件上调度轮次，并在 pre-step 处做准入裁决
  - 证据: `src/index.ts:9 import type Agent / PreStepDecision + src/index.ts:215 ctx.agents.withoutInitiator + src/index.ts:246 ctx.on('agent/error')`
- `dsh-goal` [E1+E2] - 读取当前目标、写入 blocker、撤销 activation，并复用目标消息来源词汇
  - 证据: `src/index.ts:10 import type GoalMessageSource / GoalRef / GoalView + src/index.ts:19 static inject ['agents','goals','sessions'] + src/index.ts:99 ctx.goals.get(state.agent)`
- `dsh-llm` [编译依赖] - 构造并渲染模型可见的目标轮次提示与用户消息
  - 证据: `src/index.ts:11-12 import createUserMessage + type ContentBlock / MessageId / MessageSource + src/prompt.ts:3`
- `dsh-session` [E1+E2] - 在持久化检查点之后再续跑，并从会话事件判定轮次是否已进入历史
  - 证据: `src/index.ts:13 import type Session / SessionEvent / UserMessage + src/index.ts:145 ctx.sessions.flush + src/index.ts:322 ctx.on('session/event')`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
