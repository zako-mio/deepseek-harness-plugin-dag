# dsh-goal-round-driver

- 包名: `@deepseek-ai/dsh-goal-round-driver`
- 分组: G17 目标与计划
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/goal/goal-round-driver`

## 实现逻辑
在 agent 生命周期内自动驱动同一会话的目标续轮：readyToDrive 要求精确 live agent、状态 idle 且无竞争提示（src/index.ts:103-114），drive 在轮次预算内用 renderGoalRoundPrompt 生成模型可见续轮消息并 agent.followup 投递（src/index.ts:164-204）。pre-step 瀑布监听器用 validReservation 校验排队提示仍属于当前 live 修订，否则 reject 并 restoreOtherClaimed 恢复他人已认领消息（src/index.ts:344-425）。目标变更/暂停会取消 live turn 或 disarm 并进入持久化检查点（src/index.ts:282-293, 117-124）。

## Provides
- goal 自动续轮驱动 (按目标 activation/轮次上限投递 followup 并在 pre-step 拒绝过期续轮)
- goal-round-driver-invariant 不变量伴随件 (校验续轮提示词与目标流一致)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 经 agent 生命周期/收件箱投递续轮消息并参与 pre-step 决策
  - 证据: `src/index.ts:9 import (Agent, PreStepDecision) + src/index.ts:98 ctx.agents.get + src/index.ts:192 agent.followup`
- `dsh-goal` [E1+E2] - 读取目标状态、disarm/block/pause 并在续轮消息上标注目标来源
  - 证据: `src/index.ts:10 import (GoalMessageSource/GoalRef/GoalView) + src/index.ts:19 inject ['agents','goals','sessions'] + src/index.ts:99 ctx.goals.get`
- `dsh-invariants` [E1+E2] - 注册续轮提示词不变量伴随件
  - 证据: `src/invariant.ts:6 import InvariantInstaller + src/invariant.ts:15 inject ['invariants'] + src/invariant.ts:85 ctx.invariants.register`
- `dsh-llm` [编译依赖] - 构造模型可见的续轮用户消息与提示块
  - 证据: `src/index.ts:11-12 import (createUserMessage, ContentBlock) + src/prompt.ts:3 import ContentBlock`
- `dsh-session` [E1+E2] - 会话持久化检查点与基于事件流的轮次状态跟踪
  - 证据: `src/index.ts:13 import (Session, SessionEvent) + src/index.ts:145 ctx.sessions.flush(agent.session) + src/index.ts:318 ctx.on('session/event')`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
