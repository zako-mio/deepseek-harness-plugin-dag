# cordis-plugin-timer

- 包名: `@deepseek-ai/cordis-plugin-timer`
- 分组: G46 框架 vendor
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `vendor/timer`

## 实现逻辑
可随 fiber 处置的计时器服务：TimerService 注册 ctx.timer 并把 timeout/interval/throttle/debounce 混入 Context（src/index.ts:12-16）。每个计时器经 ctx.effect 在作用域处置时自动清理（src/index.ts:28-54），interval 另提供异步迭代器形态（src/index.ts:57-104）。

## Provides
- ctx.timer / ctx.timeout / ctx.interval / ctx.throttle / ctx.debounce（随 fiber dispose 的计时器服务，src/index.ts:12-16）

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-hmr` - 提供 ctx.debounce，把同一批文件变更合并成一次重载事务
