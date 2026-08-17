# dsh-terminal-bash

- 包名: `@deepseek-ai/dsh-terminal-bash`
- 分组: G30 外部执行后端
- 拓扑层: Layer 4
- 来源层: L3 其余
- 源码路径: `packages/terminal/terminal-bash`

## 为什么需要它（设计初衷）
ctx.terminals 的持久 shell 后端：基于 PTY 的交互式 bash 会话管理。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/terminal/terminal-bash/README.md

## 实现逻辑
BashTerminalBackend implements TerminalBackend (src/index.ts:102)，apply 经 ctx.terminals.registerBackend (:152) 注册 'shell' backend；spawn 解析 sandboxPolicy (:122)、danger-full-access 外经 ctx.sandbox.confine 包裹 argv (:74-79)、subprocess.spawnTerminal 生成 SubprocessTerminalHandle (:125)、LocalPtySession 封装 (:134)；ensureSandboxModeFence 在存活 PTY 期间拒绝 sandbox/mode 切换 (:34-53)；childEnvironment 注入 DSH_* 环境 (:55-69)。

## Provides
- ctx.terminals 的 PTY backend type='shell'（config.ts:45 backendType 默认 'shell'）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - owner 隔离与 agent 事件上下文
  - 证据: `package.json:35 peerDep + src/index.ts:8 import type Agent；E2: :43 owner.ctx.on、:47 owner.session`
- `dsh-sandbox-policy` [E1+E2] - 沙箱模式决策与默认模式
  - 证据: `package.json:39 peerDep + src/index.ts:14 import effectiveSandboxMode；E2: :25 inject、:122 ctx.sandboxPolicy.resolve`
- `dsh-session` [E1+E2] - 会话事件驱动模式围栏
  - 证据: `package.json:40 peerDep + src/index.ts:9 import Session/SessionEvent；E2: :45-46 owner.ctx.on('internal/dispatch','session/event') 订阅 sandbox/mode`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
