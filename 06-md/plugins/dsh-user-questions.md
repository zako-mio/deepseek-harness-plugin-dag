# dsh-user-questions

- 包名: `@deepseek-ai/dsh-user-questions`
- 分组: G20 交互命令
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/interaction/user-questions`

## 实现逻辑
用户问答 seam：UserQuestionService 经 Agent 作用域的 user-questions/request waterfall 寻找 answerer，校验问题非空、presentation intent 的 approve 标签与 detail 合法，并把「调用方必须是存活 runtime root」作为人机交互前提（被委派的子 agent 直接拒绝并给出结构化错误码）(src/index.ts:287-339, src/index.ts:131-144)。askTimed 建立 TimedQuestionWait 前景等待，客户端认领期间由 Host 计时，超时映射为 pending 结果，取消则还原为 ASK_ABORTED (src/index.ts:234-269, src/timed-wait.ts:33-82)。迟到的回答经 agent.steer 以 user-question-reply 来源的用户消息回流，同一问题只允许一条排队回复，队列随 inbox 认领/丢弃与 turn 结束清理 (src/index.ts:164-206, src/index.ts:95-129)。projection.ts 把工具调用、结果与迟到答复折叠为 active/settled 三态视图供所有客户端读取 (src/projection.ts:235-331)。

## Provides
- ctx.userQuestions (UserQuestionService：提问、定时前景等待、迟到回答回流)
- Cordis 事件 user-questions/request（Agent 作用域 waterfall）
- Session 投影 userQuestions（active/continued 与 settled 视图）
- 消息来源 user-question-reply（迟到答复的持久归属）
- TIMED_WAIT_PARAMETER / isTimedAskUserQuestionSchema（timed 工具与投影共用的判定）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 以 Agent 注册表判定调用方是否为可交互的存活 runtime root
  - 证据: `src/index.ts:11,16 import type { Agent } + src/index.ts:132 ctx.get('agents') 校验存活 root`
- `dsh-llm` [编译依赖] - 构造回流用户消息并使用 LLM 的 brand 与内容块类型
  - 证据: `src/index.ts:12 import { createUserMessage, HarnessError } + src/projection.ts:8 import { ToolCallId }`
- `dsh-session` [编译依赖] - 投影状态以会话日志偏移为继承边界
  - 证据: `src/index.ts:13 import type { Session } + src/projection.ts:3 SessionLogOffset`
- `dsh-session-projection` [E1+E2] - 注册 userQuestions 投影并读取 active 问题
  - 证据: `src/index.ts:17 import type {} + src/index.ts:86-87 ctx.inject(['sessionProjections']) 后 register`
- `dsh-tools` [编译依赖] - 投影读取 tool/call、tool/result 事件需要工具事件类型声明合并
  - 证据: `src/projection.ts:7 import type {} from '@deepseek-ai/dsh-tools/types'`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 把该业务包的 /remote 命名空间装配进 Client
- `dsh-client-ui-tool` - ask-question 行读问题项与答案的类型
- `dsh-client-ui-user-questions` - 问题项、投影视图与待答类型由该包定义
- `dsh-experimental-claude-code-mods` - $.ui.ask 与 session.start 的 isInteractive 判定依赖用户提问服务
- `dsh-plan-mode` - exit_plan_mode 经用户问答通道发起计划评审，并区分「被驳回」与失败
- `dsh-tool-ask-user` - 人机问答能力由 userQuestions seam 提供，工具只是其 Consumer
