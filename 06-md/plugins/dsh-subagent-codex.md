# dsh-subagent-codex

- 包名: `@deepseek-ai/dsh-subagent-codex`
- 分组: G41 子代理
- 拓扑层: Layer 7
- 来源层: L3 其余
- 源码路径: `packages/subagent/subagent-codex`

## 实现逻辑
以 CodexProvider 注册 provider codex，声明零启动能力并只从 parent 读取 workspace cwd (src/index.ts:63-109)。start() 经 ctx.subprocess.spawn 启动包内 codex app-server --stdio，wire.ts 用共享 JsonRpcLineTransport 完成 initialize、创建 ephemeral thread 并驱动 turn (src/run.ts:225-301, src/wire.ts:192-374)。无人值守审批按 permissionMode 选择 cancel/decline，仅最终答案计入结果，失败按 stage/category 映射为固定诊断，dispose 关闭 wire 并终止进程 (src/wire.ts:571-630, src/run.ts:380-438)。

## Provides
- ctx.subagents 注册的 provider `codex` (Codex app-server 进程外子代理)

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 使用内容块类型
  - 证据: `src/run.ts:15 (import type ContentBlock)`
- `dsh-session` [编译依赖] - 品牌化 run id
  - 证据: `src/run.ts:16 (import type SessionId)`
- `dsh-subagent` [E1+E2] - 复用 seam 契约与共享辅助并注册 provider
  - 证据: `src/index.ts:12-19 (import NO_START_CAPABILITIES, resolveChildCwd, 类型) + src/index.ts:31 (inject ['subagents','subprocess']) + src/index.ts:135 (ctx.subagents.registerProvider)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
