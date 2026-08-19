# dsh-client-ui-message-feedback

- 包名: `@deepseek-ai/dsh-client-ui-message-feedback`
- 分组: G27 会话交互UI
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-message-feedback`

## 为什么需要它（设计初衷）
逐条消息点赞/点踩反馈的浏览器插件，经 CAS 写 Host 侧对比版本。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-message-feedback/README.md

## 实现逻辑
Like/Dislike + 备注。每 Session 一个 MessageFeedbackController 作对象层（list 一次读取 seed 整份 transcript；mutation 经 messageFeedback Remote list/put/delete，host 持有 per-item CAS，version-conflict 由应答对账）；MessageFeedbackActions 注册进 conversation.chat.assistant-actions（id=feedback, order=10），inject 暴露 ensure/rate/toggle/clearNote/clear；connection/reset 时对非 cold 控制器 resync。

## Provides
- conversation.chat.assistant-actions id=feedback(MessageFeedbackActions)
- MessageFeedbackController（每 Session 对象层，status cold/loading/ready/error）

## Depends On (上游依赖)
- `dsh-api-remotes` [运行时依赖] - host messageFeedback Remote（dsh-message-feedback 域的生成端点）
  - 证据: `index.ts:12 type-only + index.ts:32 inject remote.messageFeedback + controller.ts:27-41 MessageFeedbackRemote(list/put/delete)`
- `dsh-client-connection` [运行时依赖] - 消息 id 类型与连接重置重同步
  - 证据: `controller.ts:12 MessageId,SessionId + index.ts:54-58 ctx.on('connection/reset') resync`
- `dsh-client-locale` [编译依赖] - feedback 命名空间字典
  - 证据: `index.ts:16 type-only + index.ts:40 locale.register`
- `dsh-client-runtime` [编译依赖] - 会话上下文与对象层挂载
  - 证据: `index.ts:10 ClientContext,SessionId`
- `dsh-client-ui-conversation` [编译依赖] - 消费 assistant-actions 座位声明
  - 证据: `index.ts:14 type-only + index.ts:60-77 注册 assistant-actions + package.json:38 dsh.client.inject`
- `dsh-client-ui-primitives` [编译依赖] - UI atoms
  - 证据: `package.json:54 peerDependencies（按钮/图标 atoms）`
- `dsh-client-ui-slots` [编译依赖] - props 类型与 slot 注册
  - 证据: `slots.ts: MessageFeedbackInjected + controller.ts:11 HostObservable`
- `dsh-message-feedback` [编译依赖] - feedback 域 wire 类型（item/rating/结果）
  - 证据: `controller.ts:13-19 dsh-message-feedback/types + package.json:57 peerDependencies`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
