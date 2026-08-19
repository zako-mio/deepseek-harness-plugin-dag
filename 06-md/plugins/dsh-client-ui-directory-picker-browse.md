# dsh-client-ui-directory-picker-browse

- 包名: `@deepseek-ai/dsh-client-ui-directory-picker-browse`
- 分组: G29 UI底座
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-directory-picker-browse`

## 为什么需要它（设计初衷）
应用内 Miller 分栏目录浏览对话框的浏览器半边，经 host.listDirectory/createDirectory 工作，无需本地 OS 对话框，服务远程浏览器。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/client/ui-directory-picker-browse/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/host/directory-picker-browse

## 实现逻辑
目录选择 browse 前端（in-app 对话框）。BrowseDirectoryFlow 以嵌套 slots.inject 事务性注册进 conversation.hero.workspace.directoryFlow 与 sidebar.workspaces.directoryFlow 两个洞；对话框（Select Workspace Directory figma 家族）驱动 host 的 workspaces.listDirectory/createDirectory 原语；locale 字典（zh/en）在包内注册（LOCALE_NS 'directory-browser'）。

## Provides
- conversation.hero.workspace.directoryFlow 条目(BrowseDirectoryFlow)
- sidebar.workspaces.directoryFlow 条目(BrowseDirectoryFlow)

## Depends On (上游依赖)
- `dsh-client-locale` [运行时依赖] - 对话框字典（zh/en）
  - 证据: `index.ts:20 inject 'locale' + index.ts:67/78 ctx.locale.register/bind(LOCALE_NS)`
- `dsh-client-runtime` [运行时依赖] - host 目录列示/创建原语（dsh-host-directory-picker-browse node 半）
  - 证据: `index.ts:20 inject 'workspaces' + index.ts:76-77 ctx.workspaces.listDirectory/createDirectory + contract/workspaces.ts:48/55`
- `dsh-client-ui-primitives` [编译依赖] - UI atoms
  - 证据: `package.json:53 peerDependencies`
- `dsh-client-ui-workspace` [编译依赖] - 消费 directoryFlow 洞声明（ui-workspace 声明）
  - 证据: `index.ts:12 type-only ui-workspace/client + index.ts:83-91 注册两处 directoryFlow 洞 + package.json:36 dsh.client.inject`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
