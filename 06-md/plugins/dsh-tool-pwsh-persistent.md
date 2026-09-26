# dsh-tool-pwsh-persistent

- 包名: `@deepseek-ai/dsh-tool-pwsh-persistent`
- 分组: G36 Shell 执行
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/shell/tool-pwsh-persistent`

## 实现逻辑
向模型注册基于 PTY 的持久 pwsh 工具，与 tool-bash-persistent 逐调用对称：按 owner(Agent) 维护持久 PowerShell 会话，用 nonce 标记包裹命令（quoteForPwsh 转义反引号、引号、`$`、换行与 ESC）后发送并轮询 (src/index.ts:81-99, 308-402)。persistentShells() 负责按 owner 的会话创建/复用/重置与 fiber 处置清理；executeCommand 处理超时、abort、会话退出与 stdin_read 的提前返回 (src/index.ts:245-306, 331-401)。输出按上限截断并渲染退出码/重置/超时提示 (src/index.ts:57-243)。

## Provides
- 模型工具 pwsh (基于 owner 级 PTY 持久会话的持久 PowerShell，状态跨调用保持)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 以 Agent 为 owner 隔离持久 shell 并读取其会话 cwd
  - 证据: `src/index.ts:11 import type { Agent }; package.json:29 peerDep`
- `dsh-terminal` [E1+E2] - 经 owner 级 PTY 服务创建/发送/读取/终止持久 shell 会话
  - 证据: `src/index.ts:13 import type { TerminalSessionId }; src/index.ts:453 inject ['terminals']; src/index.ts:279 ctx.terminals.spawn`
- `dsh-tools` [E1+E2] - 注册持久 pwsh 工具定义
  - 证据: `src/index.ts:15 import defineTool; src/index.ts:453 inject ['tools']; src/index.ts:425 ctx.tools.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
