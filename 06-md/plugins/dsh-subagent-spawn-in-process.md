# dsh-subagent-spawn-in-process

- 包名: `@deepseek-ai/dsh-subagent-spawn-in-process`
- 分组: G39 子代理
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/subagent/subagent-spawn-in-process`

## 实现逻辑
最轻的进程内 SPAWN 子代理后端：apply 把 `SpawnInProcessProvider` 注册到 `ctx.subagents`（默认名 `spawn`）(src/index.ts:59-61)。provider 声明全部五项启动能力可用（因为它参与子代理构造，可在创建窗口内施加深度上限、结构化输出、路由合并与 scoped 工具/人格），并置 `inheritsParentContext = false`，因为子代理是同一 cordis 上下文上的全新 Agent（独立 session 与系统提示、零父级上下文）(src/index.ts:39-50)。prepareContinuable 返回空 spec，表示不贡献任何种子，后续操作全归 continuation manager 所有 (src/index.ts:52-56)。

## Provides
- ctx.subagents 上的 `spawn` provider（进程内全新子代理，复用 agent factory 的静默销毁）

## Depends On (上游依赖)
- `dsh-subagent` [E1+E2] - provider 契约与注册入口（子代理 Agent 的构造由子代理 seam 的 manager 负责）
  - 证据: `src/index.ts:11-15 import ContinuableCreateSpec/SubagentProvider + src/index.ts:20 inject ['subagents'] + src/index.ts:60 registerProvider`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
