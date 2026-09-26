# dsh-client-ui-workspace

- 包名: `@deepseek-ai/dsh-client-ui-workspace`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-workspace`

## 实现逻辑
注册工作区浏览区与 Session 行动作：apply 创建 UiWorkspaceService 与视图 store，用 ctx.slots.provideRoot 提供全局 workspaces hook（src/client/index.ts:117-121），向 'sidebar.workspaces' 注册 WorkspaceBrowser 并声明 directoryFlow、会话菜单/行动作、行装饰等子槽（src/client/index.ts:257-277），向 'conversation.hero.workspace' 注册 WorkspacePicker（src/client/index.ts:307-315）。随后把 pin/rename/fork/archive 四个行动作、rename/archive 对话框与 toast 注入对应槽，并安装工作区快捷键（src/client/index.ts:200,282-306）。

## Provides
- slot sidebar.workspaces（WorkspaceBrowser）与子槽 directoryFlow/session.menu.item/session.row.action/session.row.leading/session.row.hover
- slot conversation.hero.workspace（WorkspacePicker）与子槽 conversation.hero.workspace.directoryFlow
- slot shell.overlay 的 session-rename / session-archive / row-toast 表面
- ctx.uiWorkspace 服务（会话导航、pin/archive/fork、目录选择与浏览）
- 全局 useWorkspaces hook（slots.provideRoot）与工作区快捷键

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 引入 agent 活动类型用于归档确认
  - 证据: `src/client/session-actions/ArchiveSession.tsx:12 import type`
- `dsh-api-remotes` [E1+E2] - Host 目录选择器与 $host 事实
  - 证据: `src/client/index.ts:19 import + src/client/index.ts:118 ctx.remote.directoryPicker`
- `dsh-api-session-controller` [E1+E2] - 会话列表、rename、search 与引用保留
  - 证据: `src/client/index.ts:20 import + src/client/index.ts:106 ctx.get('sessions')`
- `dsh-api-workspace-controller` [E1+E2] - 读写工作区实体与快照（create/rename/delete/pin）
  - 证据: `src/client/index.ts:29 import + src/client/index.ts:107 ctx.get('workspaces')`
- `dsh-client-locale` [E1+E2] - 注册 workspace 字典
  - 证据: `src/client/index.ts:31 + src/client/index.ts:121 ctx.locale.register`
- `dsh-client-shortcuts` [E1+E2] - 注册/读取工作区快捷键命令
  - 证据: `src/client/contract/slots.ts:53 + src/client/index.ts:249 ctx.shortcuts.catalog`
- `dsh-client-ui-conversation` [编译依赖] - 引入 conversation.hero.workspace 槽声明类型
  - 证据: `src/client/contract/slots.ts:47 import type`
- `dsh-client-ui-layout` [E1+E2] - 导航取消信号与面板选择
  - 证据: `src/client/index.ts:34 import type + src/client/navigation.ts:204 ctx.layout.beginNavigation`
- `dsh-client-ui-primitives` [编译依赖] - 复用菜单项、对话框等原语
  - 证据: `src/client/rows/Rows.tsx:24 + src/client/session-actions/RenameSession.tsx:8`
- `dsh-client-ui-renderer` [编译依赖] - 拉入槽/渲染服务类型合并
  - 证据: `src/client/index.ts:33 import type`
- `dsh-client-ui-session` [编译依赖] - 拉入会话根标准 hook 类型合并
  - 证据: `src/client/index.ts:36 import type`
- `dsh-client-ui-sidebar` [编译依赖] - 引入 sidebar.workspaces 等槽的声明类型
  - 证据: `src/client/contract/slots.ts:46 import type`
- `dsh-schedule` [编译依赖] - 归档前检查会话是否有计划任务
  - 证据: `src/client/session-actions/ArchiveSession.tsx:14 import type`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/index.ts:26 SessionId`
- `dsh-subagent` [编译依赖] - 导航到子代理会话地址
  - 证据: `src/client/navigation.ts:13 SubagentAddress`

## Dependents (下游被依赖)
- `dsh-client-ui-agent-preset` - Creator 模式起草后落到新会话
- `dsh-client-ui-chat` - 分叉后打开新会话
- `dsh-client-ui-directory-picker-browse` - 占据目录流洞并驱动枚举/创建原语
- `dsh-client-ui-directory-picker-native` - 占据目录流洞并驱动 Host OS 选择器
- `dsh-client-ui-schedule` - 从任务卡跳转到原始会话
- `dsh-client-ui-subagent` - 把子代理会话打开为主视图导航
- `dsh-client-ui-workflow-run` - 从工作流面板导航到成员会话
- `dsh-experimental-client-ui-agent-team` - 切换/打开成员会话视图
