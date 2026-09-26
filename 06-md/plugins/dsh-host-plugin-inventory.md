# dsh-host-plugin-inventory

- 包名: `@deepseek-ai/dsh-host-plugin-inventory`
- 分组: G20 宿主服务
- 拓扑层: Layer 6
- 来源层: L2 web-app
- 源码路径: `packages/host/plugin-inventory`

## 实现逻辑
以 TypertRemoteService 暴露只读 Remote 服务 ctx.pluginInventory，list() 每次直接读 Loader（src/index.ts:51-73）。readPluginInventory 遍历 ctx.loader.entries() 投影非 group 条目的 moduleName/enabled/fiberPhase 与可选本地化元数据，并可选拼入 agent preset 的 composition 行（src/index.ts:82-113）。Fiber 状态经运行时镜像表映射为稳定的 PluginFiberPhase（src/index.ts:30-48）。

## Provides
- ctx.pluginInventory (Remote list：当前 Loader 插件条目与 preset 组合快照，src/index.ts:51-73)

## Depends On (上游依赖)
- `dsh-agent-preset-registry` [E1+E2] - 读取 agent preset 组合清单并投影其行
  - 证据: `package.json:51 peerDep + src/index.ts:6 type import; src/index.ts:97 ctx.get('agentPresets')、:100 compositionInventory`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配插件清单命名空间
- `dsh-plugin-manager` - 读取运行时插件清单与 entryId 映射，供 listPlugins 对齐
