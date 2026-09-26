# dsh-web-search-deepseek

- 包名: `@deepseek-ai/dsh-web-search-deepseek`
- 分组: G47 Web 访问
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/web/web-search-deepseek`

## 实现逻辑
函数插件把 DeepSeekSearchProvider 注册进 ctx.web（id 'deepseek-official'，src/index.ts:127-131）。provider 调用 Anthropic 兼容 Messages API 并携带原生 web_search_20250305 服务端工具 (src/provider.ts:199-278)，把 web_search_tool_result 块与 text 引文按 URL 合并为规范化来源 (src/provider.ts:120-173)。凭证与端点由 resolveOptions 从 ctx.get('credentials')/launchEnvironmentOf 解析，并在派发前把无密请求写入调用方会话 (src/index.ts:93-124)。

## Provides
- ctx.web 的 search provider 'deepseek-official' (DeepSeek 官方联网搜索)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 通过 ctx.get('agents') 找到当前发起方 Agent，以记录辅助搜索请求
  - 证据: `package.json:32 peerDep + src/index.ts:11 import type {} from dsh-agent (声明合并) + src/index.ts:118 ctx.get('agents')?.currentInitiator()`
- `dsh-session` [E1+E2] - 向会话日志记录搜索请求（模型可见输入须可重建），并声明对应 SessionEventMap 事件
  - 证据: `package.json:35 peerDep + src/index.ts:14 import type {} from dsh-session + src/provider.ts:79 declare module SessionEventMap + src/index.ts:118 session.append('web/deepseek-search-llm-request', ...)`
- `dsh-web` [E1+E2+E3] - 实现并注册 WebSearchProvider 到 web seam，base bundle 中装配在 web 行之后
  - 证据: `package.json:36 peerDep + src/provider.ts:9 import { WebError } + src/index.ts:41 static inject ['web'] + src/index.ts:128 ctx.web.registerSearchProvider + packages/bundle/base/cordis.patch.yml:471-478`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
