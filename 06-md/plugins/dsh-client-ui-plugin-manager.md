# dsh-client-ui-plugin-manager

- 包名: `@deepseek-ai/dsh-client-ui-plugin-manager`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-plugin-manager`

## 实现逻辑
Host 半 PluginRegistryProbe（TypertRemoteService，ctx.pluginRegistryProbe）并行 ping npm 与 npmmirror，用 Promise.any 取最快可用 registry，带超时、并发合流与 TTL 缓存（src/index.ts:50-85）。浏览器半把 Plugins 侧栏条目与 main 面板页注册进 sidebar.panellist 与 main，页面经 pluginManager/pluginInventory Remote 安装、启用、禁用、移除 bundle，并订阅 plugin-manager/changed、install-log、install-state 与 connection/reset 刷新（src/client/index.ts:76-147）。它还通过 ctx.reflect.provide('pluginNavigation') 提供跨插件跳转，并声明 plugins.* 子槽让插件自带配置界面渲染到本页（src/client/index.ts:110-140、src/client/index.ts:119-128）。

## Provides
- ctx.pluginRegistryProbe (Host 端 npm registry 可用性探测与缓存) (src/index.ts:50-57)
- ctx.pluginNavigation (跨插件打开某个 bundle 详情) (src/client/index.ts:133)
- Plugins 面板及其 plugins.* 配置槽声明 (src/client/index.ts:110-140)

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - Remote 调用与转发事件面
  - 证据: `src/client/PluginManagerPage.tsx:13 import + src/client/index.ts:89 ctx.remote`
- `dsh-client-locale` [E1+E2] - 注册 pluginManager 字典
  - 证据: `src/client/index.ts:10 import + src/client/index.ts:77 ctx.locale.register(NS)`
- `dsh-client-product-analytics` [E1+E2] - 插件管理操作埋点
  - 证据: `src/client/index.ts:9 import type + src/client/manager-store.ts:9 import`
- `dsh-client-ui-layout` [E1+E2] - 注册 main keyed 面板并读取面板选择
  - 证据: `src/client/index.ts:15 import type + src/client/index.ts:130 ctx.layout.panelInfo`
- `dsh-client-ui-primitives` [编译依赖] - 复用提示与图标控件
  - 证据: `src/client/PluginRefreshToast.tsx:3 import + src/client/PluginsPanelIcon.tsx:4 import`
- `dsh-client-ui-renderer` [编译依赖] - 渲染器槽位服务类型
  - 证据: `src/client/index.ts:17 import type`
- `dsh-client-ui-settings` [编译依赖] - 配置表单投影类型
  - 证据: `src/client/manager-store.ts:33 import + src/client/slot-contract.ts:21 import`
- `dsh-client-ui-sidebar` [编译依赖] - 占用 sidebar.panellist 槽位声明
  - 证据: `src/client/PluginsPanelIcon.tsx:6 import + src/client/index.ts:16 import type`
- `dsh-plugin-manager` [E1+E2] - 调用插件管理 Remote 并订阅其事件
  - 证据: `src/client/index.ts:22 import type + src/client/index.ts:89 ctx.remote.$on('plugin-manager/changed')`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 把该业务包的 /remote 命名空间装配进 Client
- `dsh-client-ui-agent-preset` - 在 plugins.add.actions 提供创建入口
- `dsh-client-ui-settings-agent-loop` - 页面必须注册进 Plugins 页声明的 plugins.item 槽，注册失败即加载报错
- `dsh-client-ui-settings-shell` - 页面必须注册进 Plugins 页声明的 plugins.item 槽
- `dsh-client-ui-settings-subagent` - 页面必须注册进 Plugins 页声明的 plugins.item 槽
- `dsh-client-ui-settings-web-search` - 页面必须注册进 Plugins 页声明的 plugins.item 槽
- `dsh-experimental-client-ui-cot-translation` - 偏好表单注册进 bundle 配置页，表单作用域由 configForms 服务提供
- `dsh-experimental-client-ui-voice-input` - 「打开设置」跳转到 bundle 配置页，依赖插件导航服务
