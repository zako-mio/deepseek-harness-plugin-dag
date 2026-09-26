# dsh-subagent-claude-code

- 包名: `@deepseek-ai/dsh-subagent-claude-code`
- 分组: G41 子代理
- 拓扑层: Layer 7
- 来源层: L3 其余
- 源码路径: `packages/subagent/subagent-claude-code`

## 实现逻辑
以 ClaudeCodeProvider 注册 provider claude-code，声明零启动能力并仅从 parent 读取 workspace cwd (src/index.ts:73-126)。start() 在父会话 workspace 中调用官方 @anthropic-ai/claude-agent-sdk 的 query()，并用自定义 spawnClaudeCodeProcess 把真实 CLI 进程托管到 ctx.subprocess (src/run.ts:316-377, 385-449)。只有严格 SDK success 才算完成，工具权限/MCP elicitation/用户对话框一律无人值守拒绝或取消，dispose 关闭 query 并终止整段进程 (src/run.ts:206-306, 571-586)。

## Provides
- ctx.subagents 注册的 provider `claude-code` (官方 Claude Agent SDK 进程外子代理)

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 使用内容块类型
  - 证据: `src/run.ts:18 (import type ContentBlock)`
- `dsh-session` [编译依赖] - 品牌化 run id
  - 证据: `src/run.ts:20 (import type SessionId)`
- `dsh-subagent` [E1+E2] - 复用 seam 契约与共享辅助并注册 provider
  - 证据: `src/index.ts:12-19 (import NO_START_CAPABILITIES, resolveChildCwd, 类型) + src/index.ts:31 (inject ['subagents','subprocess']) + src/index.ts:151 (ctx.subagents.registerProvider)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
