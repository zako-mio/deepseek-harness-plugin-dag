# dsh-client-ui-trajectory

- 包名: `@deepseek-ai/dsh-client-ui-trajectory`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-trajectory`

## 实现逻辑
为会话贡献 trajectory 视图页与配套事件定义：client/index.ts:69-74 依次注册 message/request-header/assistant/tool/compaction 五组 ConversationNodeDefinition 并注册视图快照构建，:75-78 用 ctx.uiSession.provide 暴露 trajectory hook（resolve 时按 binding 建 WeakMap 缓存的 ObservableSnapshot），:79-112 把 TrajectoryView 注册进 conversation.view 槽（id 'trajectory'、order 10），并声明子槽 conversation.trajectory.images、注入 loadOlder/loadImage/setActualDuration 等回调。快照数据来自 ctx.uiConversation.binding(...).target('trajectory')（:53-58），assistant 定义复用 dsh-llm 的 assistantStreamFirstTokenTime 与 dsh-compaction/dsh-agent/dsh-tools 的类型做事件投影。

## Provides
- conversation.view 的 'trajectory' 视图页
- ctx.uiSession 的 trajectory hook 提供（按会话绑定发布快照）
- 槽位 conversation.trajectory.images
- 五组 ConversationNodeDefinition（message/request-header/assistant/tool/compaction）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 消息节点读取 agent 侧事件类型
  - 证据: `src/client/trajectory-message-definitions.ts:6 import type ... from '@deepseek-ai/dsh-agent/types'`
- `dsh-api-session-controller` [E1+E2] - 取会话绑定以读取快照并翻页加载更早历史
  - 证据: `src/client/index.ts:7 import type { SessionBinding } from '@deepseek-ai/dsh-api-session-controller/client'; src/client/index.ts:89 ctx.sessions.binding(sessionId)?.session`
- `dsh-client-locale` [E1+E2] - 视图页标签与表头文案本地化
  - 证据: `src/client/index.ts:11 import type {} from '@deepseek-ai/dsh-client-locale/client'; src/client/index.ts:62 ctx.locale.register(NS, { zh, en })`
- `dsh-client-ui-conversation` [E1+E2] - 会话视图槽、事件定义注册表与 trajectory 目标快照均由 ui-conversation 提供
  - 证据: `src/client/index.ts:14 import type {} from '@deepseek-ai/dsh-client-ui-conversation/client'; src/client/index.ts:93 ctx.uiConversation.binding(sessionId).target('trajectory')`
- `dsh-client-ui-primitives` [编译依赖] - 表格、时间轴与工具条控件复用共享原语
  - 证据: `src/client/TrajectoryTable.tsx:25 import ... from '@deepseek-ai/dsh-client-ui-primitives'`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 服务由 renderer 提供
  - 证据: `src/client/index.ts:15 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-session` [E1+E2] - 把 trajectory hook 发布为会话标准 props 的一部分
  - 证据: `src/client/index.ts:16 import type {} from '@deepseek-ai/dsh-client-ui-session/client'; src/client/index.ts:75-77 ctx.uiSession.provide`
- `dsh-llm` [编译依赖] - assistant 节点按 LLM 流块与首 token 时刻投影
  - 证据: `src/client/trajectory-assistant-definition.ts:7-8 import type { StreamChunk } from '@deepseek-ai/dsh-llm' + assistantStreamFirstTokenTime from '@deepseek-ai/dsh-llm/assistant-stream'`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/index.ts:9 import type { SessionId } from '@deepseek-ai/dsh-session/types'`
- `dsh-tools` [编译依赖] - 工具节点按工具结果元数据投影
  - 证据: `src/client/trajectory-tool-definition.ts:6 import type ... from '@deepseek-ai/dsh-tools/types'`

## Dependents (下游被依赖)
- `dsh-client-ui-attachment` - 占据轨迹视图图片槽
