# dsh-client-ui-workspace

- 包名: `@deepseek-ai/dsh-client-ui-workspace`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-workspace`

## 实现逻辑
工作区与会话浏览的客户端宿主：client/index.ts:106-121 的 apply 构造 UiWorkspaceService（navigation.ts:162 super(ctx, 'uiWorkspace')）从而提供 ctx.uiWorkspace，并把 workspaces.list 作为 root 全局 hook 暴露（:121，供 useWorkspaces 选择器）。:270-290 注册 WorkspaceBrowser 进 sidebar.workspaces 并声明 directoryFlow、菜单项、行操作、行前置与悬停卡等子槽；:295-319 把 pin/rename/fork/archive 四个内建会话动作、重命名与归档确认浮层、行操作提示注册进对应槽（order 步进 100 便于插件插入）；:320-328 注册 WorkspacePicker 到 conversation.hero.workspace。快捷键经 shortcuts.ts 安装（:123），会话检索走 sessions.search（:125-129）。

## Provides
- ctx.uiWorkspace (会话/工作区导航服务：openSession、connectWorkspace、startSession 等)
- root 全局 hook workspaces（useWorkspaces 选择器）
- 槽位 sidebar.workspaces 及其子槽（directoryFlow / session.menu.item / session.row.action / session.row.leading / session.row.hover）、conversation.hero.workspace
- 内建会话行动作 pin / rename / fork / archive 与对应浮层

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 归档前判定会话活动状态
  - 证据: `src/client/session-actions/ArchiveSession.tsx:12 import type ... from '@deepseek-ai/dsh-agent/types'`
- `dsh-api-remotes` [E1+E2] - 目录选择器与 Host 事实经 Remote 提供
  - 证据: `src/client/index.ts:20 import type {} from '@deepseek-ai/dsh-api-remotes/client'; src/client/index.ts:119 ctx.remote.directoryPicker`
- `dsh-api-session-controller` [E1+E2] - 会话检索、fork 与归档动作走会话控制器
  - 证据: `src/client/index.ts:29 import type {} from '@deepseek-ai/dsh-api-session-controller/client'; src/client/index.ts:107 ctx.get('sessions') as ISessions`
- `dsh-api-workspace-controller` [E1+E2] - 工作区列表、创建、归档与固定状态由工作区控制器拥有
  - 证据: `src/client/index.ts:30 import type {} from '@deepseek-ai/dsh-api-workspace-controller/client'; src/client/index.ts:108 ctx.get('workspaces') as IWorkspaces`
- `dsh-client-locale` [E1+E2] - 浏览区、菜单与浮层文案本地化
  - 证据: `src/client/index.ts:32 import type {} from '@deepseek-ai/dsh-client-locale/client'; src/client/index.ts:122 ctx.locale.register(NS, { zh, en })`
- `dsh-client-product-analytics` [编译依赖] - 拉入产品分析客户端的 Context 合并以记录会话动作
  - 证据: `src/client/index.ts:18 import type {} from '@deepseek-ai/dsh-client-product-analytics/client'`
- `dsh-client-shortcuts` [E1+E2] - 工作区与会话动作的快捷键注册
  - 证据: `src/client/shortcuts.ts:5 import type {} from '@deepseek-ai/dsh-client-shortcuts/client'; src/client/index.ts:262-263 ctx.shortcuts 使用`
- `dsh-client-ui-conversation` [编译依赖] - conversation.hero.workspace 槽由 ui-conversation 声明
  - 证据: `src/client/index.ts:47 import { WorkspaceBrowser } ...; src/client/navigation.ts:20 import type {} from '@deepseek-ai/dsh-client-ui-conversation/client'`
- `dsh-client-ui-layout` [E1+E2] - 导航切页需驱动 frame 的 layout 面板动作
  - 证据: `src/client/index.ts:35 import type {} from '@deepseek-ai/dsh-client-ui-layout/client'; src/client/navigation.ts:227 ctx.layout`
- `dsh-client-ui-primitives` [编译依赖] - 行、菜单与按钮复用共享原语
  - 证据: `src/client/rows/Rows.tsx:24 import ... from '@deepseek-ai/dsh-client-ui-primitives'`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 服务由 renderer 提供
  - 证据: `src/client/index.ts:34 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-session` [编译依赖] - 拉入 uiSession 合并以驱动会话切换
  - 证据: `src/client/index.ts:37 import type {} from '@deepseek-ai/dsh-client-ui-session/client'`
- `dsh-client-ui-sidebar` [编译依赖] - sidebar.workspaces 槽由 ui-sidebar 声明
  - 证据: `src/client/contract/slots.ts:46 import type {} from '@deepseek-ai/dsh-client-ui-sidebar/client'`
- `dsh-schedule` [编译依赖] - 归档确认展示定时任务占用信息
  - 证据: `src/client/session-actions/ArchiveSession.tsx:14 import type ... from '@deepseek-ai/dsh-schedule/client'`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/index.ts:27 import type { SessionId } from '@deepseek-ai/dsh-session/types'`
- `dsh-subagent` [编译依赖] - 导航需识别子 Agent 地址以打开子会话
  - 证据: `src/client/navigation.ts:14 import type ... from '@deepseek-ai/dsh-subagent/client'`

## Dependents (下游被依赖)
- `dsh-client-ui-agent-preset` - 创建并落地新会话
- `dsh-client-ui-chat` - 打开会话所属工作区
- `dsh-client-ui-directory-picker-browse` - 占据目录流洞并驱动枚举/创建原语
- `dsh-client-ui-directory-picker-native` - 占据目录流洞并驱动 Host OS 选择器
- `dsh-client-ui-schedule` - 向 ui-workspace 声明的会话行 seat 注册标记与悬停卡，并用其 openSession 跳回原会话
- `dsh-client-ui-subagent` - 打开子会话走工作区导航服务
- `dsh-client-ui-workflow-run` - 面板中打开成员会话走工作区导航服务
- `dsh-experimental-client-ui-agent-team` - 切换/打开成员会话视图
