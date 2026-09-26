# dsh-client-ui-sidebar-files

- 包名: `@deepseek-ai/dsh-client-ui-sidebar-files`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-sidebar-files`

## 实现逻辑
浏览器半把 `files` tab 类型注册进 `ctx.sidebarRightTabs`（src/client/index.ts:67），并在 shortcuts 服务可见时注册 `workspace.files` 命令（primary+P，src/client/index.ts:46-66）。面板 body 经键控槽 `sidebar.right.pane.tab` 注册 FilesBody，其注入面由 `filesFace(createList(ctx.remote), createWatch(ctx.remote))` 组合（src/client/index.ts:70-75）；标题经 `sidebar.right.pane.tab.title` 注册 FilesTitle（src/client/index.ts:76-79）。node half 为空 apply。

## Provides
- sidebarFiles locale 命名空间字典
- sidebarRightTabs 注册 'files' tab 类型定义
- sidebar.right.pane.tab 键控条目 key=FILES_ID：工作区文件浏览 body
- sidebar.right.pane.tab.title 键控条目 key=FILES_ID：标签标题
- workspace.files 快捷键命令（primary+P）

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 经 remote 面列目录/订阅文件变更
  - 证据: `src/client/FilesBody.tsx:14 import (client) + src/client/index.ts:71 ctx.remote`
- `dsh-api-workspace-files` [编译依赖] - 工作区文件条目类型
  - 证据: `src/client/FilesBody.tsx:21 import (/types)`
- `dsh-client-locale` [E1+E2] - 注册并绑定本 tab 文案
  - 证据: `src/client/definition.tsx:10 import + src/client/index.ts:45 ctx.locale.bind(NS)`
- `dsh-client-shortcuts` [E1+E2] - 注册打开文件面板命令
  - 证据: `src/client/definition.tsx:8 import (client) + src/client/index.ts:47 ctx.shortcuts.register`
- `dsh-client-ui-dockkit` [编译依赖] - 标签/dock 原语
  - 证据: `src/client/face.ts:23 import`
- `dsh-client-ui-primitives` [编译依赖] - 复用共享 UI 原语
  - 证据: `src/client/FilesTitle.tsx:8 import`
- `dsh-client-ui-renderer` [编译依赖] - 引入 ctx.slots 合并
  - 证据: `src/client/index.ts:16 type-only import`
- `dsh-client-ui-session` [编译依赖] - 引入会话标准 props 合并
  - 证据: `src/client/index.ts:17 type-only import`
- `dsh-client-ui-sidebar-right` [E1+E2] - 把 tab 类型、body 与标题注册进右侧边栏
  - 证据: `src/client/definition.tsx:9 import (client) + src/client/index.ts:67 ctx.sidebarRightTabs.register`
- `dsh-session` [编译依赖] - 会话 id 类型
  - 证据: `src/client/face.ts:24 import (/types)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
