# dsh-web-search-perplexity

- 包名: `@deepseek-ai/dsh-web-search-perplexity`
- 分组: G47 Web 访问
- 拓扑层: Layer 3
- 来源层: L3 其余
- 源码路径: `packages/web/web-search-perplexity`

## 实现逻辑
函数插件把 PerplexitySearchProvider 注册进 ctx.web（id 'perplexity'，src/index.ts:52-61）。provider 以 POST /chat/completions 调用 sonar 模型 (src/provider.ts:101-152)，把生成答案作为 content，来源优先结构化 search_results[]、缺失时回退为仅 URL 的 citations[] (src/provider.ts:73-83)。API key 缺省从 launchEnvironmentOf(ctx).get('PERPLEXITY_API_KEY') 取得。

## Provides
- ctx.web 的 search provider 'perplexity' (Perplexity 生成式检索)

## Depends On (上游依赖)
- `dsh-web` [E1+E2] - 实现并注册 WebSearchProvider 到 web seam
  - 证据: `package.json:31 peerDep + src/provider.ts:9 import { WebError } + src/index.ts:27 static inject ['web'] + src/index.ts:53 ctx.web.registerSearchProvider`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
