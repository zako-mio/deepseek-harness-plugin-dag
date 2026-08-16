# cordis-plugin-timer

- 包名: `@deepseek-ai/cordis-plugin-timer`
- 分组: G01 运行时框架
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: ``

## 实现逻辑
Vendored 的 cordis 官方定时器服务插件(框架层基础能力)。定义 TimerService 类(extends Service，注册名 'timer')，通过 ctx.mixin 把 timeout/interval/throttle/debounce/setTimeout/setInterval 六个方法混入 Context，全部基于 ctx.effect 建立 fiber 生命周期绑定(context 销毁自动清理)。

## Provides
- ctx.timer (TimerService)
- ctx.timeout()/interval()/throttle()/debounce()/setTimeout()/setInterval() 六个 mixin
- Context 类型声明扩展

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `cordis-plugin-hmr` - static inject timer; ctx.debounce
