# dsh-tool-bash-persistent

- 包名: `@deepseek-ai/dsh-tool-bash-persistent`
- 分组: G30 外部执行后端
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/shell/tool-bash-persistent`

## 实现逻辑
注册单个持久 `bash` 工具 (src/index.ts:374-398)；persistentShells 以 WeakMap/Map 缓存 owner→PTY session (:200-270)，经 ctx.terminals.spawn(backendType) (:234) 创建、stty/PS1 初始化 (:246-250)；命令以 nonce 起止标记包裹 (:62-83)，轮询 scrollback 收尾 (:145-168)，deadline 超时→reset (:280,:307-321)，shell 退出→reset (:330-341)；per-owner 串行队列 (:362-372)；inject ['tools','terminals'] (:402)。

## Provides
- tool: bash（owner 作用域持久 shell）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - owner 隔离与 shell 生命周期
  - 证据: `package.json:34 peerDep + src/index.ts:9 import type Agent；E2: :391 exec.agent owner、:201-204 per-owner 缓存`
- `dsh-tools` [E1+E2] - 工具注册
  - 证据: `package.json:38 peerDep + src/index.ts:12 import defineTool；E2: :374 ctx.tools.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
