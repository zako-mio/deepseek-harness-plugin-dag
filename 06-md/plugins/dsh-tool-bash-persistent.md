# dsh-tool-bash-persistent

- 包名: `@deepseek-ai/dsh-tool-bash-persistent`
- 分组: G36 Shell 执行
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/shell/tool-bash-persistent`

## 实现逻辑
向模型注册基于 PTY 的持久 bash 工具：每个 owner(Agent) 映射一个持久终端会话，命令用随机 nonce 的起止标记包裹后发送，轮询 scrollback 直到读到结束标记/超时/会话退出 (src/index.ts:297-390)。persistentShells() 管理按 owner 的创建/复用/重置与 fiber 处置清理，初始化时先发送 stty -echo 抑制回显 (src/index.ts:223-295)。输出按 maxOutputChars 截断（不切断代理对）并渲染退出码/超时/重置提示；同一 owner 的调用经队列串行化 (src/index.ts:58-221, 401-437)。

## Provides
- 模型工具 bash (基于 owner 级 PTY 持久会话的持久 bash，状态跨调用保持)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 以 Agent 为 owner 隔离持久 shell 并读取其会话 cwd
  - 证据: `src/index.ts:9 import type { Agent }; package.json:29 peerDep`
- `dsh-terminal` [E1+E2] - 经 owner 级 PTY 服务创建/发送/读取/终止持久 shell 会话
  - 证据: `src/index.ts:11 import type { TerminalSessionId }; src/index.ts:441 inject ['terminals']; src/index.ts:257 ctx.terminals.spawn`
- `dsh-tools` [E1+E2] - 注册持久 bash 工具定义
  - 证据: `src/index.ts:13 import defineTool; src/index.ts:441 inject ['tools']; src/index.ts:413 ctx.tools.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
