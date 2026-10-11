# dsh-config-editor

- 包名: `@deepseek-ai/dsh-config-editor`
- 分组: G04 启动与插件管理
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/boot/config-editor`

## 实现逻辑
以 Cordis Service 形式提供 ctx.configEditor(src/index.ts:14-19,26-31)，静态注入 loader/profileContext(src/index.ts:27)。entries() 只挑出 include 树中 id 唯一的条目(src/index.ts:39-44)，configuration() 用 loadProfileDirectory/composeEntries 分离继承值与显式覆盖值(src/index.ts:49-80)。edit() 在 profile package.json 文件锁下重读补丁、经 internal/config waterfall 与 resolveConfig 校验后原子改写 YAML 补丁并 reconcile，失败则回滚(src/index.ts:87-150)；存在 hmr 时整个编辑经 hmr.runExclusive 串行化(src/index.ts:152-153)。

## Provides
- ctx.configEditor(profile 配置持久化编辑服务：entries/configuration/edit，src/index.ts:14-31)

## Depends On (上游依赖)
- `cordis-plugin-include` [编译依赖] - 解析 profile 补丁条目表并识别 include 归属
  - 证据: `package.json:33 peerDep + src/index.ts:6 import entryListSchema/PatchOptions`
- `cordis-plugin-loader` [E1+E2] - 枚举并校验可编辑的 Loader 条目
  - 证据: `package.json:31 peerDep + src/index.ts:8 import type Entry + src/index.ts:27 inject 'loader' + src/index.ts:40 this.ownerContext.loader.entries()`
- `dsh-hmr` [E1+E2] - 把配置写入与热重载串行化，避免并发替换
  - 证据: `package.json:32 peerDep(optional) + src/index.ts:9 import type {} + src/index.ts:152-153 this.ownerContext.get('hmr')/hmr.runExclusive`

## Dependents (下游被依赖)
- `dsh-agent-default-model` - 将默认模型选择持久化写入 profile
- `dsh-settings` - 通过配置编辑器枚举 profile 条目并对其原始文档执行 edit/写回
