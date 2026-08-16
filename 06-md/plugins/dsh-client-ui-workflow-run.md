# dsh-client-ui-workflow-run

- 包名: `@deepseek-ai/dsh-client-ui-workflow-run`
- 分组: G27 会话交互UI
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-workflow-run`

## 实现逻辑
持久化工作流生命周期的独立 Chat 节点。workflowRunDefinition（target 'chat'，match tool-workflow/run-start|agent-start|agent-end|run-end）注册进 ConversationEventRegistry；WorkflowRunPanel 以 keyed 'workflow-run' 注册进 conversation.chat.node，渲染 phase/member 状态（running/completed/failed/cancelled/interrupted），inject 注入 openSession 跳转子会话；将 WorkflowRunChatData 合入 ui-conversation 的 ChatNodeDataMap。

## Provides
- conversation.chat.node keyed 'workflow-run' 渲染器(WorkflowRunPanel)
- ConversationNodeDefinition 'workflow-run'（tool-workflow/* 事件状态机）
- ChatNodeDataMap 'workflow-run' 合并

## Depends On (上游依赖)
- `dsh-client-locale` [编译依赖] - workflowRun 命名空间字典
  - 证据: `index.ts:4 type-only + index.ts:23 locale.register`
- `dsh-client-runtime` [编译依赖] - EventDefinition/View 注册表与会话快照类型
  - 证据: `index.ts:3 ClientContext + workflow-definition.ts:1-4 ConversationNodeDefinition + WorkflowRunPanel.tsx:7 SessionId`
- `dsh-client-ui-conversation` [编译依赖] - 消费 conversation.chat.node 座位与 ChatNodeDataMap 合并面
  - 证据: `index.ts:5 type-only + workflow-definition.ts:37-42 declare ChatNodeDataMap merge + package.json:59 peerDependencies`
- `dsh-client-ui-primitives` [编译依赖] - UI atoms
  - 证据: `WorkflowRunPanel.tsx:2-5 DisclosureRow,StateDot 等`
- `dsh-client-ui-slots` [编译依赖] - props 类型与 slot 注册 API
  - 证据: `WorkflowRunPanel.tsx:6 PropsLocale/PropsRuntime`
- `dsh-session` [编译依赖] - 会话 id 类型契约
  - 证据: `workflow-definition.ts:5 SessionId from dsh-session/types + package.json:63`
- `dsh-session-projection` [运行时依赖] - 会话数据源
  - 证据: `WorkflowRunPanel.tsx 经 PropsRuntime 读会话快照（workflow-run 数据在 conversation snapshot）`
- `dsh-tool-workflow` [编译依赖] - tool-workflow 事件负载类型
  - 证据: `workflow-definition.ts:6-8 ToolWorkflowAgentStartData/AgentEndData + package.json:64`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
