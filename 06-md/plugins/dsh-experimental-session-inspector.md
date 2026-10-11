# dsh-experimental-session-inspector

- 包名: `@deepseek-ai/dsh-experimental-session-inspector`
- 分组: G13 实验特性
- 拓扑层: Layer 15
- 来源层: L3 其余
- 源码路径: `packages/experimental/session-inspector`

## 实现逻辑
纯客户端插件：注册一个会话作用域的右侧栏 tab（sidebarRightTabs + sidebar.right.pane.tab 槽位），并在其上注册 session-inspector-log 视图 (src/client/views/index.ts:22-79)。视图数据源复用既有模型——聊天侧用 ChatNodeModel 包装 uiConversation 绑定，日志侧用 SessionLogModel 包装会话事件源，按 SessionBinding 缓存并支持定位、跳转与「加载更早」 (src/client/views/index.ts:32-77)。插件的本地化字典在 apply 里注册，Host 侧入口为空实现，仅用于浏览器插件发现 (src/client/index.ts:16-19, src/index.ts:1-4)。

## Provides
- sidebarRightTabs 的 session-inspector-log tab 与 sidebar.right.pane.tab 槽位视图
- 会话检查器模型 (ChatNodeModel / SessionLogModel 及聊天节点定位与揭示)

## Depends On (上游依赖)
- `dsh-api-session-controller` [编译依赖] - 会话绑定类型与事件源由会话控制器提供
  - 证据: `src/client/views/index.ts:7 import type { SessionBinding } from '@deepseek-ai/dsh-api-session-controller/client' + src/client/views/session-log/chat-target.ts:3 import type {} + package.json:60 devDep`
- `dsh-client-locale` [E1+E2] - tab 标题与描述走客户端字典
  - 证据: `src/client/index.ts:4 import type {} from '@deepseek-ai/dsh-client-locale/client' + src/client/views/index.ts:26 ctx.locale.bind(NS) + src/client/index.ts:17 ctx.locale.register(NS, { en, zh }) + package.json:72 devDep`
- `dsh-client-ui-chat` [编译依赖] - 聊天节点模型与揭示目标解析建立在 chat 侧类型面之上
  - 证据: `src/client/views/chat-node/model.ts:3 import type {} from '@deepseek-ai/dsh-client-ui-chat/client' + src/client/views/chat-node/reveal-target.ts:4 import type {} + package.json:62 devDep`
- `dsh-client-ui-conversation` [E1+E2] - 聊天侧节点与分组来自会话 UI 的绑定与快照
  - 证据: `src/client/views/InspectorTable.tsx:5 import type {} from '@deepseek-ai/dsh-client-ui-conversation/client' + src/client/views/index.ts:40 ctx.uiConversation.binding(binding) + package.json:73 devDep`
- `dsh-client-ui-primitives` [编译依赖] - 表格与筛选器使用客户端基元组件
  - 证据: `src/client/views/InspectorTable.tsx:8 import { Tooltip } + src/client/views/TypeFilter.tsx:5 import + package.json:63 devDep`
- `dsh-client-ui-renderer` [编译依赖] - 槽位渲染由 renderer 承担，类型面需要其声明
  - 证据: `src/client/views/index.ts:4 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client' + package.json:74 devDep`
- `dsh-client-ui-session` [E1+E2] - 判断当前展示的会话以决定能否把检查器结果揭示到主聊天区
  - 证据: `src/client/views/index.ts:6 import type {} from '@deepseek-ai/dsh-client-ui-session/client' + src/client/views/index.ts:43 ctx.uiSession.adapter.current.getSnapshot() + package.json:65 devDep`
- `dsh-client-ui-sidebar-right` [E1+E2] - tab 的注册与右侧栏容器由该包提供
  - 证据: `src/client/index.ts:5 import type {} from '@deepseek-ai/dsh-client-ui-sidebar-right/client' + src/client/views/index.ts:28 ctx.sidebarRightTabs.register({ id, kind: 'session-inspector-log', ... }) + package.json:64 devDep`
- `dsh-llm` [编译依赖] - 会话日志行需要按 llm 的流式块与消息类型解释
  - 证据: `src/client/views/session-log/chat-target.ts:4 import type { StreamChunk } from '@deepseek-ai/dsh-llm' + src/client/views/session-log/model.ts:5 import from '@deepseek-ai/dsh-llm/assistant-stream' + package.json:67 devDep`
- `dsh-session` [E1+E2] - 视图以会话绑定为单位取得事件源
  - 证据: `src/client/views/chat-node/model.ts:8 import type { SessionId } from '@deepseek-ai/dsh-session/types' + src/client/views/index.ts:36 ctx.sessions.binding(sessionId) + package.json:66 devDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
