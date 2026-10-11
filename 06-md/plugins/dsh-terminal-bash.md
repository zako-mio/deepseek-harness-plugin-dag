# dsh-terminal-bash

- 包名: `@deepseek-ai/dsh-terminal-bash`
- 分组: G42 终端
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/terminal/terminal-bash`

## 实现逻辑
apply() 解析并校验配置后，把 BashTerminalBackend 注册进 ctx.terminals 的 backendType（默认 'shell'）槽位，从而以终端 seam 的 provider 身份提供持久 PTY shell (src/index.ts:234-239, src/config.ts:93-110)。spawn() 先经 ensureSandboxModeFence 在 owner 的 internal/dispatch 上挂沙箱模式变更围栏（有活动终端时拒绝改 mode），再用 ctx.sandboxPolicy.resolve 取策略、非 full-access 时经 ctx.get('sandbox').confine 包裹 argv，最后走 ctx.subprocess.spawnTerminal 并按方言做启动就绪握手 (src/index.ts:38-63, src/index.ts:101-110, src/index.ts:202-231)。LocalPtySession 用 @xterm/headless 维护有界滚动缓冲，靠 CONTROLLED_PROMPT 标记 + 前台进程组采样判定 stdin_read/inferred_idle/session_exit (src/session.ts:278-305, src/session.ts:549-608)。

## Provides
- ctx.terminals (注册 `shell` 类型的本地持久 PTY 后端：按 session 打开交互式 bash/pwsh 并给出有界输出与就绪判定)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 后端以 Agent 为 owner 单位持有会话与围栏状态（sandboxModeFences 以 Agent 为键）
  - 证据: `package.json:30 peerDep + src/index.ts:9 import type { Agent }`
- `dsh-pwsh-local` [编译依赖] - pwsh 方言下解析 shell 可执行路径，并在启动时写入 UTF-8 编码前导
  - 证据: `package.json:42 dependency + src/config.ts:4 import { resolvePwshPath } + src/index.ts:17 import { ENCODING_PREAMBLE }`
- `dsh-sandbox-policy` [运行时依赖] - 解析调用方 Session 当前生效的执行策略（mode 与围栏配置）作为启动 shell 的输入
  - 证据: `package.json:33 peerDep + src/index.ts:42 ctx.sandboxPolicy + src/index.ts:205 resolve({ session })`
- `dsh-session` [编译依赖] - 围栏监听 session/event 时需要 Session 与 SessionEvent 的类型面（判断 sandbox/mode 事件）
  - 证据: `package.json:34 peerDep + src/index.ts:10 import type { Session, SessionEvent }`
- `dsh-session-projection` [运行时依赖] - 读取 sandboxMode 投影的折叠状态，作为围栏比较的当前模式依据
  - 证据: `package.json:37 peerDep + src/index.ts:16 import type {} + src/index.ts:43 ctx.sessionProjections (stateOf 于 src/index.ts:56)`
- `dsh-terminal` [E1+E2] - 实现 TerminalBackend 契约并通过 ctx.terminals.registerBackend 把本地后端登记进终端注册表
  - 证据: `package.json:31 peerDep + src/index.ts:11-12 import (TerminalBackend, TerminalBackendCleanupError) + src/index.ts:41 ctx.terminals`
- `dsh-working-directory` [运行时依赖] - 在调用方未显式给 cwd 时解析并确保该 Agent 的工作目录
  - 证据: `package.json:38 peerDep + src/index.ts:7 import type {} + src/index.ts:211 ctx.workingDirectory.ensure(owner, signal)`

## Dependents (下游被依赖)
- `dsh-tool-bash-persistent` - 没有对应 PTY 后端时 spawn 无后端可用
- `dsh-tool-pwsh-persistent` - Windows 侧持久会话依赖该 PTY 后端注册
