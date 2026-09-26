# dsh-terminal-bash

- 包名: `@deepseek-ai/dsh-terminal-bash`
- 分组: G43 终端
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/terminal/terminal-bash`

## 实现逻辑
本地持久 shell PTY backend：BashTerminalBackend 经 ctx.subprocess.spawnTerminal 拉起 bash/pwsh 交互会话（src/index.ts:201-230），并注册到 ctx.terminals（src/index.ts:237）。它结合 sandboxPolicy 生成 argv（src/index.ts:100-109）、设置受控提示符 PS1/PROMPT_COMMAND（src/index.ts:64-89），用 LocalPtySession 做有界输出、就绪判定与终端协议回复（src/session.ts:1-60）。

## Provides
- ctx.terminals 的 shell 后端（TerminalBackend 实现，默认 type shell，注册于 src/index.ts:237）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 以会话 owner Agent 及其 session 做沙箱模式护栏
  - 证据: `package.json:30 peerDep + src/index.ts:8 import Agent + src/index.ts:37 ensureSandboxModeFence(owner)`
- `dsh-pwsh-local` [编译依赖] - pwsh 方言的可执行路径解析与 UTF-8 前置
  - 证据: `package.json:41 dep + src/config.ts:4 import resolvePwshPath + src/index.ts:16 import ENCODING_PREAMBLE`
- `dsh-sandbox-policy` [E1+E2] - 解析当前会话的沙箱执行策略
  - 证据: `package.json:33 peerDep + src/index.ts:14 type-only import + src/index.ts:27 inject ['sandboxPolicy']`
- `dsh-session` [编译依赖] - 订阅 session/event 校验 sandbox 模式切换
  - 证据: `package.json:34 peerDep + src/index.ts:9 import Session/SessionEvent`
- `dsh-session-projection` [E1+E2] - 读取 sandboxMode 投影以校验模式切换
  - 证据: `package.json:37 peerDep + src/index.ts:15 type-only import + src/index.ts:27 inject ['sessionProjections']`
- `dsh-terminal` [E1+E2] - 向 PTY seam 注册 backend 并复用其类型与 TerminalError
  - 证据: `package.json:31 peerDep + src/index.ts:10-11 import + src/index.ts:237 ctx.terminals.registerBackend`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
