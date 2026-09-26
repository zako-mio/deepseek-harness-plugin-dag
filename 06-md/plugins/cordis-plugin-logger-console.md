# cordis-plugin-logger-console

- 包名: `@deepseek-ai/cordis-plugin-logger-console`
- 分组: G46 框架 vendor
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `vendor/logger-console`

## 实现逻辑
控制台日志导出器：ConsoleExporter 基类在 shared 中定义配置与通用实现（src/shared.ts:28-42），Node 面以 util.inspect 与 supports-color 格式化对象（src/index.ts:9-26），browser 面派发原生 console 方法（src/browser.ts:8-15）。

## Provides
- logger-console 导出器（ConsoleExporter，Node 与 browser 双面，src/index.ts:14 / src/browser.ts:8）

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
