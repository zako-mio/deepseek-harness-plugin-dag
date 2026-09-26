# dsh-tool-web

- 包名: `@deepseek-ai/dsh-tool-web`
- 分组: G47 Web 访问
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/web/tool-web`

## 实现逻辑
以函数插件在 ctx.tools 上注册模型可见的 web_search 与 web_fetch 工具：Config 控制启用项与上限，apply() 据配置分派到 applyWebSearchTool/applyWebFetchTool (src/index.ts:83-95)。web_fetch 经 ctx.web.fetch 抓取 URL，用 turndown + GFM 把 HTML 转为 markdown，并对深层嵌套 HTML 做深度守卫 (src/fetch.ts:25-95, 447-515)。web_search 校验查询上限后并发调用 ctx.web.search 并合并去重、按结果上限截断 (src/search.ts:231-377)。两者都注册 systemPrompt 信任提示（外部内容视为数据而非指令，src/trust.ts:7）并附可回放的结果卡片元数据。

## Provides
- tools.web_search (模型可见的联网搜索工具，经 ctx.web 执行)
- tools.web_fetch (模型可见的 URL 抓取并转 markdown 的工具)
- systemPrompt 章节 tool:web_search / tool:web_fetch (外部内容信任与引用指引)

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 声明式 peer 依赖（模型消息/类型兼容面）
  - 证据: `package.json:31 peerDep`
- `dsh-system-prompt` [E1+E2] - 注册工具使用与外部内容信任指引的 system prompt 章节
  - 证据: `package.json:32 peerDep + src/index.ts:24 inject 'systemPrompt' + src/fetch.ts:448 ctx.systemPrompt.section`
- `dsh-tools` [E1+E2] - 通过 ctx.tools 注册 web_search/web_fetch 工具定义（含 schema、render、presentationMeta）
  - 证据: `package.json:33 peerDep + src/fetch.ts:11 import defineTool + src/index.ts:24 static inject ['tools','web','systemPrompt']`
- `dsh-web` [E1+E2+E3] - 调用 ctx.web 执行实际抓取/搜索，且 base bundle 中装配在 web 行之后
  - 证据: `package.json:34 peerDep + src/fetch.ts:13 import WebFetchBody/WebFetchResult + src/index.ts:24 inject 'web' + src/fetch.ts:501 ctx.web.fetch + packages/bundle/base/cordis.patch.yml:471-486`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
