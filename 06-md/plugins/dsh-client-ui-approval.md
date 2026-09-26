# dsh-client-ui-approval

- 包名: `@deepseek-ai/dsh-client-ui-approval`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-approval`

## 实现逻辑
浏览器半实现 Remote Event 瀑布的一环：apply 取 ctx.uiSession.registerPendingInteraction 发布器 (src/client/index.ts:88-90)，向 'conversation.composer' 以 priority 1 注册接管面板并声明子槽 'conversation.approval.detail' (src/client/index.ts:91-103)。对 ctx.remote.$on('approval/request') 的每个请求构造 PendingApproval，把 sessionId 与 callId/reason/signal 投影成可回答项；未回答时用 delegate() 抛内部拒绝以回到瀑布 next() 继续 (src/client/index.ts:36-70, 104-106)。另在 shortcuts 注册固定 Enter=允许、Esc=拒绝，并注册 approval 字典 (src/client/index.ts:78-87)。宿主半为空 apply (src/index.ts:4)。

## Provides
- slot: conversation.composer (priority 1 的审批接管面板，选择函数匹配 PendingApproval)
- 子槽声明: conversation.approval.detail (kind single, scope session)
- ctx.uiSession 待决交互类型 approval 的 PendingApproval 呈现与回答生命周期 (answer/delegate/abort/isDelegation)
- Locale 命名空间 approval (zh/en)
- 快捷键 approval.allow (Enter) 与 approval.reject (Esc)
- 导出 PendingApproval 类与 ApprovalComposerProps/ApprovalDecision/ApprovalDetailOwnerProps 类型 (供 ui-chat 的 ApprovalCommand 以 type-only 消费)

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 订阅审批请求瀑布
  - 证据: `src/client/index.ts:3 ctx.remote merge + src/client/index.ts:104 ctx.remote.$on('approval/request')`
- `dsh-api-session-controller` [运行时依赖] - 把 Remote 监听者 owner 解析成会话 id
  - 证据: `src/client/index.ts:4 + src/client/index.ts:43 ctx.sessions.scopeOf(owner)`
- `dsh-client-locale` [E1+E2] - 注册 approval 字典与 resolveText
  - 证据: `src/client/index.ts:9 + src/client/index.ts:78 ctx.locale.register(NS)`
- `dsh-client-shortcuts` [E1+E2] - 注册 Enter/Esc 固定审批快捷键
  - 证据: `src/client/index.ts:10 ShortcutCommandId + src/client/index.ts:81-86 scope.shortcuts.registerFixed`
- `dsh-client-ui-conversation` [E1+E2] - 占用会话编辑器槽位以接管审批
  - 证据: `src/client/index.ts:5 ComposerChainProps + src/client/index.ts:91 ctx.slots.inject('conversation.composer')`
- `dsh-client-ui-primitives` [编译依赖] - 审批面板复用基础组件
  - 证据: `src/client/ApprovalPanel.tsx:3 import @deepseek-ai/dsh-client-ui-primitives`
- `dsh-client-ui-renderer` [编译依赖] - 引入 slots 服务声明
  - 证据: `src/client/index.ts:6 import @deepseek-ai/dsh-client-ui-renderer/client`
- `dsh-client-ui-session` [E1+E2] - 发布待决交互供会话 UI 呈现
  - 证据: `src/client/index.ts:7 PendingInteractionPublisher + src/client/index.ts:88 ctx.uiSession.registerPendingInteraction`
- `dsh-llm` [编译依赖] - 关联工具调用标识类型
  - 证据: `src/client/contract/slots.ts:2 import ToolCallId from @deepseek-ai/dsh-llm`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/contract/slots.ts:3 import SessionId from @deepseek-ai/dsh-session/types`

## Dependents (下游被依赖)
- `dsh-client-ui-chat` - 消费 conversation.approval.detail 槽的 owner 契约
