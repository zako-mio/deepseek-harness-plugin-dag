# dsh-subagent-codex

- 包名: `@deepseek-ai/dsh-subagent-codex`
- 分组: G33 子代理外部后端
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/subagent/subagent-codex`

## 实现逻辑
固定 Codex one-shot 子代理 provider：每次被接受的 run 在委派 Session 的 workspace 启动官方 codex app-server --stdio 子进程，仅在 ephemeral thread 存在后发布；declares NO_START_CAPABILITIES。wire.ts 复用 dsh-sdk-protocol 的 JsonRpcLineTransport 实现 app-server 帧协议，外部 @openai/codex(0.147.0) 提供 CLI 类型。

## Provides
- ctx.subagents 命名 provider 'codex'(one-shot)
- startCodexRun
- wire.ts: JsonRpcLineTransport 帧适配

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - ContentBlock 类型
  - 证据: `packages/subagent/subagent-codex/src/wire.ts:11, packages/subagent/subagent-codex/src/run.ts:11`
- `dsh-session` [编译依赖] - SessionId 类型
  - 证据: `packages/subagent/subagent-codex/src/run.ts:12`
- `dsh-subagent` [运行时依赖] - inject ['subagents'] 注册 provider；SubagentProvider/SubagentResult 类型(E1)
  - 证据: `packages/subagent/subagent-codex/src/index.ts:12-19,27, packages/subagent/subagent-codex/src/run.ts:20, packages/subagent/subagent-codex/src/wire.ts:12`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
