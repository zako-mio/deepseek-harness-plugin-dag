# dsh-web-search-perplexity

- 包名: `@deepseek-ai/dsh-web-search-perplexity`
- 分组: G34 Web上下文扩展
- 拓扑层: Layer 4
- 来源层: L3 其余
- 源码路径: `packages/web/web-search-perplexity`

## 为什么需要它（设计初衷）
Perplexity 驱动的搜索提供方，web capability seam 的替代实现。

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-web-search-perplexity
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/web/web-search-perplexity

## 实现逻辑
Perplexity 搜索 provider：src/index.ts apply() 经 launchEnvironmentOf(ctx).get('PERPLEXITY_API_KEY') 取 key，默认 baseURL=api.perplexity.ai/model=sonar/maxTokens=1024，可选 searchRecency（day/week/month/year→search_recency_filter），构造 PerplexitySearchProvider 后 ctx.web.registerSearchProvider() 注册（inject ['web']）。provider.ts：PERPLEXITY_PROVIDER_ID='perplexity'；search() 调 /chat/completions，模型返回生成答案→content，结果经 citations/sources 归一化为 WebSearchSource；available() 要求 apiKey+baseURL+maxTokens 正数。与 dsh-web-search-exa/deepseek 同为注册进 ctx.web search 注册表的 provider 变体。

## Provides
- ctx.web.registerSearchProvider 注册的 'perplexity' 后端（WebSearchProvider id='perplexity'）
- PERPLEXITY_PROVIDER_ID/PERPLEXITY_DEFAULT_BASE_URL/PERPLEXITY_DEFAULT_MODEL/PERPLEXITY_DEFAULT_MAX_TOKENS 常量
- PerplexitySearchProvider 类（含 search_recency_filter 支持）
- Perplexity 搜索归一化（生成答案→content + 引文 sources）

## Depends On (上游依赖)
- `dsh-web` [编译依赖] - Web seam 能力缝：registerSearchProvider 注册 API + 搜索接口契约
  - 证据: `packages/web/web-search-perplexity/src/provider.ts:9-15 WebError + WebSearchProvider 契约；index.ts:55 ctx.web.registerSearchProvider`
- `dsh-web-search-deepseek` [组合依赖] - 搜索 provider 参照实现（同 dsh-web-search-exa 的变体）
  - 证据: `同 seam 注册表模式（web/src/index.ts:103 registerSearchProvider）与归一化语义参照`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
