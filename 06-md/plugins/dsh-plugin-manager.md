# dsh-plugin-manager

- 包名: `@deepseek-ai/dsh-plugin-manager`
- 分组: G04 启动与插件管理
- 拓扑层: Layer 7
- 来源层: L1 核心集
- 源码路径: `packages/boot/plugin-manager`

## 实现逻辑
实现当前 profile 的插件与 bundle 管理：PluginManager 继承 TypertRemoteService 注册 ctx.pluginManager 并注入 loader/profileContext(src/index.ts:178-179,207-211)，通过 @Remote 暴露 listVersionExemptions/setVersionExemption/listPlugins/listBundles/registries/inspect/setPluginEnabled/setBundleEnabled/installBundle/waitForInstall/cancelInstall/removeBundle(src/index.ts:233-673)。所有变更经 withFileLock 与 diskState 比对后 emit plugin-manager/changed(src/index.ts:824-848)，安装用 pnpm 在 profile 目录执行并流式发出 plugin-manager/install-log(src/index.ts:709-729)。另有独立函数插件 tools.ts 注册 Agent 工具 plugin_manager，先做 danger-full-access 升级审批再调用同一服务(src/tools.ts:13-92)。

## Provides
- ctx.pluginManager(当前 profile 插件/包管理服务与 ctx.remote.pluginManager 命名空间所有者，src/index.ts:170-178,207-227)
- Agent 工具 plugin_manager(list/set/install/remove/版本豁免，src/tools.ts:13-92)
- 事件 plugin-manager/changed|install-log|install-state(src/types.ts:258-271)

## Depends On (上游依赖)
- `cordis-plugin-include` [编译依赖] - 读写 profile 补丁的条目与插入语义
  - 证据: `src/index.ts:10 import type PatchOptions`
- `cordis-plugin-loader` [E1+E2] - 枚举 Loader 条目以决定哪些插件行可写
  - 证据: `package.json:69 peerDep + src/index.ts:9 import type EntryOptions + src/index.ts:179 inject 'loader' + src/index.ts:262 this.ctx.loader.entries()`
- `dsh-hmr` [E1+E2] - 在线 profile 立即应用变更，否则标记需重启
  - 证据: `package.json:74 peerDep(optional) + src/index.ts:21 import type {} + src/index.ts:805-807 this.ownerContext.get('hmr')/hmr.runExclusive`
- `dsh-host-plugin-inventory` [E1+E2] - 读取运行时插件清单并生成可寻址 entryId
  - 证据: `package.json:70 peerDep + src/index.ts:13 import pluginEntryId/readPluginInventory + src/types.ts:4-6 import types + src/index.ts:260 readPluginInventory(this.ctx)`
- `dsh-sandbox-policy` [E1+E2] - 解析当前会话沙箱档以判定所需升级
  - 证据: `package.json:76 peerDep + src/tools.ts:5 import type {} + src/tools.ts:13 inject 'sandboxPolicy' + src/tools.ts:38 ctx.sandboxPolicy.resolve`
- `dsh-tools` [E1+E2] - 向 Agent 暴露 plugin_manager 工具
  - 证据: `package.json:73 peerDep + src/tools.ts:9 import defineTool + src/tools.ts:13 inject ['tools','pluginManager','sandboxPolicy'] + src/tools.ts:19 ctx.tools.register`
- `dsh-user-approval` [E1+E2] - 把升级请求接到审批通道
  - 证据: `package.json:78 peerDep(optional) + src/tools.ts:6 import type {} + src/tools.ts:42 ctx.get('approval')`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 把该业务包的 /remote 命名空间装配进 Client
- `dsh-client-ui-plugin-manager` - 调用插件管理 Remote 并订阅其事件
