# dsh-web-search-exa

- 包名: `@deepseek-ai/dsh-web-search-exa`
- 分组: G47 Web 访问
- 拓扑层: Layer 3
- 来源层: L3 其余
- 源码路径: `packages/web/web-search-exa`

## 实现逻辑
函数插件把 ExaSearchProvider 注册进 ctx.web（id 'exa'，src/index.ts:57-66）。provider 以 POST /search 携带 highlights 请求 Exa (src/provider.ts:96-149)，把首个非空 highlight 映射为 snippet、publishedDate→publishedAt，并丢弃无 snippet 的条目 (src/provider.ts:56-81)。API key 缺省从 launchEnvironmentOf(ctx).get('EXA_API_KEY') 取得。

## Provides
- ctx.web 的 search provider 'exa' (Exa 检索)

## Depends On (上游依赖)
- `dsh-web` [E1+E2] - 实现并注册 WebSearchProvider 到 web seam
  - 证据: `package.json:31 peerDep + src/provider.ts:9 import { WebError } + src/index.ts:32 static inject ['web'] + src/index.ts:58 ctx.web.registerSearchProvider`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
