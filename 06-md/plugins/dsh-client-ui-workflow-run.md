# dsh-client-ui-workflow-run

- 包名: `@deepseek-ai/dsh-client-ui-workflow-run`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-workflow-run`

## 实现逻辑
注册 durable workflow-run 会话节点：apply 用 ctx.uiConversation.events.register 挂载 workflowRunDefinition（src/client/index.ts:27），并向 'conversation.chat.node' 注册 key='workflow-run' 的 WorkflowRunPanel，注入 openSession 用于打开成员子会话（src/client/index.ts:29-36）。workflow-definition.ts 从工具 workflow agent start/end 事件折叠出 phase/member 状态并产出 keyed Chat 数据（src/client/workflow-definition.ts:41-60）。

## Provides
- ConversationNodeDefinition 'workflow-run'（注册进 uiConversation.events）
- slot conversation.chat.node key='workflow-run' 的 WorkflowRunPanel 渲染
- ChatNodeDataMap 'workflow-run' 数据契约

## Depends On (上游依赖)
- `dsh-api-session-controller` [编译依赖] - 读取会话列表状态与导航目标类型
  - 证据: `src/client/WorkflowRunPanel.tsx:10 SessionListState/SessionTarget`
- `dsh-client-locale` [E1+E2] - 注册 workflowRun 字典
  - 证据: `src/client/index.ts:5 + src/client/index.ts:28 ctx.locale.register`
- `dsh-client-ui-chat` [编译依赖] - 引入 keyed Chat 节点渲染契约
  - 证据: `src/client/index.ts:6 + src/client/workflow-definition.ts:4`
- `dsh-client-ui-conversation` [E1+E2] - 注册会话节点定义并读取 ConversationNodeContext
  - 证据: `src/client/index.ts:7 import + src/client/index.ts:27 ctx.uiConversation.events.register`
- `dsh-client-ui-primitives` [编译依赖] - 复用折叠行与状态点原语
  - 证据: `src/client/WorkflowRunPanel.tsx:9 DisclosureRow/StateDot`
- `dsh-client-ui-renderer` [编译依赖] - 拉入槽/渲染服务类型合并
  - 证据: `src/client/index.ts:8 import type`
- `dsh-client-ui-session` [编译依赖] - 引入会话状态快照与 UI 服务类型
  - 证据: `src/client/WorkflowRunPanel.tsx:13 + src/client/index.ts:9`
- `dsh-client-ui-workspace` [E1+E2] - 从工作流面板导航到成员会话
  - 证据: `src/client/index.ts:10 import type + src/client/index.ts:34 ctx.uiWorkspace.openSession`
- `dsh-session` [编译依赖] - 成员子会话标识类型
  - 证据: `src/client/workflow-definition.ts:5 SessionId`
- `dsh-tool-workflow` [编译依赖] - 解析工具侧工作流成员事件数据
  - 证据: `src/client/workflow-definition.ts:8 ToolWorkflowAgentStartData/EndData`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
