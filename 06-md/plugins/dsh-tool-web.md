# dsh-tool-web

- 包名: `@deepseek-ai/dsh-tool-web`
- 分组: G24 Web搜索
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/web/tool-web`

## 实现逻辑
模型可见 web 工具套件：apply 按 config 决定注册 web_search(经 ctx.web.search 执行并投影 WebSearchResult)与 web_fetch(经 ctx.web.fetch 执行后由 turndown 把 HTML 转 markdown，带深度上限)。两工具把 config 的 timeoutMs 附到 ToolDefinition.timeoutMs 交 timeout-policy 强制。

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
