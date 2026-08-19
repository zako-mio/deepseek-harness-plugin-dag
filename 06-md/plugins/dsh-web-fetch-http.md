# dsh-web-fetch-http

- 包名: `@deepseek-ai/dsh-web-fetch-http`
- 分组: G34 Web上下文扩展
- 拓扑层: Layer 2
- 来源层: L3 其余
- 源码路径: `packages/web/web-fetch-http`

## 为什么需要它（设计初衷）
匿名公共 HTTP(S) WebFetchProvider，web 能力 seam(ctx.web) 的实现包。负责安全资源获取（URL 校验、重定向策略、超时、字节上限、charset 解码、二进制拒绝）；SSRF/私有网络防护明确列为暂缓事项，注明是 SSRF 原语，敏感内网部署禁止启用。

发展史：位于 packages/web/web-fetch-http，2026-08-10 首批发布，0.1.0-rc.6 转公开。与 dsh-tool-web（呈现）职责分离；属于实现包，注册 ctx.web 提供方但不拥有该键、不注册模型工具。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/web/web-fetch-http/README.zh.md
- https://registry.npmjs.org/@deepseek-ai/dsh-web-fetch-http

## 实现逻辑
匿名公开 HTTP(S) WebFetchProvider：src/index.ts apply() 以 schemastery Config 校验并填充限额（maxUrlLength=2048/maxResponseBytes=5MB/maxBodyChars=100k/timeoutMs=30s/maxRedirects=5/userAgent），构造 HttpFetchProvider 后 ctx.web.registerFetchProvider() 注册进 ctx.web 的 fetch 注册表（inject ['web']）。provider.ts 实现 WebFetchProvider：available() 恒 true（匿名无凭证）；fetch() 用 dsh-timeout 的 deadline 建立统一 abort 信号（WEB_FETCH_TIMEOUT）；followAndRead() 手动跟随仅同源重定向（maxRedirects 预算 + isSameOrigin 校验，跨源即 WEB_REDIRECT_BLOCKED）；requestOnce() 用 redirect:'manual' + 显式 User-Agent（deepseek-harness 产品代理，非浏览器伪装）；readBody() 按 content-type 分类（html/text）、parseCharset+decoderForCharset 解码、maxResponseBytes 截断字节与 maxBodyChars 截断字符并标记 truncated。注释明确：无私网/SSRF 保护，不可在能触达敏感内部目标的环境启用。函数/命名空间插件，不拥有 ctx.web 键，仅向 seam 注册。

## Provides
- ctx.web.registerFetchProvider 注册的 'http' 后端（WebFetchProvider id='http'）
- LOCAL_FETCH_PROVIDER_ID 常量
- HttpFetchProvider 类（fetch: WebFetchRequest→WebFetchResult）
- 匿名公开 HTTP(S) 抓取能力（无凭证/无 cookie）

## Depends On (上游依赖)
- `dsh-web` [编译依赖] - Web seam 能力缝：registerFetchProvider 注册 API + WebFetchProvider 接口/WebError 契约
  - 证据: `packages/web/web-fetch-http/src/index.ts:12 import type {} from '@deepseek-ai/dsh-web'；provider.ts:11-12 WebError/WebFetchProvider/WebFetchRequest/WebFetchResult；src/index.ts:100 ctx.web.registerFetchProvider`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
