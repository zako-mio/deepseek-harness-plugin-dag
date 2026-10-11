# dsh-client-ui-tool

- 包名: `@deepseek-ai/dsh-client-ui-tool`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-tool`

## 实现逻辑
工具调用 UI 的总装配点：apply.ts:34-42 把 ToolCallTree 注册为键控 conversation.chat.node（key 'tool-call'）并声明子槽 tool.call.toolview，:44-52 再以 ctx.plugin 装载 bash/read/read-image/file-mutation/search/web/todo/details/ask-question 九个内建 toolview。contract/slots.ts:14-45 声明两个槽：tool.call.toolview（按线上工具名键控、未占用键回落通用行）与 tool.call.images（单例图片画廊，由附件插件填充）；:133-138 声明可选服务 ctx.userQuestionPanels，apply.ts:29-33 用 hostInfo hook 暴露 Host 事实供 POSIX `~` 路径显示。models/ 与 toolviews/ 下的模型与行组件各自从原始 call/result 事件派生展示数据。

## Provides
- 槽位 tool.call.toolview（按线上工具名键控的原子工具视图）
- 槽位 tool.call.images（单例图片画廊，供附件呈现插件填充）
- conversation.chat.node 的 'tool-call' 渲染器
- 内建原子视图：bash/read/read-image/file-mutation/search/web/todo/details/ask-question

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 问题行的待答状态类型来自 agent
  - 证据: `src/client/tool/toolviews/ask-question-row.tsx:4 import type ... from '@deepseek-ai/dsh-agent/types'`
- `dsh-api-remotes` [E1+E2] - Host 家目录事实用于路径摘要显示
  - 证据: `src/client/contract/slots.ts:5 import type { RemoteHostFacts } from '@deepseek-ai/dsh-api-remotes/client'; src/client/apply.ts:30 ctx.remote.$host`
- `dsh-client-locale` [E1+E2] - 工具行文案走 locale 字典（复用 conversation 命名空间）
  - 证据: `src/client/contract/slots.ts:12 import type {} from '@deepseek-ai/dsh-client-locale/client'; src/client/apply.ts:10 CONVERSATION_NS`
- `dsh-client-ui-chat` [编译依赖] - 工具视图消费 chat 侧的工具调用阶段/结果节点类型
  - 证据: `src/client/tool/ToolCallTree.tsx:3 import ... from '@deepseek-ai/dsh-client-ui-chat/client'; src/client/tool/components/ToolRow.tsx:9`
- `dsh-client-ui-conversation` [编译依赖] - conversation.chat.node 槽与图片加载契约由 ui-conversation 声明
  - 证据: `src/client/contract/slots.ts:10 import type { MessageImageLoader, MessageImageSource } from '@deepseek-ai/dsh-client-ui-conversation/client'; src/client/tool/components/ToolRow.tsx:10`
- `dsh-client-ui-primitives` [编译依赖] - 卡片、标签与图标复用共享原语
  - 证据: `src/client/tool/models/diff-card-model.ts:2 import ... from '@deepseek-ai/dsh-client-ui-primitives'`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 服务由 renderer 提供
  - 证据: `src/client/apply.ts:7 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-session` [E1+E2] - 拉入 uiSession/uiConversation 合并以读取会话作用域数据
  - 证据: `src/client/apply.ts:8 import type {} from '@deepseek-ai/dsh-client-ui-session/client'; src/client/tool/models/todo-history.ts:86-88 ctx.uiConversation/uiSession 读取`
- `dsh-spill-policy` [编译依赖] - 被 spill 的截断结果在卡片上显示统一提示
  - 证据: `src/client/tool/models/inspection-details-model.ts:3 import ... from '@deepseek-ai/dsh-spill-policy/notice'`
- `dsh-tools` [编译依赖] - todo 历史重建依赖工具结果类型
  - 证据: `src/client/tool/models/todo-history.ts:2 import type ... from '@deepseek-ai/dsh-tools/types'`
- `dsh-user-questions` [编译依赖] - ask-question 行读问题项与答案的类型
  - 证据: `src/client/contract/slots.ts:11 import type { AskUserQuestionAnswerItem, AskUserQuestionItem } from '@deepseek-ai/dsh-user-questions/types'`

## Dependents (下游被依赖)
- `dsh-client-ui-attachment` - 占据工具调用图片槽
- `dsh-client-ui-cordis` - 复用工具卡片行组件契约与 toolview 注入协议，渲染 cordis_* 工具调用
- `dsh-client-ui-deliverables` - 工具视图基础类型
- `dsh-client-ui-schedule` - 创建卡复用 ui-tool 的 Tool 调用视图 props 类型，但不在 tool.call.toolview 注册条目
- `dsh-client-ui-skill` - tool.call.toolview 槽由 ui-tool 声明，skill 行按其视图契约实现
- `dsh-client-ui-user-questions` - 实现 ui-tool 声明的 userQuestionPanels 服务契约，并复用其记录类型
