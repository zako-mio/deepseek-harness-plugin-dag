# dsh-client-ui-user-questions

- 包名: `@deepseek-ai/dsh-client-ui-user-questions`
- 分组: G27 会话交互UI
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-user-questions`

## 实现逻辑
用户提问 UI。QuestionComposer 以 selector selectQuestion（interactions 中 kind==='question' 的 PendingWait 载体）注册进 conversation.composer 链；一个条目两种形态：请求带 plan-review 呈现意图时渲染 PlanReviewPanel（approve/decline/discuss 决策卡），否则走通用提问流程（pager/选项/自定义/跳过）；PendingQuestion 域 face 封装 answer/cancel（wait.respond 编码 wire 应答）；零业务 face，数据/动词全部随 carrier。

## Provides
- conversation.composer 链条目(QuestionComposer)
- PlanReviewPanel（plan-review 意图接管）
- PendingQuestion 域 face（answer/cancel）

## Depends On (上游依赖)
- `dsh-api-remotes` [编译依赖] - 提问应答负载类型
  - 证据: `contract/slots.ts:14 QuestionResponsePayload + package.json:57 peerDependencies`
- `dsh-client-locale` [编译依赖] - question 命名空间字典
  - 证据: `index.ts:18 type-only + index.ts:54 locale.register`
- `dsh-client-runtime` [编译依赖] - PendingWait 载体（question 等待帧）
  - 证据: `contract/slots.ts:13 PendingWait 类型`
- `dsh-client-ui-conversation` [编译依赖] - 消费 composer 链座位与 ComposerChainProps（interactions 载体）
  - 证据: `index.ts:16 ComposerChainProps + contract/slots.ts:12 type-only + index.ts:56-59 注册 conversation.composer + package.json:36 dsh.client.inject`
- `dsh-client-ui-primitives` [编译依赖] - UI atoms
  - 证据: `QuestionComposer.tsx:3-6 Button/MarkdownText/图标 + PlanReviewPanel.tsx:17`
- `dsh-client-ui-slots` [编译依赖] - props 类型与 slot 注册
  - 证据: `contract/slots.ts:9 PropsLocale/PropsRuntime`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
