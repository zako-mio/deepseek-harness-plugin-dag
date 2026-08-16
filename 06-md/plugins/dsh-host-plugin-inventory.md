# dsh-host-plugin-inventory

- 包名: `@deepseek-ai/dsh-host-plugin-inventory`
- 分组: G25 宿主服务
- 拓扑层: Layer 0
- 来源层: L2 web-app
- 源码路径: `packages/host/plugin-inventory`

## 实现逻辑
PluginInventoryGateway（TypertRemoteService）：@Remote('list') 直接遍历 ctx.loader.entries() 投影非 group 条目（entryId/moduleName/enabled/fiberPhase，FiberState→phase 映射），每次调用实时读 Loader，无二级缓存。

## Provides
- ctx.pluginInventory（pluginInventory Typert Remote：list）

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-client-ui-settings-plugin-inventory` - 只读 Loader 条目投影 Remote
