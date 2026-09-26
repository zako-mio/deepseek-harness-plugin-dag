# dsh-client-ui-plan

- 包名: `@deepseek-ai/dsh-client-ui-plan`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 17
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-plan`

## 实现逻辑
apply 先注册 planDefinition 为会话节点定义、注册 plan 资源 provider、再向 ctx.sidebarRightTabs 注册 plan/preview 页型（src/client/index.ts:63-71），使提交的计划可从日志重建为右侧预览。随后注册五个界面面：Turn 末尾的 PlanCards（src/client/index.ts:79）、review 动作（index.ts:97）、侧栏 pane.tab/title（index.ts:109/112）与 composer 的 PlanChip（index.ts:116）。计划身份由 submittedPlan 从 tool/call 或 PTC 事件解析出 callId 与首行标题（src/client/plan.ts:33-58），再用 dsh-resource://plan/... 地址编解码做持久化（src/client/plan.ts:65-107）；退出计划模式走 remote.commands.execute('/plan off')（src/client/index.ts:116-124）。

## Provides
- conversation.chat.turnTail 条目 PlanCards（Turn 末尾持久计划卡，读 'submitted-plan' Turn 数据源）
- conversation.plan-review.actions 条目 PlanReviewOpen（计划评审打开动作 + 评审窗口 store）
- conversation.input.plan 座位 PlanChip（composer 计划模式指示与退出）
- sidebar.right.pane.tab / sidebar.right.pane.tab.title 的 plan 预览页与标题
- ctx.uiConversation 的 plan 会话节点定义 + ctx.resources 的 plan 资源 provider + ctx.sidebarRightTabs 的 plan 页型

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - ctx.remote 与 Remote 转发事件面
  - 证据: `src/client/index.ts:2 import + src/client/index.ts:64 ctx.remote.session`
- `dsh-api-session-controller` [E1+E2] - Session 地址与投影类型
  - 证据: `src/client/index.ts:13 import remote + src/client/plan-resource.ts:3 import types`
- `dsh-client-locale` [运行时依赖] - 注册 plan 文案
  - 证据: `src/client/index.ts:8 import type + src/client/index.ts:59 ctx.locale.register(NS)`
- `dsh-client-resources` [E1+E2] - 注册计划资源 provider
  - 证据: `src/client/index.ts:17 import type + src/client/index.ts:64 ctx.resources.register`
- `dsh-client-ui-chat` [E1+E2] - Chat 节点类型与标准来源面
  - 证据: `src/client/index.ts:14 import type {} + src/client/plan-definition.ts:3 import type { ChatNode }`
- `dsh-client-ui-conversation` [运行时依赖] - 使用会话 UI 的 Turn 末尾槽与 uiConversation 事件注册面
  - 证据: `src/client/index.ts:6 import type + src/client/index.ts:79 slots.inject('conversation.chat.turnTail')`
- `dsh-client-ui-primitives` [编译依赖] - 复用 Markdown/图标/纯文本提取
  - 证据: `src/client/index.ts:18 import { extractMarkdownPlainText } + src/client/PlanCard.tsx:3`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 槽注册表
  - 证据: `src/client/index.ts:11 import type + src/client/index.ts:52 inject 'slots'`
- `dsh-client-ui-session` [E1+E2] - Session 绑定解析与标准来源
  - 证据: `src/client/index.ts:12 import type + src/client/index.ts:80 ctx.sessions.binding`
- `dsh-client-ui-sidebar-right` [E1+E2] - 打开计划资源与注册预览页型
  - 证据: `src/client/index.ts:16 import type + src/client/index.ts:74 ctx.sidebarRight.openResource`
- `dsh-client-ui-user-questions` [E1+E2] - 计划卡复用 user-questions 的类型面/交互
  - 证据: `src/client/index.ts:15 import type + src/client/PlanCard.tsx:10 import type {}`
- `dsh-plan-mode` [编译依赖] - 引入 plan SessionProjectionMap 声明以使用投影
  - 证据: `src/client/index.ts:10 import type {}`
- `dsh-session` [编译依赖] - 会话身份类型
  - 证据: `src/client/plan.ts:3 import type { SessionId }`
- `dsh-tools` [编译依赖] - 工具结果类型
  - 证据: `src/client/plan-definition.ts:2 import type`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
