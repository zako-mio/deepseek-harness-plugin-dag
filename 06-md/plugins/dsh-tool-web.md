# dsh-tool-web

- 包名: `@deepseek-ai/dsh-tool-web`
- 分组: G24 Web搜索
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/web/tool-web`

## 为什么需要它（设计初衷）
给模型提供 Web 工具（web_search/web_fetch），封装 ctx.web 能力 seam，用 turndown+GFM 插件把 HTML 转 Markdown 供模型读取。

发展史：RC8 web_search 支持并发查询(最多4个)

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-tool-web
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/web/tool-web/README.zh.md

## 实现逻辑
search.ts:22-29 新增 WEB_SEARCH_MAX_QUERIES=4 与 WebSearchArgs.queries 数组; parseSearchArgs 校验queries非空/上限/去重。:220-296 新增 runSearchQueries: 多query用 Promise.allSettled 并发执行(ctx.web.search)，任一失败abort兄弟查询并等全部settle后抛首个错误; mergeSearchResults round-robin去重合并并封顶maxResults。

## Provides
- 模型工具 web_search/web_fetch
- systemPrompt sections tool:web_search
- presentation meta: WebSearchMeta/WebFetchMeta

## Depends On (上游依赖)
- `dsh-llm` [组合依赖] - ContentBlock/assertNever 类型
  - 证据: `packages/web/tool-web/src/index.ts:37`
- `dsh-system-prompt` [编译依赖] - systemPrompt.section
  - 证据: `packages/web/tool-web/src/index.ts:24`
- `dsh-tool-call-timeout-policy` [运行时依赖] - timeoutMs 交策略强制
  - 证据: `packages/web/tool-web/src/index.ts:75-78`
- `dsh-tools` [编译依赖] - defineTool + register
  - 证据: `packages/web/tool-web/src/index.ts:24`
- `dsh-web` [编译依赖] - ctx.web.search/fetch
  - 证据: `packages/web/tool-web/src/index.ts:24,261`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
