# dsh-client-ui-plugin-manager

- 包名: `@deepseek-ai/dsh-client-ui-plugin-manager`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-plugin-manager`

## 实现逻辑
客户端半在 apply 中创建 PluginManagerController，订阅 Host 的 plugin-manager/changed、install-log、install-state 与 connection/reset 事件，仅在有快照时刷新（src/client/index.ts:85-92）。随后用 slots.inject('main') 注册 main 面板 'plugins'，并声明 plugins.item / bundle.activation / bundle.config / row.config / detail.* 等子槽作为页面配置扩展点（src/client/index.ts:100-120）；同时把 ctx.pluginNavigation 以 reflect.provide 暴露供跨插件打开某 bundle（src/client/index.ts:122-128），并把 Plugins 入口注册进 sidebar.panellist（index.ts:130）。Host 半 src/index.ts 默认导出 PluginRegistryProbe，用并行 HTTPS ping 探测 npm/npmmirror 注册表并缓存结果（src/index.ts:31-84）。

## Provides
- main 面板 'plugins'（PluginManagerPage，并声明 plugins.item / plugins.bundle.activation / plugins.bundle.config / plugins.row.config / plugins.detail.actions / plugins.detail.badge / plugins.detail.section 子槽）
- ctx.pluginNavigation.openBundle (跨插件导航并打开指定 bundle 详情视图)
- sidebar.panellist 条目 'plugins'（PluginsPanelIcon 侧栏入口）
- ctx.pluginRegistryProbe (Host 侧 PluginRegistryProbe Remote 服务：探测最快 npm 注册表)

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 调用 pluginManager 等 Remote 并订阅 Host 事件
  - 证据: `src/client/index.ts:19 import + src/client/manager-store.ts:607 ctx.remote`
- `dsh-client-locale` [运行时依赖] - 注册 pluginManager 文案
  - 证据: `src/client/index.ts:10 import + src/client/index.ts:75 ctx.locale.register(NS)`
- `dsh-client-ui-layout` [E1+E2] - 注册 main 面板并订阅主面板切换重置视图
  - 证据: `src/client/index.ts:15 import type { MainPanelId } + src/client/index.ts:119 ctx.layout.panelInfo`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 槽注册表
  - 证据: `src/client/index.ts:17 import type + src/client/index.ts:67 inject 'slots'`
- `dsh-client-ui-settings` [E1+E2] - 插件配置页复用 ui-settings 的 configForms
  - 证据: `src/client/manager-store.ts:32 import + src/client/manager-store.ts:543 ctx.configForms`
- `dsh-client-ui-sidebar` [运行时依赖] - 使用 ui-sidebar 声明的面板列表槽
  - 证据: `src/client/index.ts:16 import type + src/client/index.ts:130 slots.inject('sidebar.panellist')`
- `dsh-plugin-manager` [E1+E2] - 插件管理 Remote 与 registry 协议类型
  - 证据: `src/client/index.ts:22 import types + src/client/manager-store.ts:28 import '/registry'`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配插件管理 UI 探针命名空间
- `dsh-client-ui-settings-agent-loop` - Plugins 页拥有 plugins.item 槽位，本包向其贡献页面
- `dsh-client-ui-settings-shell` - Plugins 页拥有 plugins.item 槽位
- `dsh-client-ui-settings-subagent` - Plugins 页拥有 plugins.item 槽位
- `dsh-client-ui-settings-web-search` - Plugins 页拥有 plugins.item 槽位
- `dsh-experimental-client-ui-voice-input` - 跳转到 voice-input 插件 bundle 进行模型准备
