# dsh-api-workspace-controller

- 包名: `@deepseek-ai/dsh-api-workspace-controller`
- 分组: G02 API 网关与控制器
- 拓扑层: Layer 4
- 来源层: L2 web-app
- 源码路径: `packages/api/workspace-controller`

## 实现逻辑
WorkspaceController 继承 TypertRemoteService，以 namespace 'workspace' 注册，注入 typert/workspaceRegistry，并用 WorkspaceCommands/WorkspaceFeed 承载命令与状态流，同时把 DirectoryPickerController 作为子插件挂载 (src/index.ts:51-78)。命令方法（create/rename/delete/insertBefore/insertSessionBefore/archiveSession/unarchiveSession/pinSession/unpinSession）先串行化再调用 workspaceRegistry，并把注册表异常映射为 workspace/* / session/* Remote 失败 (src/commands.ts:45-227, 242-248)。follow 先产 baseline 再订阅 domain/changed，按 workspace 域变更派发 upsert/order/archived/pinned/remove 增量 (src/feed.ts:85-139)。DirectoryPickerController 依 directoryPicker.capability() 门控分发 pick/list/createDirectory，并把 seam 错误投影为 directory-picker/* (src/directory-picker.ts:54-119, 127-170)。

## Provides
- ctx.remote.workspace（workspace 命名空间：create/initializeDefault/rename/delete/insertBefore/insertSessionBefore/archiveSession/unarchiveSession/pinSession/unpinSession/follow）
- ctx.remote.directoryPicker（目录选择/浏览：pick/list/createDirectory）

## Depends On (上游依赖)
- `dsh-api-gateway` [编译依赖] - 客户端 Remote 载体
  - 证据: `src/client/model.ts:5 import`
- `dsh-session` [编译依赖] - 会话身份类型
  - 证据: `src/types.ts:8 import type`
- `dsh-storage-domain` [编译依赖] - domain/changed 事件类型
  - 证据: `src/feed.ts:5 import type DomainChanged`
- `dsh-workspace` [E1+E2] - 工作区注册表 seam（全部命令与状态源）
  - 证据: `src/commands.ts:4 import + src/index.ts:52 static inject 'workspaceRegistry'`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配 workspace 命名空间
- `dsh-client-ui-conversation` - 工作区状态以渲染工作区标题
- `dsh-client-ui-schedule` - 工作区状态以判定会话是否可跳转
- `dsh-client-ui-sidebar` - startSession 的 workspace 参数类型
- `dsh-client-ui-sidebar-browser` - 经 workspace 服务把浏览器页面映射到工作区
- `dsh-client-ui-workspace` - 读写工作区实体与快照（create/rename/delete/pin）
