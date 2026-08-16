# dsh-client-ui-model-selection

- 包名: `@deepseek-ai/dsh-client-ui-model-selection`
- 分组: G28 设置输入UI
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-model-selection`

## 实现逻辑
模型选择双入口共享每会话 ModelDirectory：注册 ModelDirectoryResolver（ctx.modelDirectories，service.ts:34-47）与 /model popupSelect 贡献（command.register，index.ts:122-151）、conversation.input.model seat（:154-175）。目录经 session.models RPC 加载、session.selectModel 提交（directory.ts:67,98-105），Host 报告当前选择为唯一事实；向 composer 发布 routable=false 输入封锁（service.ts:88-103）。

## Provides
- ctx.modelDirectories (ModelDirectoryResolver)
- /model popupSelect 命令贡献
- conversation.input.model seat (ModelSelect)
- model 字典

## Depends On (上游依赖)
- `dsh-api-remotes` [运行时依赖] - 模型目录加载与选择提交
  - 证据: `packages/client/ui-model-selection/src/client/directory.ts:67,98-105 (session.models / session.selectModel RPC)`
- `dsh-client-connection` [运行时依赖] - 会话 wire 面
  - 证据: `packages/client/ui-model-selection/src/client/service.ts:76 (connection.api.sessions)`
- `dsh-client-ui-commands` [运行时依赖] - popupSelect 贡献注册
  - 证据: `packages/client/ui-model-selection/src/client/index.ts:100,122-150 (inject commandUi + command.register)`
- `dsh-client-ui-conversation` [编译依赖] - composer model 槽声明
  - 证据: `packages/client/ui-model-selection/src/client/index.ts:19 (type-only import input.model seat)`
- `dsh-session` [运行时依赖] - 会话目录键与可用性判定
  - 证据: `packages/client/ui-model-selection/src/client/service.ts:35,73-75,80 (inject sessions + sessions.scope + subagentAddress)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
