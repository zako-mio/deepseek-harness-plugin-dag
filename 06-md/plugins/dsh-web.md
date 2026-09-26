# dsh-web

- 包名: `@deepseek-ai/dsh-web`
- 分组: G47 Web 访问
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/web/web`

## 实现逻辑
WebRuntime 服务 (src/index.ts:74-164) 作为 ctx.web 能力 seam：持有 search/fetch 两个 provider 注册表，暴露 registerSearchProvider/registerFetchProvider (src/index.ts:103-116)。search()/fetch() 在调用时经 resolveProvider 做与注册顺序无关的选择（配置缺失→WEB_PROVIDER_CONFIGURED_MISSING、多个可用→WEB_PROVIDER_AMBIGUOUS 等，src/index.ts:172-194），并按 maxResults 截断结果并置 truncated (src/index.ts:196-200)。types.ts 定义请求/结果词汇、provider 接口与 WebError 分类 (src/types.ts:35-130)，并以默认导出满足服务类插件约定 (src/index.ts:202)。

## Provides
- ctx.web (Web 访问能力 seam：search/fetch provider 注册表与与注册顺序无关的选择)
- WebError 错误分类与 WebSearch/WebFetch 请求结果词汇

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 以 dsh-llm 的 HarnessError 为基类定义 WebError，保持全仓错误分类一致
  - 证据: `package.json:30 peerDep + src/types.ts:8 import { HarnessError }`

## Dependents (下游被依赖)
- `dsh-tool-web` - 调用 ctx.web 执行实际抓取/搜索，且 base bundle 中装配在 web 行之后
- `dsh-web-fetch-http` - 实现并注册 WebFetchProvider 到 web seam，base bundle 中装配在 web 行之后
- `dsh-web-search-deepseek` - 实现并注册 WebSearchProvider 到 web seam，base bundle 中装配在 web 行之后
- `dsh-web-search-exa` - 实现并注册 WebSearchProvider 到 web seam
- `dsh-web-search-perplexity` - 实现并注册 WebSearchProvider 到 web seam
