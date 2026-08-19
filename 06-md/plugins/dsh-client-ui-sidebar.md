# dsh-client-ui-sidebar

- 包名: `@deepseek-ai/dsh-client-ui-sidebar`
- 分组: G29 UI底座
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-sidebar`

## 为什么需要它（设计初衷）
侧边栏插件：会话多级树、搜索、分组、状态点，组织会话导航。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-sidebar/package.json

## 实现逻辑
侧栏外壳。SidebarRoot 注册进 layout 声明的 'sidebar' slot，并声明三个 child：sidebar.workspaces（whole browsing region，ui-workspace 占据）、sidebar.settings（ui-settings 占据）、sidebar.footer.action（list，ui-cordis 等注册）；inject 提供 startSession（ctx.workspaces.startSession，当前 Workspace→最近回退）与 toggleSidebar（ctx.layout.toggleSidebar）。

## Provides
- slot 声明: sidebar.workspaces(single/root), sidebar.settings(single/root), sidebar.footer.action(list/root)
- SidebarRoot 外壳（含折叠 rail）

## Depends On (上游依赖)
- `dsh-client-locale` [编译依赖] - sidebar 命名空间字典
  - 证据: `index.ts:4 type-only + index.ts:32 locale.register`
- `dsh-client-runtime` [运行时依赖] - 新会话创建与工作区服务
  - 证据: `index.ts:26 inject sessions/workspaces + index.ts:37 ctx.workspaces.startSession`
- `dsh-client-ui-layout` [编译依赖] - 消费 sidebar 列座位与 ctx.layout 面板动作
  - 证据: `index.ts:41-53 注册 'sidebar'（layout 声明的 child）+ package.json:36 dsh.client.inject + index.ts:38 ctx.layout.toggleSidebar()`
- `dsh-client-ui-primitives` [编译依赖] - UI atoms
  - 证据: `package.json:53 peerDependencies`
- `dsh-client-ui-slots` [编译依赖] - slot 注册与 child 声明
  - 证据: `contract/slots.ts 类型 + slots.register API`

## Dependents (下游被依赖)
- `dsh-client-ui-brand-official` - 填充侧边栏品牌slot contract
- `dsh-client-ui-cordis` - 消费 sidebar.footer.action 座位声明
- `dsh-client-ui-settings-general` - 占用 sidebar 提供的 settings 洞
- `dsh-client-ui-workspace` - 消费 sidebar.workspaces 座位（SidebarRoot 声明的洞）
