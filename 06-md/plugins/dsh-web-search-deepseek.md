# dsh-web-search-deepseek

- 包名: `@deepseek-ai/dsh-web-search-deepseek`
- 分组: G24 Web搜索
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/web/web-search-deepseek`

## 实现逻辑
DeepSeek 官方搜索 provider：apply 通过 ctx.web.registerSearchProvider 注册 id='deepseek-official'。search() 每次操作快照 options 后向 Anthropic 兼容 Messages API 发原生 web_search_20250305 工具请求，mapAnthropicResponse 合并引用为 WebSearchResult；apiKey 经 dsh-credentials resolveApiKey 解析，并把脱密请求体记入 session 事件 'web/deepseek-search-llm-request'。

## Provides
- ctx.web 搜索 provider 'deepseek-official'
- settings 段 web-search-deepseek
- Session 事件 web/deepseek-search-llm-request

## Depends On (上游依赖)
- `dsh-agent` [组合依赖] - currentInitiator 归属
  - 证据: `packages/web/web-search-deepseek/package.json:35`
- `dsh-session` [编译依赖] - session.append 记录搜索请求
  - 证据: `packages/web/web-search-deepseek/src/index.ts:14,117-122`
- `dsh-web` [编译依赖] - registerSearchProvider + WebError
  - 证据: `packages/web/web-search-deepseek/src/index.ts:41,137`

## Dependents (下游被依赖)
- `dsh-web-search-exa` - 搜索 provider 参照实现：注册方式/归一化语义/装配路径同模式
- `dsh-web-search-perplexity` - 搜索 provider 参照实现（同 dsh-web-search-exa 的变体）
