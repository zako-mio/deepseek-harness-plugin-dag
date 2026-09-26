# dsh-client-ui-user-questions

- 包名: `@deepseek-ai/dsh-client-ui-user-questions`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-user-questions`

## 实现逻辑
把 QuestionComposer 注册为 conversation.composer 链上的 selector 路由入口：选择器把 owner 货币收窄为 PendingQuestion 载体，并声明 conversation.plan-review.actions 子槽（src/client/index.ts:94-104）。用 ctx.uiSession.registerPendingInteraction 发布待处理交互（plan-review 优先级 2、普通问题 1）（src/client/index.ts:91-93），并通过 ctx.remote.$on('user-questions/request') 挂 waterfall 监听，按作答/取消/委托结算 PendingQuestion（src/client/index.ts:54-80,105-107）。

## Provides
- slot conversation.composer 的 question/plan-review 呈现与子槽 conversation.plan-review.actions
- SessionPendingInteractionMap 'question' 发布器（ctx.uiSession.registerPendingInteraction）
- remote 事件 user-questions/request 的客户端 waterfall 监听器

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 订阅 Host 的 user-questions/request waterfall
  - 证据: `src/client/index.ts:16 import + src/client/index.ts:105 ctx.remote.$on`
- `dsh-api-session-controller` [E1+E2] - 把请求归属到具体会话作用域
  - 证据: `src/client/index.ts:17 import + src/client/index.ts:61 sessions.scopeOf`
- `dsh-client-locale` [E1+E2] - 注册 question 字典
  - 证据: `src/client/index.ts:23 + src/client/index.ts:89 ctx.locale.register`
- `dsh-client-ui-conversation` [编译依赖] - 接入 conversation.composer 链与 matched 货币
  - 证据: `src/client/index.ts:18 ComposerChainProps`
- `dsh-client-ui-renderer` [编译依赖] - 拉入槽/渲染服务类型合并
  - 证据: `src/client/index.ts:19 import type`
- `dsh-client-ui-session` [E1+E2] - 发布待处理问题交互并供 Session UI 消费
  - 证据: `src/client/index.ts:20 import type + src/client/index.ts:91 ctx.uiSession.registerPendingInteraction`
- `dsh-llm` [编译依赖] - 引入品牌化 ToolCallId 用于重开计划
  - 证据: `src/client/contract/slots.ts:4 ToolCallId`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/contract/slots.ts:5 SessionId`
- `dsh-user-questions` [编译依赖] - 复用 Host 侧问题结构与答案类型
  - 证据: `src/client/contract/slots.ts:8 AskUserQuestionItem/Answer`

## Dependents (下游被依赖)
- `dsh-client-ui-plan` - 计划卡复用 user-questions 的类型面/交互
