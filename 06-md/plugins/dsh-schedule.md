# dsh-schedule

- 包名: `@deepseek-ai/dsh-schedule`
- 分组: G29 定时调度
- 拓扑层: Layer 8
- 来源层: L2 web-app
- 源码路径: `packages/schedule/schedule`

## 实现逻辑
以 default 导出的 ScheduleService（extends TypertRemoteService，注册为 ctx.schedule，static inject=['agents','sessions','storageDomain','sessionController','sessionPersistence']）把提醒做成 Host 级持久化任务：构造期打开 schedule storage domain（严格 schema，键与 record.id 不一致即拒绝打开），建立 ScheduleRuntime，并把 create/list/catalog/delete/update/history 全部串进一条 FIFO 队列以串行化管理与投递 (src/index.ts:99-165、src/storage.ts:37-60)。规则与时间算术集中在 domain.ts：六种规则（after/at/every/daily/weekly/cron）各自校验并算出唯一 UTC 目标，日历规则用 Temporal 以「gap 跳过、overlap 取较早」解析，cron 按 Vixie 的 DOM_STAR/DOW_STAR 语义匹配并做 400 年搜索地平线 (src/domain.ts:791-823、src/domain.ts:909-955、src/domain.ts:969-983、src/domain.ts:1049-1113)。runtime.ts 用单个 timer 扫描到期任务，经 sessionController.resolveAgent 恢复原会话、以 followup 投递、等 sessions.flush 确认后才把状态/目标/回执写回，失败只记录不自动重试 (src/runtime.ts:85-165)。归档准入经 workspace 事件读取存储行：会话仍有活跃提醒则拒绝归档，归档停止则删除这些行 (src/index.ts:188-206、src/index.ts:430-461)。

## Provides
- ctx.schedule (ScheduleService：Host 级持久化提醒的创建/列举/目录/删除/更新/投递历史，读取与删除都不激活会话)
- Typert Remote 方法 list/catalog/history/delete/update (浏览器与 Agent 共用同一服务)
- storage domain 'schedule' v1 的 tasks 表 (scheduleTaskSchema 严格校验并拒绝打开损坏域)
- 规则与视图出口 scheduleView/renderReminderFraming/renderRecurringReminderBatchFraming (模型可见提醒文本的稳定框架)
- 事件 'schedule/changed' (持久化任务集变更通知，供客户端重取目录)
- session 事件 'schedule/change' v1 与 LegacyScheduleRecord 词表 (历史提醒保持可读，不隐式迁移)
- workspace 归档准入族 SessionActivityKindMap['schedule'] (有活跃提醒的会话拒绝归档)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 按会话查活跃 Agent 以判定委派深度，决定是否拒绝绑定
  - 证据: `package.json:49 peerDep + packages/schedule/schedule/tsconfig.json:30 项目引用；src/index.ts:411 ctx.agents.get(sessionId)`
- `dsh-api-session-controller` [E1+E2] - 到期时经既有控制器恢复原会话的 Agent，保证 preset 组合与并发激活只有一个所有者
  - 证据: `package.json:50 peerDep + src/runtime.ts:10 type import；src/index.ts:100 inject 'sessionController'、src/runtime.ts:101 ctx.sessionController.resolveAgent(sessionId)`
- `dsh-llm` [E1+E2] - 以 schedule 来源构造投递消息，并用 MessageId 记录投递回执身份
  - 证据: `package.json:52 peerDep + src/runtime.ts:2 import createUserMessage、src/runtime.ts:3 type import ContextFormed、src/storage.ts:4 import MessageId、src/types.ts:7 type import；src/runtime.ts:119 createUserMessage、src/runtime.ts:4-8 declare module MessageSourceMap`
- `dsh-session` [E1+E2] - 以 SessionId 绑定任务原始会话，并在会话创建时读取历史 schedule 事件给出告警
  - 证据: `package.json:53 peerDep + src/index.ts:8 type import SessionId、src/storage.ts:3 import SessionId、src/types.ts:6 与 src/types.ts:9 type import、src/domain.ts:7 import SessionLogOffset；src/index.ts:166 ctx.on('session/created')、src/index.ts:173 session.ownEvents()`
- `dsh-session-projection` [运行时依赖] - 切换 preset 前用 turnBoundary 投影判定会话是否已开始首轮
  - 证据: `package.json:55 peerDep + src/index.ts:349 this.owner.sessionProjections.stateOf(agent.session,'turnBoundary')`
- `dsh-storage-domain` [E1+E2] - 以 schema 校验的 domain/table 持久化任务，损坏即拒绝打开
  - 证据: `package.json:56 peerDep + src/index.ts:6 type import Domain、src/storage.ts:5 import defineDomain/domainTable；src/index.ts:100 inject 'storageDomain'、src/index.ts:125 ctx.storageDomain.open(scheduleDomain)`
- `dsh-subagent` [编译依赖] - 拒绝把提醒绑定到委派子会话（投递永远到不了），与委派深度上限共用同一记账
  - 证据: `package.json:57 peerDep + src/index.ts:7 import delegationDepthOf；src/index.ts:412 delegationDepthOf(agent) === 0`
- `dsh-tools` [编译依赖] - 编译期契约对齐：提醒工具的 schema/错误码词汇与本包导出的类型共用同一基线；仅声明式依赖
  - 证据: `package.json:58 peerDep + packages/schedule/schedule/tsconfig.json:33 项目引用（源码无直接 import）`
- `dsh-workspace` [E1+E2] - 参与工作区归档准入：有活跃提醒的会话拒绝归档，归档停止则删除其任务行
  - 证据: `package.json:60 peerDep + src/index.ts:9 type import SessionActivity、src/types.ts:11 type import、src/types.ts:352 declare module SessionActivityKindMap；src/index.ts:189 ctx.on('workspace/session-activity')、src/index.ts:199 ctx.on('workspace/session-stop')`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 把该业务包的 /remote 命名空间装配进 Client
- `dsh-client-ui-schedule` - 任务记录、删除结果与更新请求的类型契约由 schedule 包持有
- `dsh-client-ui-workspace` - 归档确认展示定时任务占用信息
- `dsh-tool-schedule` - 复用提醒服务的规范词表与视图，并把工具注册在能解析到该服务的 scope（由 preset 装配决定）
