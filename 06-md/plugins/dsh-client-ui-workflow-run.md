# dsh-client-ui-workflow-run

- 包名: `@deepseek-ai/dsh-client-ui-workflow-run`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-workflow-run`

## 实现逻辑
把持久化的 workflow 运行渲染为会话节点：client/index.ts:27 向 ctx.uiConversation.events 注册 workflowRunDefinition（workflow-definition.ts 内按 dsh-workflow 与 dsh-tool-workflow 的事件类型做 match/update 投影），:29-36 把 WorkflowRunPanel 注册为键控 conversation.chat.node（key 'workflow-run'），并在 inject 中提供 openSession 回调（走 ctx.uiWorkspace.openSession）。字典经 ctx.locale.register(NS, { zh, en }) 注册（:28）。

## Provides
- conversation.chat.node 的 'workflow-run' 渲染器
- workflowRunDefinition（workflow 运行事件的会话节点定义）

## Depends On (上游依赖)
- `dsh-api-session-controller` [E1+E2] - 会话目标与绑定类型由会话控制器定义
  - 证据: `src/client/WorkflowRunPanel.tsx:10 import type { SessionTarget } from '@deepseek-ai/dsh-api-session-controller/client'; src/client/index.ts:4 import type {} from ...`
- `dsh-client-locale` [E1+E2] - 运行状态与面板文案本地化
  - 证据: `src/client/index.ts:5 import type {} from '@deepseek-ai/dsh-client-locale/client'; src/client/index.ts:28 ctx.locale.register(NS, { zh, en })`
- `dsh-client-ui-chat` [编译依赖] - 节点定义返回 chat 侧会话视图节点类型
  - 证据: `src/client/index.ts:6 import type {} from '@deepseek-ai/dsh-client-ui-chat/client'; src/client/workflow-definition.ts:4 import type { ChatConversationViewNode }`
- `dsh-client-ui-conversation` [E1+E2] - 节点定义注册表与 conversation.chat.node 槽由 ui-conversation 提供
  - 证据: `src/client/index.ts:7 import type {} from '@deepseek-ai/dsh-client-ui-conversation/client'; src/client/index.ts:27 ctx.uiConversation.events.register(workflowRunDefinition)`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 服务由 renderer 提供
  - 证据: `src/client/index.ts:8 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-session` [编译依赖] - 拉入 uiSession 合并以按会话渲染面板
  - 证据: `src/client/WorkflowRunPanel.tsx:13 import type {} from '@deepseek-ai/dsh-client-ui-session/client'`
- `dsh-client-ui-workspace` [E1+E2] - 面板中打开成员会话走工作区导航服务
  - 证据: `src/client/index.ts:10 import type {} from '@deepseek-ai/dsh-client-ui-workspace/client'; src/client/index.ts:34 ctx.uiWorkspace.openSession(target)`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/workflow-definition.ts:5 import type { SessionId } from '@deepseek-ai/dsh-session/types'`
- `dsh-tool-workflow` [编译依赖] - 读取工具侧 workflow 代理起止事件数据
  - 证据: `src/client/workflow-definition.ts:8 import type { ToolWorkflowAgentEndData, ToolWorkflowAgentStartData } from '@deepseek-ai/dsh-tool-workflow/types'`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
