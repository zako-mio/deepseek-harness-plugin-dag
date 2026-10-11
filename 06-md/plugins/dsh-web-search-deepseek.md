# dsh-web-search-deepseek

- 包名: `@deepseek-ai/dsh-web-search-deepseek`
- 分组: G46 Web 访问
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/web/web-search-deepseek`

## 实现逻辑
apply() 把 DeepSeekSearchProvider 注册进 ctx.web 的搜索 provider 槽位，provider 的选项由 thunk 每次操作现取，避免一次搜索跨两个配置段落 (src/index.ts:140-144, src/provider.ts:196-203)。resolveOptions 组装凭据与端点：账号令牌优先（仅当最新 request context 的 provider 为 deepseek-account 时向 ctx.get('deepseekAccount') 解析），否则回落 credentials 服务或启动环境里的 DEEPSEEK_API_KEY，端点独立于 $DEEPSEEK_BASE_URL 而走 DEEPSEEK_SEARCH_BASE_URL (src/index.ts:99-137)。search() 以 Anthropic 兼容 Messages API + 原生 web_search_20250305 工具发一次模型调用，把 web_search_tool_result 的条目与 text 块 citations 里的 cited_text 按 url 合并成 sources，无结果块则报 WEB_PROVIDER_ERROR (src/provider.ts:213-292, src/provider.ts:126-137, src/provider.ts:150-179)。分发前的脱敏请求会先 append 成 web/deepseek-search-llm-request 事件 (src/provider.ts:79-84, src/index.ts:130-135)。

## Provides
- ctx.web (注册 id 为 `deepseek-official` 的 WebSearchProvider：经 DeepSeek Anthropic 兼容 Messages API 的原生 web_search 实现检索)

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - 从当前发起者会话读取 request context 的 provider，决定是否走账号令牌路径；并作为事件记录归属
  - 证据: `package.json:30 peerDep + src/index.ts:13 import type {} + src/index.ts:111 ctx.get('agents')?.currentInitiator()`
- `dsh-session` [编译依赖] - 把分发前的脱敏请求作为 session 事件留痕，使模型可见的辅助输入不会逃逸日志
  - 证据: `package.json:34 peerDep + src/index.ts:17 import type {} + src/provider.ts:79-84 declare module '@deepseek-ai/dsh-session/types' 增补 web/deepseek-search-llm-request`
- `dsh-web` [E1+E2] - 实现 WebSearchProvider 契约、复用 WebError 错误词汇，并注册进搜索 provider 注册表
  - 证据: `package.json:35 peerDep + src/index.ts:18 import type {} + src/provider.ts:9 import { WebError } + src/index.ts:141 ctx.web.registerSearchProvider`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
