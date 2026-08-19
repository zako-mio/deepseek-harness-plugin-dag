# dsh-subagent-codex

- 包名: `@deepseek-ai/dsh-subagent-codex`
- 分组: G33 子代理外部后端
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/subagent/subagent-codex`

## 为什么需要它（设计初衷）
ACP 子代理 provider（对应仓库目录 subagent-acp，Codex 场景）：每子代理独立子进程按 Agent Client Protocol 驱动，冷启动隔离环境。

发展史：RC8 Codex Profile Bundle按需安装 + 非交互权限模式 + 多命名实例

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/subagent/subagent-acp/README.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-subagent-codex

## 实现逻辑
index.ts:37,44 改为 providerName 可配置(多命名实例); run.ts:37-127 新增 CodexPermissionMode(never默认/approve-for-me/dangerously-bypass-approvals-and-sandbox)，wire.ts:24-33 THREAD_PERMISSION_PARAMS 映射到thread/start审批策略，实现非交互权限模式。run.ts:40-45 用 createRequire 解析 @openai/codex bin 生成包内wrapper(CODEX_PACKAGE_BIN)，argv固定为[node, wrapper, app-server, --stdio]，不依赖PATH的codex命令，支持Profile Bundle按需安装。cordis.patch.yml可选注册; @openai/codex 由devDeps移入deps。

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
