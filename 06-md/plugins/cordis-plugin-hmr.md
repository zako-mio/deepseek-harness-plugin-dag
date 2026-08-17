# cordis-plugin-hmr

- 包名: `@deepseek-ai/cordis-plugin-hmr`
- 分组: G01 运行时框架
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: ``

## 为什么需要它（设计初衷）
Cordis 客户端插件热重载：浏览器经 SSE 按 rebuilt 帧重载单插件，node 端轮询统计重构建，无需整页刷新。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/hmr/README.md
- https://www.npmjs.com/package/cordis-plugin-hmr

## 实现逻辑
Vendored 的 cordis 官方热更新插件(框架层)。Hmr 类(Service 'hmr')static inject=['loader','timer']。(1) registerConfig 对配置树外精确路径起 chokidar watcher；(2) [Service.init] 对 root/ignored 建全局 watcher，external 文件触发 loader.exit() 全量重载；(3) partialReload 通过 loadCache 依赖图分析把变更分类 accepted/declined，重 import 插件入口，失败 rollback。

## Provides
- ctx.hmr (Hmr 服务)
- ctx.hmr.registerConfig()
- 事件 hmr/change|hmr/reload|hmr/config-update-failed

## Depends On (上游依赖)
- `cordis-plugin-timer` [运行时依赖] - static inject timer; ctx.debounce
  - 证据: `vendor/hmr/src/index.ts:87,242`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
