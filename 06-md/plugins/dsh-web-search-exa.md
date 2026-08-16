# dsh-web-search-exa

- 包名: `@deepseek-ai/dsh-web-search-exa`
- 分组: G34 Web上下文扩展
- 拓扑层: Layer 4
- 来源层: L3 其余
- 源码路径: `packages/web/web-search-exa`

## 实现逻辑
Exa 搜索 provider：src/index.ts apply() 经 launchEnvironmentOf(ctx).get('EXA_API_KEY') 从启动环境取 key（config 可覆盖），填默认 baseURL=api.exa.ai/searchType=auto/highlightsPerResult=1，构造 ExaSearchProvider 后 ctx.web.registerSearchProvider() 注册（inject ['web']）。provider.ts：EXA_PROVIDER_ID='exa'；available() 要求 apiKey 非空 + baseURL 合法 + 正数约束；search() POST /search（highlightsPerUrl 参数），mapExaResponse 将 results[] 归一化：首个非空 highlight→snippet、publishedDate→publishedAt，无 snippet 的条目丢弃（seam 无其他字段可派生），Exa 无生成答案故省略 content、truncated:false。映射顺序/裁剪语义与 dsh-web-search-deepseek 同模式（注册进 seam 的 search 注册表，不拥有 ctx.web 键）。

## Provides
- ctx.web.registerSearchProvider 注册的 'exa' 后端（WebSearchProvider id='exa'）
- EXA_PROVIDER_ID/EXA_DEFAULT_BASE_URL/EXA_DEFAULT_SEARCH_TYPE/EXA_DEFAULT_HIGHLIGHTS_PER_RESULT 常量
- ExaSearchProvider 类（search: WebSearchRequest→WebSearchResult）
- Exa 搜索归一化映射（highlight→snippet, publishedDate→publishedAt）

## Depends On (上游依赖)
- `dsh-web` [编译依赖] - Web seam 能力缝：registerSearchProvider 注册 API + WebSearchProvider 接口契约
  - 证据: `packages/web/web-search-exa/src/provider.ts:9-15 WebError + WebSearchProvider/WebSearchRequest/WebSearchResult/WebSearchSource；index.ts:61 ctx.web.registerSearchProvider`
- `dsh-web-search-deepseek` [组合依赖] - 搜索 provider 参照实现：注册方式/归一化语义/装配路径同模式
  - 证据: `同 web seam 注册表模式（web/src/index.ts:103 registerSearchProvider）；tool-web/tests/integration.spec.ts:41 以 EXA_PROVIDER_ID 装配`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
