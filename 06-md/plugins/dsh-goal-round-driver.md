# dsh-goal-round-driver

- 包名: `@deepseek-ai/dsh-goal-round-driver`
- 分组: G17 目标计划
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/goal/goal-round-driver`

## 实现逻辑
apply() 安装 per-agent 竞态防护的自动续跑调度：监听 agent/created|disposed|session-start|status|error、goal/changed、agent/inbox/inserted|claimed|discarded、session/event。drive() 在 agent idle+armed+未达 maxGoalRounds 时渲染 round prompt 并经 agent.followup 排队；agent/pre-step 校验 reservation，失败则 block('prompt-rejected') 或 restore。

## Provides
- goal round 自动续跑调度
- agent/pre-step 续跑校验(reject)
- goal-round 消息源

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - agent 事件与 followup
  - 证据: `packages/goal/goal-round-driver/src/index.ts:9,106-107,192,215,435`
- `dsh-goal` [运行时依赖] - goal 状态读取与 block
  - 证据: `packages/goal/goal-round-driver/src/index.ts:10,99,167,269`
- `dsh-llm` [编译依赖] - createUserMessage
  - 证据: `packages/goal/goal-round-driver/src/index.ts:11,176`
- `dsh-session` [运行时依赖] - checkpoint 冲刷与 turn 边界
  - 证据: `packages/goal/goal-round-driver/src/index.ts:13,145,307`

## Dependents (下游被依赖)
- `dsh-agent-spine-demo` - 可选 ctx.plugin(goalSession) 同会话目标驱动
