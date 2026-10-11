# dsh-client-ui-subagent

- 包名: `@deepseek-ai/dsh-client-ui-subagent`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-subagent`

## 实现逻辑
为子 Agent 会话提供血统导航与只读输入面：client/index.ts:60-73 构造 catalogActions（openChild 走 ctx.uiWorkspace.openSession，openChildAside 走 ctx.sidebarRight.openResource 打开 subagentchat 标签，refreshProjection 走 ctx.sessions.refreshProjections），:74-94 把它们注册进 conversation.session.header.lineage 与 header.actions（order -30 领衔标题带）；:95-103 用 selectReadOnlySubagent（:37-49）按 one-shot / 父不可用 / unknown 判定是否接管 conversation.composer。sidebar-chat/index.tsx 另注册右侧边栏的 subagentchat 标签类型与资源提供者，使子会话可在侧栏内查看（:178-181 读 ctx.sessions/ctx.resources/sidebarRightTabs）。

## Provides
- 槽位贡献 conversation.session.header.lineage、conversation.session.header.actions（subagent-catalog）、conversation.composer（只读 composer 选择器）
- sidebarRightTabs 标签类型 subagentchat（侧栏查看子会话）

## Depends On (上游依赖)
- `dsh-api-session-controller` [E1+E2] - 子 Agent 目录来自会话投影，刷新经 sessions 服务
  - 证据: `src/client/SubagentHeaderLineage.tsx:5 import type { SessionProjectionMap, SessionSummary } from '@deepseek-ai/dsh-api-session-controller/client'; src/client/index.ts:71 ctx.sessions.refreshProjections`
- `dsh-client-locale` [E1+E2] - 目录、血统与只读提示文案本地化
  - 证据: `src/client/index.ts:11 import type {} from '@deepseek-ai/dsh-client-locale/client'; src/client/index.ts:56 ctx.locale.register(NS, { zh, en })`
- `dsh-client-resources` [E1+E2] - subagentchat 作为资源类型接入资源模型
  - 证据: `src/client/sidebar-chat/index.tsx:6 import type { ResourceProvider } from '@deepseek-ai/dsh-client-resources/client'`
- `dsh-client-ui-chat` [编译依赖] - 复用 chat 侧的会话节点/视图类型
  - 证据: `src/client/index.ts:12 import type {} from '@deepseek-ai/dsh-client-ui-chat/client'`
- `dsh-client-ui-conversation` [编译依赖] - composer 链与会话视图契约由 ui-conversation 声明
  - 证据: `src/client/index.ts:5 import type { ComposerChainProps } from '@deepseek-ai/dsh-client-ui-conversation/client'; src/client/sidebar-chat/index.tsx:7 import type { ConversationViewsProps }`
- `dsh-client-ui-primitives` [编译依赖] - 血统行图标与提示控件复用共享原语
  - 证据: `src/client/SubagentHeaderLineage.tsx:8-10 import { IconChevronDownOutlineRegular, StateDot, Tooltip, ... } from '@deepseek-ai/dsh-client-ui-primitives'`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 服务由 renderer 提供
  - 证据: `src/client/index.ts:13 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-session` [编译依赖] - 拉入 uiSession 合并以读取当前会话
  - 证据: `src/client/index.ts:14 import type {} from '@deepseek-ai/dsh-client-ui-session/client'`
- `dsh-client-ui-sidebar-right` [E1+E2] - 侧栏标签类型与资源打开能力由 sidebar-right 提供
  - 证据: `src/client/sidebar-chat/index.tsx:8 import type { SidebarRightTabDefinition } from '@deepseek-ai/dsh-client-ui-sidebar-right/client'; src/client/index.ts:65 ctx.sidebarRight.openResource`
- `dsh-client-ui-workspace` [E1+E2] - 打开子会话走工作区导航服务
  - 证据: `src/client/index.ts:16 import type {} from '@deepseek-ai/dsh-client-ui-workspace/client'; src/client/index.ts:62 ctx.uiWorkspace.openSession(address)`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/index.ts:4 import type { SessionId } from '@deepseek-ai/dsh-session/types'`
- `dsh-subagent` [编译依赖] - 子 Agent 地址与血统类型由 dsh-subagent 定义
  - 证据: `src/client/SubagentHeaderLineage.tsx:6 import type { SubagentAddress } from '@deepseek-ai/dsh-subagent/client'`
- `dsh-token-meter` [编译依赖] - 血统行复用 token-meter 的用量展示类型
  - 证据: `src/client/SubagentHeaderLineage.tsx:14 import type {} from '@deepseek-ai/dsh-token-meter/client'`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
