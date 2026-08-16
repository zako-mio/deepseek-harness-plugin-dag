# dsh-client-ui-plan

- 包名: `@deepseek-ai/dsh-client-ui-plan`
- 分组: G28 设置输入UI
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-plan`

## 实现逻辑
Composer plan seat：注册 conversation.input.plan 槽的 PlanChip（index.ts:52-64），经 useProjection('plan') 读 plan-mode 会话投影决定显隐（PlanModeControl.tsx:20,32-34），退出时 ctx.remote.commands.execute(sessionId, '/plan off')（index.ts:58-62）。host 半注释明确 plan 行为本体归 dsh-plan-mode（src/index.ts:5-7）。

## Provides
- conversation.input.plan 槽 'PlanChip' 注册
- plan 字典

## Depends On (上游依赖)
- `dsh-client-ui-conversation` [编译依赖] - composer plan 槽声明
  - 证据: `packages/client/ui-plan/src/client/index.ts:13 (type-only import input.plan seat)`
- `dsh-commands` [运行时依赖] - 执行 /plan off 命令通道
  - 证据: `packages/client/ui-plan/src/client/index.ts:58 (ctx.remote.commands.execute)`
- `dsh-plan-mode` [编译依赖] - plan 投影会话值决定 chip 显隐（web 下 plan-mode 被 disabled 仍取投影）
  - 证据: `packages/client/ui-plan/src/client/index.ts:17 (type-only import plan SessionProjectionMap), PlanModeControl.tsx:20 (useProjection('plan'))`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
