# dsh-subagent-fork-in-process

- 包名: `@deepseek-ai/dsh-subagent-fork-in-process`
- 分组: G39 子代理
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/subagent/subagent-fork-in-process`

## 实现逻辑
进程内 FORK 子代理后端：apply 把 `ForkInProcessProvider` 注册到 `ctx.subagents`（默认名 `fork`）(src/index.ts:83-85)。它的核心是 `completedTurnPrefix`——取父会话日志中截至最后一个 `turn/end` 的平衡前缀，因实时 seq 等于数组下标，该前缀仍是自 seq 0 起连续的合法种子 (src/index.ts:46-53)。provider 声明 agentOptions/outputSchema/depthLimit/toolFilter/persona 全部可用，并置 `inheritsParentContext = true`，prepareContinuable 在创建时一次性捕获该前缀作为子会话种子，使后续冷恢复重放该前缀而不是重新 fork 父级更新的历史 (src/index.ts:61-80)。

## Provides
- ctx.subagents 上的 `fork` provider（进程内子代理，子会话以父级已完成轮次前缀为种子）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 以 Agent 为父级读取其会话历史
  - 证据: `src/index.ts:13 import type { Agent } + src/index.ts:46 completedTurnPrefix(parent: Agent)`
- `dsh-session` [编译依赖] - fork 种子直接来自父会话事件日志
  - 证据: `src/index.ts:12 import type { SessionEvent } + src/index.ts:48 parent.session.snapshotEvents()`
- `dsh-subagent` [E1+E2] - provider 契约与注册入口
  - 证据: `src/index.ts:14-19 import ContinuableCreateRequest/SubagentProvider + src/index.ts:26 inject ['subagents'] + src/index.ts:84 registerProvider`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
