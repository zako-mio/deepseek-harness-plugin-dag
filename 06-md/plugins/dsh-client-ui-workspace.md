# dsh-client-ui-workspace

- 包名: `@deepseek-ai/dsh-client-ui-workspace`
- 分组: G27 会话交互UI
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-workspace`

## 实现逻辑
工作区选择/切换。注册两处：sidebar.workspaces（WorkspaceBrowser，含 sidebar.workspaces.directoryFlow single child + workspace 视图 store）与 conversation.hero.workspace（WorkspacePicker，含 conversation.hero.workspace.directoryFlow child）。二者都通过框架 useWorkspaces hook 读 host Workspaces；inject face 封装 ctx.sessions.search/open/fork/rename/binding 与 ctx.workspaces.startSession/rename/delete/insertBefore/archiveSession/insertSessionBefore/create；flowSource 用 slots.entries/subscribe 观察 directoryFlow 洞是否被填（决定是否渲染目录流）。

## Provides
- slot 声明: sidebar.workspaces, sidebar.workspaces.directoryFlow, conversation.hero.workspace, conversation.hero.workspace.directoryFlow
- WorkspaceBrowser（sidebar 整个浏览区）
- WorkspacePicker（hero 选择器）

## Depends On (上游依赖)
- `dsh-client-locale` [编译依赖] - workspace 命名空间字典
  - 证据: `index.ts:14 type-only + index.ts:54 locale.register`
- `dsh-client-runtime` [运行时依赖] - 会话列表/搜索/分叉与工作区 CRUD 服务
  - 证据: `index.ts:12 ClientContext + index.ts:45 inject sessions/workspaces + index.ts:56-107 sessions.search/fork/open/binding, workspaces.startSession/rename/delete/insertBefore/archiveSession`
- `dsh-client-ui-conversation` [编译依赖] - 消费 conversation.hero.workspace 座位
  - 证据: `index.ts:120-128 注册 conversation.hero.workspace（ui-conversation 声明的 hero child）+ package.json:37`
- `dsh-client-ui-sidebar` [编译依赖] - 消费 sidebar.workspaces 座位（SidebarRoot 声明的洞）
  - 证据: `index.ts:110-119 注册 sidebar.workspaces（ui-sidebar 声明的 child）+ package.json:38 dsh.client.inject`
- `dsh-client-ui-slots` [编译依赖] - slot 注册与洞占用观察
  - 证据: `index.ts:11 HostObservable + index.ts:64-69 slots.entries/subscribe 观察 directoryFlow`

## Dependents (下游被依赖)
- `dsh-client-ui-directory-picker-browse` - 消费 directoryFlow 洞声明（ui-workspace 声明）
- `dsh-client-ui-directory-picker-native` - 消费 directoryFlow 洞声明
