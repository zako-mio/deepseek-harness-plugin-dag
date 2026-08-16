# dsh-subagent-claude-code

- 包名: `@deepseek-ai/dsh-subagent-claude-code`
- 分组: G33 子代理外部后端
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/subagent/subagent-claude-code`

## 实现逻辑
固定 Claude Code one-shot 子代理 provider：每次被接受的 run 经官方 Agent SDK 在委派 Session 的 workspace 启动真实 CLI 子进程，置于共享 subprocess owner 之下；declares NO_START_CAPABILITIES(inheritsParentContext=false)。经外部 @anthropic-ai/sdk(0.93.0)+@anthropic-ai/claude-agent-sdk(0.3.220) 通信，env 显式条目层叠在 subprocess seam 的 credential-scrubbed 父环境之上。

## Provides
- ctx.subagents 命名 provider 'claude-code'(one-shot)
- startClaudeCodeRun
- disposeGraceMs 进程树终止控制

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - ContentBlock 类型
  - 证据: `packages/subagent/subagent-claude-code/src/run.ts:18`
- `dsh-session` [编译依赖] - SessionId 类型
  - 证据: `packages/subagent/subagent-claude-code/src/run.ts:19`
- `dsh-subagent` [运行时依赖] - inject ['subagents'] 注册 provider；SubagentProvider/ResolvedSubagentStartRequest 类型(E1)
  - 证据: `packages/subagent/subagent-claude-code/src/index.ts:12-19,27, packages/subagent/subagent-claude-code/src/run.ts:27`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
