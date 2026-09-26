# dsh-web-fetch-http

- 包名: `@deepseek-ai/dsh-web-fetch-http`
- 分组: G47 Web 访问
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/web/web-fetch-http`

## 实现逻辑
函数插件 apply() 构造 HttpFetchProvider 并通过 ctx.web.registerFetchProvider 注册为 fetch provider 'http' (src/index.ts:79-93，id 见 src/provider.ts:36-40)。provider.fetch 用 deadline 施加超时 (src/provider.ts:56-63)，validateFetchUrl 校验 URL 并只跟随同源重定向 (src/provider.ts:66-115)，经 publicHttpNetwork 解析并固定公共 IP、可选择走 dsh-http-proxy 代理 (src/provider.ts:134-139)。readBody 按字节/字符上限截断并按 charset 解码 (src/provider.ts:147-177)。

## Provides
- ctx.web 的 fetch provider 'http' (匿名公共 HTTP(S) 安全抓取实现)

## Depends On (上游依赖)
- `dsh-web` [E1+E2+E3] - 实现并注册 WebFetchProvider 到 web seam，base bundle 中装配在 web 行之后
  - 证据: `package.json:32 peerDep + src/provider.ts:9 import { WebError } + src/index.ts:29 static inject ['web'] + src/index.ts:93 ctx.web.registerFetchProvider + packages/bundle/base/cordis.patch.yml:471-483`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
