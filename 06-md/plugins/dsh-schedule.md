# dsh-schedule

- 包名: `@deepseek-ai/dsh-schedule`
- 分组: G30 外部执行后端
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/schedule/schedule`

## 为什么需要它（设计初衷）
会话本地提醒：持久状态存于原会话日志，进程内计时器只在会话有活根 Agent 时等待，到期工作经普通后续队列进同一对话。

来源：
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/schedule
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/schedule.md

## 实现逻辑
inject ['agents','sessions','tools','sessionPersistence'] (src/index.ts:35)；apply 订阅 agent/created (:45)，仅对 root agents 创建 ScheduleRuntime (:47) 并注册 schedule_create/list/delete 工具 (:49，tools.ts:318/400/420)，监听 agent/status idle→runtime.requestDrive (:50-54)；基于 session event log 的 durable after/at/fixed-rate 提醒，持久化经 sessionPersistence seam。

## Provides
- tools: schedule_create/schedule_list/schedule_delete
- 每 root agent 的 ScheduleRuntime 实例

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - root agent 生命周期与 owner 作用域
  - 证据: `package.json:35 peerDep + src/index.ts:7 import type Agent；E2: :45 ctx.on('agent/created')、:46 ctx.agents.roots()、:47 new ScheduleRuntime(ctx, agent)`
- `dsh-llm` [编译依赖] - 提醒渲染类型
  - 证据: `package.json:38 peerDep`
- `dsh-session` [E1+E2] - session 事件日志（提醒持久化载体）
  - 证据: `package.json:39 peerDep + src/index.ts:8 import type Session/SessionEvent；E2: :51 agent.session.events 读 schedule/change 事件`
- `dsh-tools` [E1+E2] - 工具注册
  - 证据: `package.json:41 peerDep + src/tools.ts:9 import defineTool；E2: src/index.ts:49 registerScheduleTools(ctx,...)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
