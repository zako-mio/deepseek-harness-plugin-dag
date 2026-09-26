# dsh-hmr

- 包名: `@deepseek-ai/dsh-hmr`
- 分组: G04 启动与插件管理
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/boot/hmr`

## 实现逻辑
HMR 服务以 Chokidar 监听模块根，把文件变更经 debounce 后串行投入 `runExclusive` 队列处理 (src/index.ts:139-153, 260-305)。它对变更做 externals/accepted/declined 分类与依赖图闭包分析 (src/index.ts:66-77, 351-404)，据此清 ESM loadCache 与 CJS require.cache 并重导入插件、重建 fiber，失败时回滚缓存与旧插件 (src/index.ts:471-575)。同一队列也承载 profile 配置文件监视 (`watchConfig` 委托 watch-config.ts，处理尚不存在的路径) (src/index.ts:160-176)，完成后发 `hmr/reload` 事件 (src/index.ts:578)。

## Provides
- ctx.hmr (串行化的模块与配置热重载服务：runExclusive/watchConfig/getLinked/getOuterStack)
- hmr/change 与 hmr/reload 事件，供其它插件感知文件变更与重载批次

## Depends On (上游依赖)
- `cordis-plugin-include` [E1+E2] - 识别 include 配置树并触发其增量刷新，区分配置文件与模块变更
  - 证据: `src/index.ts:6 + src/index.ts:288-298 include.refresh()`
- `cordis-plugin-loader` [E1+E2] - 经 loader.internal 访问 Node ModuleLoader(loadCache)并重建插件 fiber
  - 证据: `src/index.ts:5 + src/index.ts:86-87 @Inject('loader')`
- `cordis-plugin-timer` [E1+E2] - 提供 ctx.debounce，把同一批文件变更合并成一次重载事务
  - 证据: `src/index.ts:13 + src/index.ts:87 @Inject('timer') + src/index.ts:268 ctx.debounce`

## Dependents (下游被依赖)
- `dsh-config-editor` - 配置写入与 HMR 模块/配置重载串行化，避免编辑过程与热重载竞态
- `dsh-plugin-manager` - 配置写入与热重载串行化，并在无 HMR 时降级为 restart-required
