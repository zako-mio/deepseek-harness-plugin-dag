# dsh-client-ui-trajectory

- 包名: `@deepseek-ai/dsh-client-ui-trajectory`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-trajectory`

## 实现逻辑
注册 trajectory 会话视图标签与轨迹 Definition：apply 为每个 SessionBinding 构造 trajectory 的 ObservableSnapshot 源并 ctx.uiSession.provide hooks 'trajectory'（src/client/index.ts:49-78），依次注册 assistant/compaction/message/request-header/tool 五类 Definition（src/client/index.ts:69-74），最后向 'conversation.view' 注册 id='trajectory' 的 TrajectoryView 并声明子槽 conversation.trajectory.images（src/client/index.ts:79-112）。视图组件用 client-store 引擎与 ui-primitives 渲染虚拟行、表格与时间线。

## Provides
- slot conversation.view id='trajectory' 的轨迹视图与子槽 conversation.trajectory.images
- conversation 节点 Definitions（assistant-stream/compaction/message/request-header/tool）注册进 uiConversation.events
- uiSession hooks 'trajectory'（TrajectorySnapshot 观察源）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 引入 agent 类型用于消息定义
  - 证据: `src/client/trajectory-message-definitions.ts:6 import type`
- `dsh-api-session-controller` [E1+E2] - 读取会话 binding 与分页 loadOlder
  - 证据: `src/client/index.ts:7 import + src/client/index.ts:89 ctx.sessions.binding`
- `dsh-client-locale` [E1+E2] - 注册 trajectory 字典
  - 证据: `src/client/index.ts:11 + src/client/index.ts:62 ctx.locale.register`
- `dsh-client-ui-conversation` [E1+E2] - 读取 trajectory target 并注册 conversation view Definition
  - 证据: `src/client/index.ts:14 import + src/client/index.ts:53 ctx.uiConversation.binding`
- `dsh-client-ui-primitives` [编译依赖] - 复用表格、时间线等展示原语
  - 证据: `src/client/TrajectoryTable.tsx:25 + TrajectoryTimeline.tsx:7`
- `dsh-client-ui-renderer` [编译依赖] - 拉入槽/渲染服务类型合并
  - 证据: `src/client/index.ts:15 import type`
- `dsh-client-ui-session` [E1+E2] - 向会话 UI 提供 trajectory hook
  - 证据: `src/client/index.ts:16 import type + src/client/index.ts:75 ctx.uiSession.provide`
- `dsh-llm` [编译依赖] - 投影 assistant 流事件与 LLM 类型
  - 证据: `src/client/trajectory-assistant-definition.ts:7-8 + src/client/trajectory-event-projection.ts:3`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/index.ts:9 SessionId`
- `dsh-tools` [编译依赖] - 工具类型用于工具轨迹定义
  - 证据: `src/client/trajectory-tool-definition.ts:6 import type`

## Dependents (下游被依赖)
- `dsh-client-ui-attachment` - 占据轨迹视图图片槽
