# dsh-tool-todo

- 包名: `@deepseek-ai/dsh-tool-todo`
- 分组: G44 待办
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/todo/tool-todo`

## 实现逻辑
面向模型的整表替换 todo_write 工具：校验去空白、唯一 content 与 in_progress 策略（src/index.ts:80-100），并把 todo/write 快照 append 到调用 Agent 的 session（src/index.ts:199）。同时注册 sessionProjections 的 todos 投影（最新列表、turn/start 清零，src/index.ts:123-134），配套 invariant 伴生插件校验耐久日志的形状与 turn 边界（src/invariant.ts:24-58）。

## Provides
- 工具 todo_write（注册 ctx.tools，src/index.ts:135）
- ctx.sessionProjections 的 todos 投影单元（src/index.ts:123）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - todo 列表挂在调用 Agent 的 session 上
  - 证据: `package.json:44 peerDep + src/index.ts:199 exec.agent.session.append`
- `dsh-invariants` [E1+E2] - 注册 todo 快照不变量校验
  - 证据: `package.json:45 peerDep + src/invariant.ts:5 import InvariantInstaller + src/invariant.ts:104 ctx.invariants.register`
- `dsh-session` [E1+E2] - 耐久校验基于 session 事件日志
  - 证据: `package.json:46 peerDep + src/invariant.ts:4 import Session/SessionEvent + src/invariant.ts:92 ctx.on('session/event')`
- `dsh-session-projection` [E1+E2] - 注册 todos 投影单元
  - 证据: `package.json:47 peerDep + src/index.ts:15 type-only import + src/index.ts:23 inject ['sessionProjections']`
- `dsh-tools` [E1+E2] - 注册 todo_write 工具
  - 证据: `package.json:48 peerDep + src/index.ts:12 import defineTool + src/index.ts:23 inject ['tools']`

## Dependents (下游被依赖)
- `dsh-client-ui-conversation` - Todo 记录与 Todo 停靠面板
