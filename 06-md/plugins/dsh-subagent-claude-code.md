# dsh-subagent-claude-code

- 包名: `@deepseek-ai/dsh-subagent-claude-code`
- 分组: G33 子代理外部后端
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/subagent/subagent-claude-code`

## 为什么需要它（设计初衷）
注册 claude-code 子代理 provider：在父会话工作区调用官方 Claude Agent SDK。

发展史：RC8 Claude Code子代理Profile Bundle按需安装 + 非交互权限模式

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/subagent/subagent-claude-code/README.md

## 实现逻辑
index.ts:37,40 由固定'claude-code' provider改为可配置 providerName(默认claude-code，支持多命名实例); index.ts:46-52 + run.ts:42-55 新增 permissionMode 配置(dontAsk默认/acceptEdits/auto/plan/bypassPermissions)固定非交互权限。cordis.patch.yml 将provider注册为可选 Profile Bundle(dsh.bundle.patch)，支持按需安装; process.ts:20 移除Windows batch shim改用共享subprocess管理。

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
