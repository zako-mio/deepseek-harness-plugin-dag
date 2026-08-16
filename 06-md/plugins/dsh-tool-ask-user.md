# dsh-tool-ask-user

- 包名: `@deepseek-ai/dsh-tool-ask-user`
- 分组: G36 Hooks工具扩展
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/interaction/tool-ask-user`

## 实现逻辑
注册 ask_user_question 工具 (src/index.ts:20-100)，inject ['tools','userQuestions'] (:14)；execute 转发 ctx.userQuestions.ask (:81)，将 id/question/header/options/multiSelect 映射后传入 (:82-91)，answers 归一返回 (:92-98)；output schema+render JSON 文本 (:58-79)；name 'tool-ask-user' (:13)。

## Provides
- tool: ask_user_question

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - agent 上下文透传
  - 证据: `package.json:35 peerDep + src/index.ts:9 import type Context 无关（agent 类型经 dsh-tools exec 传递）；E2: :89 exec.agent 传入 ask`
- `dsh-tools` [E1+E2] - 工具注册
  - 证据: `package.json:37 peerDep + src/index.ts:10 import defineTool；E2: :14 inject=['tools','userQuestions']、:20 ctx.tools.register`
- `dsh-user-questions` [E1+E2] - 用户提问能力 seam
  - 证据: `package.json:38 peerDep + src/index.ts:11 import '@deepseek-ai/dsh-user-questions'（side-effect merge）；E2: :14 inject、:81 ctx.userQuestions.ask`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
