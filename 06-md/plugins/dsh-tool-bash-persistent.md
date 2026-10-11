# dsh-tool-bash-persistent

- 包名: `@deepseek-ai/dsh-tool-bash-persistent`
- 分组: G34 Shell 执行
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/shell/tool-bash-persistent`

## 实现逻辑
基于 owner 作用域的 PTY seam（`ctx.terminals`）实现跨调用保持状态的持久 `bash` 工具：按 Agent 用 WeakMap 缓存会话并惰性 spawn，初始化时发送 `stty -echo` 抑制回显 (src/index.ts:251-293)。每条命令被包进带随机 nonce 的单行 START/END wrapper，用 `startSend` 提交后轮询 scrollback，靠标记与紧邻的退出码提取输出 (src/index.ts:66-107、src/index.ts:321-390)。超时、中止、shell 退出都会 reset 该 owner 的会话并追加“下次从工作区全新开始”的提示 (src/index.ts:201-222、src/index.ts:350-377)；同一 owner 的调用经 WeakMap 队列串行化，避免并发写同一 PTY (src/index.ts:402-412)。

## Provides
- ctx.tools 上的 `bash` 工具定义（owner 隔离的持久 PTY 会话，跨调用保留 cwd 与环境变量）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 以 Agent 作为会话所有者（owner 隔离与清理）
  - 证据: `package.json:29 peerDependencies '@deepseek-ai/dsh-agent' + src/index.ts:10 type Agent`
- `dsh-terminal` [E1+E2] - 持久会话的 spawn、发送、读取与 kill 全部由终端 seam 提供
  - 证据: `src/index.ts:12 type TerminalSessionId/TerminalReadResult + src/index.ts:258 ctx.terminals.spawn + src/index.ts:334 ctx.terminals.startSend`
- `dsh-terminal-bash` [组合依赖] - 没有对应 PTY 后端时 spawn 无后端可用
  - 证据: `src/index.ts:458 backendType 默认 'shell'（PTY 后端名）；packages/bundle/sdk-minimal/cordis.patch.yml:62-63 由 dsh-terminal-bash 注册该后端`
- `dsh-tools` [E1+E2] - 工具必须注册进工具注册表
  - 证据: `src/index.ts:14 import defineTool + src/index.ts:442 inject 'tools' + src/index.ts:414 ctx.tools.register`
- `dsh-working-directory` [运行时依赖] - 会话初始 cwd 取自 owner 的工作区
  - 证据: `src/index.ts:6 type import + src/index.ts:257 ctx.workingDirectory.ensure(owner, combinedSignal)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
