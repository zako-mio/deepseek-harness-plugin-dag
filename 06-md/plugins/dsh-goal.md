# dsh-goal

- 包名: `@deepseek-ai/dsh-goal`
- 分组: G17 目标与计划
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/goal/goal`

## 实现逻辑
实现同会话目标的领域服务：GoalService 继承 TypertRemoteService 并注册为 ctx.goals，把目标状态唯一存放在所属会话日志中，构造期订阅 agent/created 把 activation 置为 disarmed，并注册 key 为 goal 的投影 (src/index.ts:239-268)。所有变更（create/edit/pause/resume/complete/block/clear）先做 compare-and-set 校验当前 ref，再由 commit 以 agent.session.append('goal/change', change) 追加全量快照事件，并借 pendingActivation 与 append 返回的 seq 比对把进程内 activation 绑定到该次提交 (src/index.ts:589-626)。投影侧用严格 replay fold 加 zod 校验把事件折叠成可检查点状态，首个非法事件记入 failure 而不抛穿注册表 (src/index.ts:146-169)。

## Provides
- ctx.goals（GoalService：get / disarm / create / edit / pause / resume / complete / block / clear，含 @Remote 远程导出）
- key 为 goal 的 session projection（当前目标 + seenGoalIds + failure，stateVersion 6）
- goal/activation-changed 事件（进程内 activation 边沿变化通知）
- goal/changed 作用域事件（经 agentEvents 按 Agent 发出）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 按 Agent 作用域发出目标变更事件，并用 agents 注册表校验 Agent 是否为存活实例
  - 证据: `src/index.ts:12-13 import agentEvents / type Agent + src/index.ts:241 static inject ['agents','sessionProjections'] + src/index.ts:625 agentEvents(this.ctx, agent).emit('goal/changed')`
- `dsh-llm` [编译依赖] - GoalError 继承 HarnessError 携带稳定 code；目标轮次消息来源沿用 LLM 消息来源词汇
  - 证据: `src/runtime.ts:3 import HarnessError + src/fold.ts:3 import type MessageSource`
- `dsh-session` [E1+E2] - 目标状态以会话事件为唯一持久化载体，并在事件落地时同步 activation
  - 证据: `src/index.ts:14-15 import SessionSeq / type Session + src/index.ts:613 agent.session.append('goal/change', change) + src/index.ts:259 ctx.on('session/event')`
- `dsh-session-projection` [E1+E2] - 把目标折叠注册为可检查点、可下发给客户端的会话投影
  - 证据: `src/index.ts:17-18 import type {} / type ProjectionDefinition + src/index.ts:258 ctx.sessionProjections.register(goalProjectionDefinition)`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 把该业务包的 /remote 命名空间装配进 Client
- `dsh-client-ui-conversation` - 目标投影类型
- `dsh-client-ui-goal` - 复用 goal 投影与 Remote 契约类型
- `dsh-command-goal` - 通过目标域服务读写持久化目标并捕获 GoalError
- `dsh-goal-round-driver` - 读取当前目标、写入 blocker、撤销 activation，并复用目标消息来源词汇
- `dsh-tool-goal` - 通过目标域服务执行工具操作并读取 CAS 引用
