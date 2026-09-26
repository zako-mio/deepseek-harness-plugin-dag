# dsh-deepseek-llm-api-extensions

- 包名: `@deepseek-ai/dsh-deepseek-llm-api-extensions`
- 分组: G23 LLM 适配
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/llm/deepseek-llm-api-extensions`

## 实现逻辑
定义并暴露 ctx.deepseekLlmApiExtensions 服务，作为官方 DeepSeek 请求顶层字段的扩展注册表 (src/index.ts:66-71, 18-22)。register() 以 ctx.effect 让插件按字段名注册唯一 provider 并在释放时撤销 (src/index.ts:79-99)。prepare() 在 HTTP 派发前并发调用各 provider 准备字段、对取值做结构化克隆并冻结，并把各 provider 的 accept 回调收拢为幂等的联合提交事务，支持中止传播 (src/index.ts:108-129)。types.ts 用声明合并声明可扩展字段表与 provider 协议 (src/types.ts:16, 39-48)。

## Provides
- ctx.deepseekLlmApiExtensions (DeepSeek 顶层请求字段扩展注册表，供 plugin-package-inventory-deepseek 等贡献独立字段)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-plugin-package-inventory-deepseek` - 把插件包清单作为独立顶层字段注册进 DeepSeek 请求扩展注册表
- `dsh-session-log-deepseek` - 把 dsh_session_log 字段注册到官方 DeepSeek 请求扩展点
