# dsh-plugin-manager

- 包名: `@deepseek-ai/dsh-plugin-manager`
- 分组: G04 启动与插件管理
- 拓扑层: Layer 7
- 来源层: L1 核心集
- 源码路径: `packages/boot/plugin-manager`

## 实现逻辑
`PluginManager extends TypertRemoteService` 以 `@Remote` 方法向前端暴露当前 profile 的插件/包管理 (src/index.ts:176-178)。它把 profile patch 与 manifest 组合成可寻址行，判定 protected/unaddressable/management-required 只读原因 (src/index.ts:256-272)，并以 `withFileLock`+`writeFileAtomic` 串行化 set/install/remove，失败或取消时回滚 `package.json`/`pnpm-lock.yaml` (src/index.ts:767-791, 697-713)。安装走 `runProfilePnpm` 并逐 registry 重试、做 GitHub 连通性预检与产物 bundle 校验 (src/index.ts:461-567)；`tools.ts` 另注册 `plugin_manager` 工具，经沙箱提权审批后调用同一服务 (src/tools.ts:18-91)。

## Provides
- ctx.pluginManager (当前 profile 的插件/包管理服务：listPlugins/listBundles/inspect/installBundle/removeBundle/setPluginEnabled/setBundleEnabled)
- plugin_manager 工具 (Agent 侧管理入口，含沙箱提权与审批)
- 版本豁免管理 (listVersionExemptions/setVersionExemption)
- plugin-manager/install-log、plugin-manager/install-state、plugin-manager/changed 事件

## Depends On (上游依赖)
- `cordis-plugin-include` [编译依赖] - 解析/生成 profile patch 的 PatchOptions 行结构
  - 证据: `src/index.ts:10 + src/operations.ts:7`
- `cordis-plugin-loader` [E1+E2] - 读取活动 Loader 行以判定可寻址性与 bundle 贡献是否在用
  - 证据: `src/index.ts:9 + src/index.ts:177 static inject 'loader'`
- `dsh-hmr` [运行时依赖] - 配置写入与热重载串行化，并在无 HMR 时降级为 restart-required
  - 证据: `src/index.ts:20 (type merge) + src/index.ts:757-759 ctx.get('hmr').runExclusive`
- `dsh-host-plugin-inventory` [编译依赖] - 读取运行时插件清单与 entryId 映射，供 listPlugins 对齐
  - 证据: `src/index.ts:13 + src/types.ts:4-6`
- `dsh-sandbox-policy` [运行时依赖] - 解析会话沙箱模式，决定管理操作是否需要 danger-full-access 提权
  - 证据: `src/tools.ts:5 + src/tools.ts:13 inject + src/tools.ts:38 ctx.sandboxPolicy.resolve`
- `dsh-tools` [E1+E2] - 注册面向模型的 plugin_manager 工具
  - 证据: `src/tools.ts:9 + src/tools.ts:13 inject 'tools' + src/tools.ts:19 ctx.tools.register`
- `dsh-user-approval` [运行时依赖] - 对提权的管理动作要求用户审批
  - 证据: `src/tools.ts:6 + src/tools.ts:42 ctx.get('approval')`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配插件管理命名空间与事件
- `dsh-client-ui-plugin-manager` - 插件管理 Remote 与 registry 协议类型
