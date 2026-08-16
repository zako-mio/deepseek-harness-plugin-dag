# dsh-client-ui-trajectory

- 包名: `@deepseek-ai/dsh-client-ui-trajectory`
- 分组: G27 会话交互UI
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-trajectory`

## 实现逻辑
轨迹展示（纯消费者，无服务）。注册 conversation.view id=trajectory（order=10, label thunk）的 TrajectoryView（Table+Timeline+Toolbar，含 @tanstack/react-virtual 虚拟行、search index、duration store）；6 个轨迹 Definition（trajectory-inbox-next-step/message/assistant/tool/compaction/request-header）注册进 conversationEvents（target 'trajectory'），trajectory 专用 ConversationViewBuilder 注册进 conversationViews 组装 TrajectorySnapshot；loadOlder 走 session.loadOlder 分页。

## Provides
- conversation.view id=trajectory(TrajectoryView)
- 6 个 ConversationNodeDefinition（trajectory-*，target 'trajectory'）
- trajectory 目标 ConversationViewBuilder
- TrajectorySearchIndex/duration store（包内）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - agent/inbox/spliced 等事件类型
  - 证据: `trajectory-message-definitions.ts:9 dsh-agent/types + package.json:52 peerDependencies`
- `dsh-client-locale` [编译依赖] - 轨迹命名空间字典
  - 证据: `index.ts:8 type-only + index.ts:31 locale.register`
- `dsh-client-runtime` [编译依赖] - EventDefinition/View 注册表与会话分页
  - 证据: `index.ts:6 SessionId + trajectory-request-header-definition.ts:2-5 ConversationNodeDefinition + index.ts:56-60 session.loadOlder`
- `dsh-client-ui-conversation` [编译依赖] - 消费 conversation.view 视图环座位与 ConvViewProps
  - 证据: `index.ts:11 type-only + index.ts:43-64 注册 conversation.view + TrajectoryView.tsx:4 ConvViewProps + package.json:37 dsh.client.inject`
- `dsh-client-ui-primitives` [编译依赖] - UI atoms + markdown 纯文本提取
  - 证据: `TrajectoryTable.tsx:14, TrajectoryTimeline.tsx:7, TrajectoryToolbar.tsx:4, trajectory-preview.ts:3`
- `dsh-client-ui-slots` [编译依赖] - props 类型与 slot 注册
  - 证据: `TrajectoryView.tsx:5 InjectFace/PropsLocale + TrajectoryToolbar.tsx:3 TranslateNS`
- `dsh-tools` [编译依赖] - tool 调用轨迹事件类型
  - 证据: `trajectory-tool-definition.ts:6 dsh-tools/types + package.json:59`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
