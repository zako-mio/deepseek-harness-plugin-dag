# dsh-goal

- 包名: `@deepseek-ai/dsh-goal`
- 分组: G17 目标与计划
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/goal/goal`

## 实现逻辑
GoalService 以会话日志为唯一持久源：每次变更把完整快照写成一个 goal/change 会话事件（src/index.ts:609-626），并由 goalProjectionDefinition 严格重放派生当前目标（src/index.ts:146-169）。fold.ts 提供纯函数式解码/校验/折叠，逐操作校验相位转移与修订号恰好加一（src/fold.ts:199-332）。进程本地的 activation（armed/disarmed）单独保存，变更时 emit 'goal/activation-changed'（src/index.ts:496-515）。invariant.ts 以独立增量折叠校验全量目标流的合法性（src/invariant.ts:40-80）。

## Provides
- ctx.goals (目标域服务 seam：create/edit/pause/resume/complete/block/clear/get/disarm + 远程绑定)
- goal 会话投影 ('goal' 投影键，含 seenGoalIds 与失败状态)
- goal/change 会话事件类型 (持久化目标变更载荷)
- goal/changed 与 goal/activation-changed 事件 (变更通知与进程本地激活边)
- goal-invariant 不变量伴随件 (目标流严格重放校验)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 以 agent 为键持有运行时激活状态、校验 live 身份并订阅 agent/created
  - 证据: `src/index.ts:12-13 import (agentEvents, Agent) + src/index.ts:241 inject ['agents','sessionProjections'] + src/index.ts:470 ctx.agents.get`
- `dsh-invariants` [E1+E2] - 注册目标流不变量校验伴随件
  - 证据: `src/invariant.ts:4 import InvariantInstaller + src/invariant.ts:14 inject ['invariants'] + src/invariant.ts:80 ctx.invariants.register`
- `dsh-llm` [编译依赖] - 目标消息来源类型合并与 GoalError 的错误基类
  - 证据: `src/fold.ts:3 import MessageSource + src/runtime.ts:3 import HarnessError`
- `dsh-scope` [编译依赖] - goal/changed 事件按 agent 作用域分发的类型约束
  - 证据: `src/domain.ts:114 import('@deepseek-ai/dsh-scope').Scoped + package.json peerDependencies`
- `dsh-session` [E1+E2] - 以会话事件日志作为目标状态的唯一持久来源
  - 证据: `src/fold.ts:4 import SessionEvent + src/index.ts:14-15 import SessionSeq/Session + src/index.ts:613 agent.session.append('goal/change', change)`
- `dsh-session-projection` [E1+E2] - 注册并读取 'goal' 会话投影以派生当前目标
  - 证据: `src/index.ts:17-18 import (ProjectionDefinition) + src/index.ts:258 ctx.sessionProjections.register(goalProjectionDefinition) + src/index.ts:477 ctx.sessionProjections.stateOf(session,'goal')`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配 goal 命名空间
- `dsh-client-ui-conversation` - 目标模式输入提示
- `dsh-client-ui-goal` - 目标投影与目标标识类型
- `dsh-command-goal` - 通过目标域服务读写持久化目标并捕获 GoalError
- `dsh-goal-round-driver` - 读取目标状态、disarm/block/pause 并在续轮消息上标注目标来源
- `dsh-tool-goal` - 通过目标域服务执行工具操作并读取 CAS 引用
