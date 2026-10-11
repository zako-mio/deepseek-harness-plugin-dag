# dsh-deepseek-llm-api-extensions

- 包名: `@deepseek-ai/dsh-deepseek-llm-api-extensions`
- 分组: G22 LLM 适配
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/llm/deepseek-llm-api-extensions`

## 实现逻辑
官方 DeepSeek 请求顶层扩展字段的注册表：register(field, provider) 以 effect 作用域保证一个字段只有一个所有者，字段名必须非空且已 trim (src/index.ts:81-101)。prepare() 并发调用各 provider 的 prepare，把返回值结构化克隆后递归冻结并合并为字段集；单个字段准备失败或不可克隆时从本次请求中省略，且每个字段只告警一次 (src/index.ts:111-141)。accept() 在 HTTP 2xx 后用 Promise.allSettled 统一结算各 provider 的接受回调，单错直接抛、多错抛 AggregateError；重复调用复用同一结算 promise (src/index.ts:41-48, src/index.ts:136-140)。整体准备以 abortable 与请求信号竞速，只有取消会拒绝 (src/index.ts:51-63, src/index.ts:112-125)。

## Provides
- ctx.deepseekLlmApiExtensions (DeepSeekLlmApiExtensionRegistry：顶层请求字段注册与准备/接受事务)
- 类型出口 DeepSeekLlmApiExtensionMap 与 provider 契约（供插件声明合并自有字段）

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-plugin-package-inventory-deepseek` - 字段必须注册进扩展注册表才会并入官方 DeepSeek 请求
- `dsh-session-log-deepseek` - 注册并参与构建 DeepSeek 请求的扩展字段
