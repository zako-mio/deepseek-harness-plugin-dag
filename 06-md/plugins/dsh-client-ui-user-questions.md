# dsh-client-ui-user-questions

- 包名: `@deepseek-ai/dsh-client-ui-user-questions`
- 分组: G27 会话交互UI
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-user-questions`

## 为什么需要它（设计初衷）
Web 提问功能：渲染 dsh-tool-ask-user 的问题为结构化表单（单选/多选/自定义），支持 plan-review 意图的审批卡片。RC7 增加卡片折叠与本地草稿，提升多问题场景的可用性。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/client/ui-user-questions/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness

## 实现逻辑
用户提问 UI。QuestionComposer 以 selector selectQuestion（interactions 中 kind==='question' 的 PendingWait 载体）注册进 conversation.composer 链；一个条目两种形态：请求带 plan-review 呈现意图时渲染 PlanReviewPanel（approve/decline/discuss 决策卡），否则走通用提问流程（pager/选项/自定义/跳过）；PendingQuestion 域 face 封装 answer/cancel（wait.respond 编码 wire 应答）；零业务 face，数据/动词全部随 carrier。RC7：提问卡片支持折叠(header strip 折叠时仅剩标题行，展开按钮不抢占焦点)与本地草稿(DraftAnswer[] 按 questions 1:1 镜像，切换/展开时输入保留)。

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
