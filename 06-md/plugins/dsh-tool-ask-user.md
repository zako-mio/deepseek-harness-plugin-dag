# dsh-tool-ask-user

- 包名: `@deepseek-ai/dsh-tool-ask-user`
- 分组: G20 交互命令
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/interaction/tool-ask-user`

## 实现逻辑
以 defineTool 向 ctx.tools 注册模型可见的 ask_user_question 工具，声明 questions/options/multi_select 参数与 answers 输出 schema，render 直接把结果 JSON 化 (src/index.ts:38-97)。execute 把模型参数映射为 ctx.userQuestions.ask 请求，透传 exec.agent 与 exec.signal，并把答案裁剪为 {id,selected,custom} (src/index.ts:98-117)。Config.mode 选择第二种形态：timed 分支交给 registerTimedAskUser，额外声明 timeout 参数（-1 表示必须等待），调用 askTimed 并在前景窗口关闭时返回 pending 结果而非答案 (src/timed.ts:103-206)。

## Provides
- tools 注册：ask_user_question 工具（legacy 阻塞形态与 timed 前景等待形态）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 把调用 agent 作为问答请求的归属与作用域
  - 证据: `package.json:30 peerDep（src/index.ts:107 exec.agent 的 Agent 类型来源）`
- `dsh-tools` [E1+E2] - 工具必须注册进工具注册表才能被模型调用
  - 证据: `src/index.ts:10 import { defineTool } + src/index.ts:38 ctx.tools.register；src/timed.ts:6,106`
- `dsh-user-questions` [E1+E2] - 人机问答能力由 userQuestions seam 提供，工具只是其 Consumer
  - 证据: `src/index.ts:13 import '@deepseek-ai/dsh-user-questions' + src/index.ts:99 ctx.userQuestions.ask；src/timed.ts:197 askTimed`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
