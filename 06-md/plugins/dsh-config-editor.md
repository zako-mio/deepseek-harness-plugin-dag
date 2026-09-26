# dsh-config-editor

- 包名: `@deepseek-ai/dsh-config-editor`
- 分组: G04 启动与插件管理
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/boot/config-editor`

## 实现逻辑
`ConfigEditor extends Service` 提供对当前 profile patch 文件的持久化配置编辑能力 (src/index.ts:26-31)。`entries()` 筛出由 `include` 父树拥有且 id 唯一的可寻址行 (src/index.ts:39-44)，`configuration()` 用 `loadProfileDirectory`+`composeEntries` 同时给出继承层值与显式覆盖值 (src/index.ts:49-68)。`edit()` 在文件锁下校验目标行仍在册、经 `waterfall('internal/config')`+`resolveConfig` 预演新配置、用 yaml AST 精确改写对应行，写盘后调用 `reconcileProfilePatches` 触发 Loader 重载，失败则回滚文件与 patch (src/index.ts:75-142)。

## Provides
- ctx.configEditor (对活动 profile 插件配置的持久化编辑服务：entries/configuration/edit)
- 基于 YAML AST 的配置行改写与写盘回滚 (保留 __jsExpr 等自定义标签)

## Depends On (上游依赖)
- `cordis-plugin-include` [编译依赖] - 复用 entryListSchema 与 PatchOptions 类型解析 profile patch 的 entry 列表
  - 证据: `src/index.ts:6`
- `cordis-plugin-loader` [E1+E2] - 读取 loader.entries() 定位可编辑行，并在写盘后走正常 Loader 重载路径
  - 证据: `src/index.ts:8 + src/index.ts:27 static inject 'loader'`
- `dsh-hmr` [运行时依赖] - 配置写入与 HMR 模块/配置重载串行化，避免编辑过程与热重载竞态
  - 证据: `src/index.ts:9 (type merge) + src/index.ts:140-141 ctx.get('hmr').runExclusive`

## Dependents (下游被依赖)
- `dsh-agent-default-model` - 将默认模型选择持久化写入 profile
- `dsh-settings` - 通过配置编辑器枚举 profile 条目并对其原始文档执行 edit/写回
