# dsh-tool-todo

- 包名: `@deepseek-ai/dsh-tool-todo`
- 分组: G43 待办
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/todo/tool-todo`

## 实现逻辑
apply() 在 ctx.sessionProjections 注册 'todos' 投影单元（init 为 null，apply 时 todo/write 整体替换、turn/start 清空，stateVersion 2），并在 ctx.tools 注册模型面向的 todo_write 工具 (src/index.ts:117-134, src/index.ts:135-211)。工具参数是 COMPLETE 任务清单，execute 先经 toTodoList 做 trim 非空、去重、以及非并行部署下至多一个 in_progress 的校验，再 append('todo/write', { todos }) 到调用方 Agent 的 session，非 Agent 调用直接拒绝 (src/index.ts:80-100, src/index.ts:192-208)。描述文案只在 active-status 子句上按 allowParallelInProgress 切换 (src/index.ts:45-67)。类型侧在 types.ts 里声明 todo/write 事件与 todos 投影键，client.ts 与 index.ts 都只是同一真相源的命名空间再导出 (src/types.ts:28-46, src/client.ts:10)。

## Provides
- ctx.tools (注册 `todo_write` 模型工具：整表替换式待办清单写入)
- ctx.sessionProjections (注册 `todos` 投影单元：最新 todo/write 快照，turn/start 后清空)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 待办清单是 per-agent-session 状态，需要 Agent 身份来定位归属会话
  - 证据: `package.json:39 peerDep (Agent 会话身份类型面；src/index.ts:194 以 exec.agent 判定归属)`
- `dsh-session` [编译依赖] - 把待办快照作为 session 事件写入事件溯源日志（日志即唯一真相源）
  - 证据: `package.json:40 peerDep + src/types.ts:28-33 declare module '@deepseek-ai/dsh-session/types' 增补 'todo/write' + src/index.ts:199 exec.agent.session.append`
- `dsh-session-projection` [运行时依赖] - 注册 todos 投影单元，使 UI/客户端能从 session 事件流折叠出当前待办列表
  - 证据: `package.json:41 peerDep + src/index.ts:15 import type {} + src/index.ts:123 ctx.sessionProjections.register`
- `dsh-tools` [运行时依赖] - 用 defineTool 定义 schema/输出渲染并把 todo_write 登记进工具注册表
  - 证据: `package.json:42 peerDep + src/index.ts:12 import { defineTool } + src/index.ts:135 ctx.tools.register`

## Dependents (下游被依赖)
- `dsh-client-ui-conversation` - 待办记录类型与面板
