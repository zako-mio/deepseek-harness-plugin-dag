# dsh-user-questions

- 包名: `@deepseek-ai/dsh-user-questions`
- 分组: G08 会话展示
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/interaction/user-questions`

## 实现逻辑
用户提问能力接缝：UserQuestionService(ctx.userQuestions) 维护单一活动 UI provider 槽。ask(request) 是唯一出口：前置校验(signal 中止/空问题/agent 必须精确 live root/plan-review intent 标签合法)，然后委托 provider.ask。

## Provides
- ctx.userQuestions(ask/registerProvider)
- UserQuestionProvider 单槽契约
- UserQuestionError 错误面
- wire-safe 类型出口

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 调用者身份边界
  - 证据: `packages/interaction/user-questions/src/index.ts:11,101-112`
- `dsh-llm` [编译依赖] - HarnessError 基类
  - 证据: `packages/interaction/user-questions/src/index.ts:12`

## Dependents (下游被依赖)
- `dsh-host-apiproxy` - AskUserQuestion* 类型
- `dsh-plan-mode` - exit 前计划评审
- `dsh-tool-ask-user` - 用户提问能力 seam
