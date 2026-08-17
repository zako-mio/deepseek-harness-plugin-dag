# dsh-web

- 包名: `@deepseek-ai/dsh-web`
- 分组: G24 Web搜索
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/web/web`

## 为什么需要它（设计初衷）
网页能力族：把搜索与抓取合并到单一 provider 选择缝（ctx.web），并提供 provider 中立（Exa/Perplexity/DeepSeek 原生/HTTP fetch）以及模型面对工具 web_search/web_fetch。解耦「提供者」与「消费工具」——换一次 provider 全产品切换，且工具可见性不依赖后端可用性（enablement 而非 availability）。

发展史：2026-06-24 web capability seam 决策记录为何搜索与抓取共享一个 provider 选择服务；明确推迟 SSRF 防护。工具侧演化出 web result card 渲染。

来源：
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/web
- https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/implemented/architecture/2026-06-24-web-capability-seam.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/web.md

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
