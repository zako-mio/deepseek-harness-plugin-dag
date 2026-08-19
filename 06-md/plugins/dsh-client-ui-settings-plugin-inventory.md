# dsh-client-ui-settings-plugin-inventory

- 包名: `@deepseek-ai/dsh-client-ui-settings-plugin-inventory`
- 分组: G28 设置输入UI
- 拓扑层: Layer 11
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-plugin-inventory`

## 为什么需要它（设计初衷）
Web 插件设置里的只读 Cordis Loader 清单标签页，展示已装载插件库存。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-settings-plugin-inventory/package.json

## 实现逻辑
只读插件清单 tab：注册 settings.plugins.tab id=all order=10（index.ts:39-46），list 闭包调 ctx.remote.pluginInventory.list() RPC 拉取当前 Loader 条目投影（:30-36），渲染 PluginInventorySettingsTab。inject 含 remote.pluginInventory 生成 Remote 面。

## Provides
- settings.plugins.tab 'all' 注册 (PluginInventorySettingsTab)
- settings.pluginInventory 字典命名空间

## Depends On (上游依赖)
- `dsh-api-remotes` [编译依赖] - remote 面与转发事件键
  - 证据: `packages/client/ui-settings-plugin-inventory/package.json:35 (dsh.client inject api-remotes)`
- `dsh-client-ui-settings` [编译依赖] - settings.plugins.tab 槽声明
  - 证据: `packages/client/ui-settings-plugin-inventory/src/client/index.ts:5 (type-only import), :39 (slots.inject('settings.plugins.tab'))`
- `dsh-host-plugin-inventory` [运行时依赖] - 只读 Loader 条目投影 Remote
  - 证据: `packages/client/ui-settings-plugin-inventory/src/client/index.ts:31 (ctx.remote.pluginInventory.list())`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
