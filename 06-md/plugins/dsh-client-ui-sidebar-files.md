# dsh-client-ui-sidebar-files

- 包名: `@deepseek-ai/dsh-client-ui-sidebar-files`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-sidebar-files`

## 实现逻辑
把工作区文件树做成右侧边栏 files 类型：client/index.ts:81 注册 filesDefinition，:86-92 将 FilesBody 注入键控 sidebar.right.pane.tab 并声明子槽 sidebar.right.tab.files.actions，:93-96 注入 FilesTitle，:82 注册字典。数据面由 face.ts 的 filesFace(createList, createWatch) 提供（:85），经 ctx.remote.workspaceFiles 列目录与监听变更；浏览状态（展开层级、加载态）存于 createFilesStore（:84）。快捷键 workspace.files 在 ctx.inject(['shortcuts']) 内注册（:60-80），使类型可用性与侧栏目标解耦。

## Provides
- sidebarRightTabs 标签类型 files（工作区文件树）
- 槽位 sidebar.right.tab.files.actions（目录级动作扩展点）
- 快捷键命令 workspace.files

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 目录列表与文件变更监听走 Remote 命名空间
  - 证据: `src/client/face.ts:21 import type { ClientRemote, RemoteResult } from '@deepseek-ai/dsh-api-remotes/client'; src/client/index.ts:85 filesFace(createList(ctx.remote), createWatch(ctx.remote))`
- `dsh-api-workspace-files` [E1+E2] - 文件树只读能力来自 workspaceFiles 远程面
  - 证据: `src/client/face.ts:26 import type { WorkspaceFileWatchFrame } from '@deepseek-ai/dsh-api-workspace-files/types'; src/client/index.ts:52 inject 声明 'remote.workspaceFiles'`
- `dsh-client-locale` [E1+E2] - 类型标题与快捷键拒绝文案来自字典
  - 证据: `src/client/definition.tsx:10 import type {} from '@deepseek-ai/dsh-client-locale/client'; src/client/index.ts:59 ctx.locale.bind(NS)`
- `dsh-client-shortcuts` [E1+E2] - 注册 workspace.files 命令及平台默认键
  - 证据: `src/client/index.ts:13 import type { ShortcutCommandId }; src/client/index.ts:60-62 ctx.inject(['shortcuts']) + ctx.shortcuts.register`
- `dsh-client-ui-dockkit` [编译依赖] - 标签身份与停靠面板 id
  - 证据: `src/client/face.ts:23 import type { TabId } from '@deepseek-ai/dsh-client-ui-dockkit'`
- `dsh-client-ui-primitives` [编译依赖] - 标题图标与控件复用共享原语
  - 证据: `src/client/FilesTitle.tsx:8 import ... from '@deepseek-ai/dsh-client-ui-primitives'`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 服务由 renderer 提供
  - 证据: `src/client/index.ts:16 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-session` [编译依赖] - 拉入 uiSession 合并以按会话渲染
  - 证据: `src/client/index.ts:17 import type {} from '@deepseek-ai/dsh-client-ui-session/client'`
- `dsh-client-ui-sidebar-right` [E1+E2] - 文件树类型与键控槽由 sidebar-right 声明
  - 证据: `src/client/definition.tsx:9 import type {} from '@deepseek-ai/dsh-client-ui-sidebar-right/client'; src/client/index.ts:81 ctx.sidebarRightTabs.register`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/face.ts:24 import type { SessionId } from '@deepseek-ai/dsh-session/types'`

## Dependents (下游被依赖)
- `dsh-client-ui-open-in-app` - 占用文件标签动作槽位声明
