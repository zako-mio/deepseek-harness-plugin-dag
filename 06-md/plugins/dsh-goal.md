# dsh-goal

- 包名: `@deepseek-ai/dsh-goal`
- 分组: G17 目标计划
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/goal/goal`

## 为什么需要它（设计初衷）
解决 agent 长任务执行缺乏「持久目标状态」的问题：在既有会话内维护一个事件溯源的当前目标（含 phase/revision/续行权限），提供 create/edit/pause/resume/complete/block/clear 等动词。其核心价值是让长期目标在会话恢复/fork 后仍保真，同时把目标与继续执行权限分离、绝不持久化续行状态，为 goal-round-driver 等策略层提供可靠状态底座。

发展史：来自 packages/goal/goal，伴随 goal 领域（2026-07-19 同会话目标领域 Agent Note）从简单状态演进为事件溯源+严格回放校验的服务，与 tool-goal、goal-round-driver 构成目标子系统三件套。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/goal/goal/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/implemented/feature/2026-07-19-persisted-same-session-goal-domain.md

## 实现逻辑
事件溯源 goal 域(ctx.goals GoalService，extends TypertRemoteService)。所有变更 append 'goal/change' 事件，per-session 缓存经 fold.ts 增量同步，compare-and-set ref 校验防 stale。create/edit/pause/resume/complete/block/clear 提交后经 agentEvents 发 'goal/changed'；'agent/session-start' 重置 activation=disarmed；注册 'goal' 投影单元；@Remote 导出。

## Provides
- ctx.goals(GoalService)
- session 事件 goal/change
- goal/changed agent-scoped emit
- goal session projection
- @Remote API

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - agent 身份与 goal/changed
  - 证据: `packages/goal/goal/src/index.ts:12,198,415,557`
- `dsh-session` [运行时依赖] - goal/change 持久化
  - 证据: `packages/goal/goal/src/index.ts:546`
- `dsh-session-projection` [组合依赖] - goal 投影单元
  - 证据: `packages/goal/goal/src/index.ts:204`

## Dependents (下游被依赖)
- `dsh-agent-spine-demo` - 可选 ctx.plugin(GoalService) 持久化目标域
- `dsh-client-ui-conversation` - goal 投影 key 类型合并（hasGoal 开关）
- `dsh-client-ui-goal` - goal 投影 key 类型与 GoalRef 契约
- `dsh-command-goal` - goal 域状态读写
- `dsh-goal-round-driver` - goal 状态读取与 block
- `dsh-host-apiproxy` - GoalError/GoalRef（goals 域）
- `dsh-tool-goal` - goal 域读写
