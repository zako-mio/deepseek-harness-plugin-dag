# dsh-client-ui-plan

- 包名: `@deepseek-ai/dsh-client-ui-plan`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-plan`

## 实现逻辑
浏览器半注册 planDefinition 事件定义与 plan 资源提供者、sidebar 的 plan/plan-review 标签类型，并把 PlanCards 挂到 conversation.chat.turnTail、PlanReviewOpen 挂到 conversation.plan-review.actions、PlanChip 挂到 conversation.input.plan（src/client/index.ts:63-128）。退出计划模式经 ctx.remote.commands.execute 执行 '/plan off'，并把失败还原为可见文本（src/client/index.ts:121-126）。

## Provides

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 执行 /plan off 命令
  - 证据: `src/client/index.ts:2 import type + src/client/index.ts:122 ctx.remote.commands.execute`
- `dsh-api-session-controller` [E1+E2] - 按会话绑定与 subagent 寻址
  - 证据: `src/client/index.ts:13 import type + src/client/index.ts:82 ctx.sessions.binding(sessionId)`
- `dsh-client-locale` [E1+E2] - 注册 plan 字典
  - 证据: `src/client/index.ts:8 import type + src/client/index.ts:59 ctx.locale.register(NS)`
- `dsh-client-resources` [E1+E2] - 注册 plan 资源提供者
  - 证据: `src/client/index.ts:17 import type + src/client/index.ts:64 ctx.resources.register(planResourceProvider(…))`
- `dsh-client-ui-chat` [E1+E2] - 读取 chat 目标的 turn 数据源
  - 证据: `src/client/index.ts:14 import type + src/client/index.ts:84 ctx.uiConversation.binding(binding).target('chat')`
- `dsh-client-ui-conversation` [E1+E2] - 注册会话事件定义与输入槽位
  - 证据: `src/client/index.ts:6 import type + src/client/index.ts:63 ctx.uiConversation.events.register(planDefinition)`
- `dsh-client-ui-primitives` [编译依赖] - 复用 markdown 纯文本提取与基础控件
  - 证据: `src/client/index.ts:18 import + src/client/PlanCard.tsx:3 import`
- `dsh-client-ui-renderer` [编译依赖] - 渲染器槽位服务类型
  - 证据: `src/client/index.ts:11 import type`
- `dsh-client-ui-session` [编译依赖] - 会话标准 seat 类型
  - 证据: `src/client/index.ts:12 import type`
- `dsh-client-ui-sidebar-right` [E1+E2] - 打开计划预览资源
  - 证据: `src/client/PlanPreview.tsx:5 import + src/client/index.ts:74 ctx.sidebarRight.openResource(planAddress(…))`
- `dsh-client-ui-user-questions` [编译依赖] - 计划审阅与提问界面衔接
  - 证据: `src/client/PlanCard.tsx:10 import + src/client/index.ts:15 import type`
- `dsh-llm` [编译依赖] - 计划内容的模型类型
  - 证据: `src/client/PlanCard.tsx:8 import + src/client/plan.ts:2 import`
- `dsh-plan-mode` [编译依赖] - 复用 plan 投影键类型
  - 证据: `src/client/index.ts:10 import type`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/PlanCard.tsx:9 import + src/client/index.ts:4 import type`
- `dsh-tools` [编译依赖] - 工具调用标识类型
  - 证据: `src/client/plan-definition.ts:2 import`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
