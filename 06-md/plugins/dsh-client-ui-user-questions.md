# dsh-client-ui-user-questions

- 包名: `@deepseek-ai/dsh-client-ui-user-questions`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-user-questions`

## 实现逻辑
承接 ask_user_question 的交互面板：apply（client/index.ts:368-403）先注册 question 字典，用 ctx.uiSession.registerPendingInteraction 发布待答卡片（:371-374），并通过 ctx.reflect.provide('userQuestionPanels', ...)（:376-380）向 ui-tool 暴露 reveal/review，使已结算的调用仍可从工具行回看。QuestionComposer 以 select 匹配 PendingQuestion 注入 conversation.composer 链（:382-393），question-reply 定义作为 conversation.chat.node 呈现迟到答复（:394-399），:400-402 再以 ctx.remote.$on('user-questions/request') 接管转发的问答瀑布。QuestionCards（:82-115）按 tool call id 复用同一张卡，卡片可脱离座位存活。

## Provides
- ctx.userQuestionPanels (待答面板 reveal/review，供 ui-tool 的 ask-question 行回看)
- 槽位贡献 conversation.composer（问题卡片）与 conversation.chat.node 的 'question-reply' 渲染器
- conversation.plan-review.actions 子槽

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 读取 agent 侧待答信箱状态
  - 证据: `src/client/index.ts:14 import type { InboxWireState } from '@deepseek-ai/dsh-agent/types'`
- `dsh-api-remotes` [E1+E2] - 转发问答请求与答复走 Remote Events 瀑布
  - 证据: `src/client/index.ts:15 import type {} from '@deepseek-ai/dsh-api-remotes/client'; src/client/index.ts:400 ctx.remote.$on('user-questions/request', ...)`
- `dsh-client-locale` [E1+E2] - 问答界面文案本地化
  - 证据: `src/client/index.ts:24 import type {} from '@deepseek-ai/dsh-client-locale/client'; src/client/index.ts:369 ctx.locale.register(NS, { zh, en })`
- `dsh-client-ui-chat` [编译依赖] - 回复视图复用 chat 侧会话节点类型
  - 证据: `src/client/index.ts:17 import type {} from '@deepseek-ai/dsh-client-ui-chat/client'; src/client/QuestionReplyView.tsx:2 import ... from '@deepseek-ai/dsh-client-ui-chat/client'`
- `dsh-client-ui-conversation` [E1+E2] - composer 链、会话节点注册表与 conversation.chat.node 槽由 ui-conversation 提供
  - 证据: `src/client/index.ts:18 import type { ComposerChainProps } from '@deepseek-ai/dsh-client-ui-conversation/client'; src/client/index.ts:394 ctx.uiConversation.events.register`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 服务由 renderer 提供
  - 证据: `src/client/index.ts:19 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-session` [E1+E2] - 待答卡片发布到会话级待交互注册表
  - 证据: `src/client/index.ts:20 import type { PendingInteractionPublisher } from '@deepseek-ai/dsh-client-ui-session/client'; src/client/index.ts:371 ctx.uiSession.registerPendingInteraction`
- `dsh-client-ui-tool` [编译依赖] - 实现 ui-tool 声明的 userQuestionPanels 服务契约，并复用其记录类型
  - 证据: `src/client/index.ts:25 import type { UserQuestionPanels, UserQuestionRecord } from '@deepseek-ai/dsh-client-ui-tool/client'`
- `dsh-llm` [编译依赖] - 卡片以 ToolCallId 品牌类型关联工具调用
  - 证据: `src/client/index.ts:26 import type { ToolCallId } from '@deepseek-ai/dsh-llm'; src/client/contract/slots.ts:4 import ... from '@deepseek-ai/dsh-llm/brand'`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/contract/slots.ts:5 import type { SessionId } from '@deepseek-ai/dsh-session/types'`
- `dsh-user-questions` [编译依赖] - 问题项、投影视图与待答类型由该包定义
  - 证据: `src/client/index.ts:22 import type { AskUserQuestionItem, PendingUserQuestion, UserQuestionProjectionView } from '@deepseek-ai/dsh-user-questions/types'`

## Dependents (下游被依赖)
- `dsh-client-ui-plan` - 计划审阅与提问界面衔接
