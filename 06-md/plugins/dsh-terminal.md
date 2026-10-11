# dsh-terminal

- 包名: `@deepseek-ai/dsh-terminal`
- 分组: G42 终端
- 拓扑层: Layer 4
- 来源层: L3 其余
- 源码路径: `packages/terminal/terminal`

## 实现逻辑
owner 作用域的持久 PTY 注册表：TerminalSessionService 注册 ctx.terminals（src/index.ts:105-118），管理 backend 注册（src/index.ts:125-137）、按精确 Agent owner 隔离的会话发布（src/index.ts:154-224）与 awaited 清理（src/index.ts:423-454）。服务只拥有 ids、发布、授权与清理，把终端机制留给 backend（src/types.ts:166-171），并以机器可路由的 TerminalError 暴露失败（src/index.ts:55-71）。

## Provides
- ctx.terminals（持久 PTY 会话 seam：backend 注册、owner 隔离 id、send/read/signal/close 与 awaited 清理）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 以精确 Agent 作为会话 owner，并绑定其生命周期做 cleanup
  - 证据: `package.json:30 peerDep + src/index.ts:8 import Agent + src/index.ts:319 ctx.get('agents')`

## Dependents (下游被依赖)
- `dsh-terminal-bash` - 实现 TerminalBackend 契约并通过 ctx.terminals.registerBackend 把本地后端登记进终端注册表
- `dsh-tool-bash-persistent` - 持久会话的 spawn、发送、读取与 kill 全部由终端 seam 提供
- `dsh-tool-pwsh-persistent` - 持久会话的 spawn/发送/读取/kill 由终端 seam 提供
- `dsh-tool-terminal` - 声明并调用 terminals 服务完成 spawn/startSend/read/signal/kill/list 全部 owner 隔离的 PTY 操作
