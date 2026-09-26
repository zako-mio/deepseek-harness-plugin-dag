# dsh-schedule

- 包名: `@deepseek-ai/dsh-schedule`
- 分组: G31 定时调度
- 拓扑层: Layer 8
- 来源层: L2 web-app
- 源码路径: `packages/schedule/schedule`

## 实现逻辑
ScheduleService（ctx.schedule）以 storageDomain 持久化 Host 级提醒任务，暴露 create/list/catalog/history/delete/update（部分 @Remote）并派生四条 agent 作用域工具 schedule_create/list/delete/update（src/index.ts:100-460, src/tools.ts:408-551）。ScheduleRuntime 持有单个定时器，扫描到期任务、经 sessionController.resolveAgent 恢复会话、以 producer kind 'schedule' 投递提醒消息并在 ctx.sessions.flush 确认后推进或退休任务（src/runtime.ts:44-165）。storage.ts 用严格 zod schema 定义 tasks 表与投递历史（src/storage.ts:37-60），domain.ts 负责纯递归/一次性规则与视图，invariant.ts 校验 schedule/change 事件流（src/invariant.ts:19-54）。

## Provides
- ctx.schedule (Host 级持久化提醒/定时任务的创建、检索、修改、删除与到期投递)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 把工具注册绑定到根 agent 的作用域与会话
  - 证据: `src/tools.ts:7 import + src/index.ts:170 ctx.agents.roots`
- `dsh-api-session-controller` [E1+E2] - 在到期投递时恢复/激活目标会话
  - 证据: `src/index.ts:7 type import + src/runtime.ts:10 import + src/runtime.ts:101 ctx.sessionController.resolveAgent`
- `dsh-invariants` [E1+E2] - 注册 schedule/change 事件流的运行时不变式
  - 证据: `src/invariant.ts:8 import + src/invariant.ts:63 ctx.invariants.register`
- `dsh-llm` [编译依赖] - 构造 schedule 来源的用户消息并标记 MessageId 品牌
  - 证据: `src/runtime.ts:2-3 import + src/storage.ts:4 import`
- `dsh-session` [E1+E2] - 以会话作为投递目标并强制送达前持久化
  - 证据: `src/domain.ts:7-8 import + src/storage.ts:3 import + src/index.ts:96 ctx.sessions + src/runtime.ts:124 ctx.sessions.flush`
- `dsh-storage-domain` [E1+E2] - 把任务与投递历史持久化到 schedule 存储域
  - 证据: `src/index.ts:6 import + src/storage.ts:5 import + src/index.ts:126 ctx.storageDomain.open`
- `dsh-tools` [E1+E2] - 用 defineTool 向 agent 作用域注册四个 schedule 工具
  - 证据: `src/tools.ts:9-10 import + src/index.ts:101 static inject`
- `dsh-workspace` [编译依赖] - 以 SessionActivity 类型参与工作区归档准入与停止判定
  - 证据: `src/index.ts:9 type import + src/types.ts:11 import`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配 schedule 命名空间
- `dsh-client-ui-schedule` - 读/写/删 Host 日程任务与投递历史
- `dsh-client-ui-workspace` - 归档前检查会话是否有计划任务
