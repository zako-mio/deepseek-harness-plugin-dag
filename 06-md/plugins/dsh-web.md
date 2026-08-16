# dsh-web

- 包名: `@deepseek-ai/dsh-web`
- 分组: G24 Web搜索
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/web/web`

## 实现逻辑
web 能力缝服务定义：WebRuntime extends Service 注册为 ctx.web，维护 searchProviders/fetchProviders 两个命名注册表。search()/fetch() 在调用时按配置 id→注册→available() 优先级解析唯一 provider，无配置时恰好一个可用自动选中；search 结果按 maxResults 截断。

## Provides
- ctx.web(WebRuntime)
- registerSearchProvider/registerFetchProvider
- WebError 错误分类学
- searchProvider/fetchProvider 选择配置

## Depends On (上游依赖)
- `dsh-llm` [组合依赖] - 类型/错误基类声明依赖
  - 证据: `packages/web/web/package.json:36`

## Dependents (下游被依赖)
- `dsh-tool-web` - ctx.web.search/fetch
- `dsh-web-fetch-http` - Web seam 能力缝：registerFetchProvider 注册 API + WebFetchProvider 接口/WebError 契约
- `dsh-web-search-deepseek` - registerSearchProvider + WebError
- `dsh-web-search-exa` - Web seam 能力缝：registerSearchProvider 注册 API + WebSearchProvider 接口契约
- `dsh-web-search-perplexity` - Web seam 能力缝：registerSearchProvider 注册 API + 搜索接口契约
