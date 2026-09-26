# dsh-terminal

- 包名: `@deepseek-ai/dsh-terminal`
- 分组: G43 终端
- 拓扑层: Layer 5
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
- `dsh-terminal-bash` - 向 PTY seam 注册 backend 并复用其类型与 TerminalError
- `dsh-tool-bash-persistent` - 经 owner 级 PTY 服务创建/发送/读取/终止持久 shell 会话
- `dsh-tool-pwsh-persistent` - 经 owner 级 PTY 服务创建/发送/读取/终止持久 shell 会话
- `dsh-tool-terminal` - 调用 ctx.terminals 的会话操作
