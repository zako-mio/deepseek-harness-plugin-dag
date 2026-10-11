# dsh-hmr

- 包名: `@deepseek-ai/dsh-hmr`
- 分组: G04 启动与插件管理
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/boot/hmr`

## 实现逻辑
实现协调式模块与配置热重载：Hmr 服务以 @Inject 声明 loader/timer 并以 'hmr' 注册(src/index.ts:208-210,301-302)，要求 loader.internal 暴露 Node 模块加载缓存(src/index.ts:304-309)。它把模块变更与 profile 补丁/清单变更统一排入 runExclusive 队列(src/index.ts:262-299)，用 chokidar 监视 root 并把变更分类为 externals(整体重启)/include 刷新/可替换模块(src/index.ts:361-424,470-520)。替换时重新 import 入口模块、删除并重注册受影响插件 fiber，失败则回滚模块缓存与旧插件(src/index.ts:624-722)，成功后 emit hmr/reload(src/index.ts:728)。

## Provides
- ctx.hmr(模块与 profile 配置热重载服务，含 runExclusive/watchConfig，src/index.ts:21-25,207-299)
- 事件 hmr/change 与 hmr/reload(src/index.ts:27-38,410,728)

## Depends On (上游依赖)
- `cordis-plugin-include` [E1+E2] - 对 include 树做局部刷新而非整体重启
  - 证据: `package.json:34 peerDep + src/index.ts:7 import type Include + src/index.ts:407-417 include.refresh()`
- `cordis-plugin-loader` [E1+E2] - 读取模块加载缓存、重新 import 并重注册插件条目
  - 证据: `package.json:33 peerDep + src/index.ts:6 import type ModuleLoader/ModuleJob + src/index.ts:208 @Inject('loader') + src/index.ts:304 this.ctx.loader.internal`
- `cordis-plugin-timer` [E1+E2] - 提供变更合并所需的 debounce 定时能力
  - 证据: `package.json:31 peerDep + src/index.ts:15 import type {} + src/index.ts:209 @Inject('timer') + src/index.ts:382 ctx.debounce`

## Dependents (下游被依赖)
- `dsh-config-editor` - 把配置写入与热重载串行化，避免并发替换
- `dsh-plugin-manager` - 在线 profile 立即应用变更，否则标记需重启
