# dsh-tool-todo

- 包名: `@deepseek-ai/dsh-tool-todo`
- 分组: G23 工具守卫
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/todo/tool-todo`

## 实现逻辑
apply() 注册 todo_write 工具：整表替换语义，execute 校验后 exec.agent.session.append('todo/write')，返回新表+counts；无 agent 则拒绝。ctx.inject(['sessionProjections']) 注册 'todos' 投影(last todo/write 快照，turn/start 清空)。

## Provides
- ctx.tools: todo_write
- session 事件 todo/write
- todos session projection

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - owning session 归属
  - 证据: `packages/todo/tool-todo/src/index.ts:208-212`
- `dsh-session` [运行时依赖] - todo 快照持久化
  - 证据: `packages/todo/tool-todo/src/index.ts:13,213`
- `dsh-session-projection` [组合依赖] - todos 投影单元
  - 证据: `packages/todo/tool-todo/src/index.ts:135`
- `dsh-tools` [组合依赖] - 工具注册
  - 证据: `packages/todo/tool-todo/src/index.ts:12,149`

## Dependents (下游被依赖)
- `dsh-client-ui-conversation` - todos 投影类型（todo dock 数据）
