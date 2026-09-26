# schemastery

- 包名: `@deepseek-ai/schemastery`
- 分组: G46 框架 vendor
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `vendor/schemastery`

## 实现逻辑
类型驱动的 schema 校验器：Schema 工厂与 Schema 类做值校验、默认值填充与类型推断（src/index.ts:42-50, 254），默认导出供 z(...) 调用（src/index.ts:962）。它基于 cosmokit 的原语（Binary/clone/deepEqual/volatile 等）实现 schema 组合与序列化简写（src/index.ts:1-2, 5-6）。

## Provides
- Schema / z(...) 类型驱动校验器（默认导出，src/index.ts:962）

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
