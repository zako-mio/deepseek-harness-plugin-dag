# dsh-client-ui-message-feedback

- 包名: `@deepseek-ai/dsh-client-ui-message-feedback`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-message-feedback`

## 实现逻辑
每个 Session 惰性构造一个 FeedbackSurface，把消息级反馈对象层与对话框控制器绑在一起：消息目标走 remote.messageFeedback.rate，Session 目标走 remote.sessionFeedback.record（src/client/surface.ts:14-38）。apply 中向 conversation.chat.assistant-actions 注册 Like/Dislike 条目（src/client/index.ts:98）、向 conversation.input.overlay 注册反馈对话框（src/client/index.ts:115），并以 ctx.provide('feedbackUi') 暴露给其他插件打开草稿（src/client/index.ts:88）。connect/reset 时只重取已读过的非冷反馈（src/client/index.ts:91-95），并通过 commandUi.decorate 挂 /feedback 命令装饰（src/client/index.ts:136）。对话框状态机由 FeedbackDialogController 用快照 store 维护，成功关草稿并发确认 toast、失败保留草稿并发布错误码（src/client/dialog.ts:87-115）。

## Provides
- ctx.feedbackUi (打开指定 Session 反馈草稿的服务，不直接提交)
- conversation.chat.assistant-actions 条目 'feedback'（MessageFeedbackActions 赞/踩控件）
- conversation.input.overlay 条目 'feedback-dialog'（FeedbackDialog 对话框与确认/失败 toast）
- commandUi 的 /feedback 命令装饰（裸调用打开对话框，带参仍走 Host 命令）

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 调用 messageFeedback/sessionFeedback Remote 记录反馈
  - 证据: `src/client/controller.ts:11 import + src/client/surface.ts:27 ctx.remote.messageFeedback`
- `dsh-client-locale` [运行时依赖] - 注册 feedback 字典
  - 证据: `src/client/index.ts:20 import type + src/client/index.ts:69 ctx.locale.register(NS)`
- `dsh-client-ui-chat` [编译依赖] - 引入 ui-chat 的类型面（对话内容与标准来源）
  - 证据: `src/client/index.ts:23 import type {}`
- `dsh-client-ui-commands` [运行时依赖] - 挂 /feedback 命令装饰
  - 证据: `src/client/index.ts:18 import type + src/client/index.ts:136 scope.commandUi.decorate`
- `dsh-client-ui-conversation` [运行时依赖] - 使用 ui-conversation 声明的 assistant-actions 与 input.overlay 槽
  - 证据: `src/client/index.ts:16 import type + src/client/index.ts:98/index.ts:115 slots.inject`
- `dsh-client-ui-primitives` [编译依赖] - 复用 ui-primitives 的 Toast/Button 等控件
  - 证据: `src/client/FeedbackDialog.tsx:13 import + src/client/MessageFeedbackActions.tsx:13`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 槽注册表由 ui-renderer 提供
  - 证据: `src/client/index.ts:22 import type + src/client/index.ts:60 inject 'slots'`
- `dsh-client-ui-session` [编译依赖] - 引入 ui-session 的 Session 标准来源类型面
  - 证据: `src/client/index.ts:24 import type {}`
- `dsh-command-feedback` [编译依赖] - 反馈记录与分类的协议类型
  - 证据: `src/client/FeedbackDialog.tsx:14 import + src/client/surface.ts:15`
- `dsh-message-feedback` [编译依赖] - 消息反馈评分/视图协议类型
  - 证据: `src/client/MessageFeedbackActions.tsx:14 import + src/client/slots.ts:16`
- `dsh-session` [编译依赖] - 会话身份类型
  - 证据: `src/client/index.ts:12 import type { SessionId }`

## Dependents (下游被依赖)
- `dsh-session-log-export` - 探测 feedbackUi 可用性并在下拉菜单中提供反馈入口
