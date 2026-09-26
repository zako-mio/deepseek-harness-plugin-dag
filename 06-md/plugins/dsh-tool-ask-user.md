# dsh-tool-ask-user

- 包名: `@deepseek-ai/dsh-tool-ask-user`
- 分组: G21 交互命令
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/interaction/tool-ask-user`

## 实现逻辑
作为 ctx.userQuestions 的模型侧 Consumer，用 defineTool 注册 ask_user_question 工具（参数为 questions 数组、输出为 answers），execute 调 ctx.userQuestions.ask 暂停直到 UI 作答，再把答案作为普通工具结果回灌模型循环（src/index.ts:18-99）。工具 schema 与渲染输出均为纯模型可见文本（src/index.ts:19-78）。

## Provides
- ask_user_question 模型工具 (向 ctx.userQuestions 发起人类问答，src/index.ts:19-99)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 工具执行携带的 agent 身份
  - 证据: `package.json:30 peerDep（execute 的 exec.agent 来自工具执行上下文，src/index.ts:88）`
- `dsh-tools` [E1+E2] - 注册模型可用工具
  - 证据: `package.json:31 peerDep + src/index.ts:10 import defineTool; src/index.ts:19 ctx.tools.register`
- `dsh-user-questions` [E1+E2] - 调用人类问答能力 seam
  - 证据: `package.json:32 peerDep + src/index.ts:11 side-effect type import; src/index.ts:80 ctx.userQuestions.ask`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
