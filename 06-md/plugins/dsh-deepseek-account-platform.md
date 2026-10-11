# dsh-deepseek-account-platform

- 包名: `@deepseek-ai/dsh-deepseek-account-platform`
- 分组: G10 凭据与授权
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/credentials/deepseek-account-platform`

## 实现逻辑
DeepSeekAccount 的平台实现：用 PKCE 授权码流在本机注册 /oauth/callback 路由，state 以 timingSafeEqual 定长校验，拿到 code 后换 token 并以 grant 记录提交给 credentials (src/index.ts:522-612, src/index.ts:539-558)。构造时向 authorization 注册 key 为 deepseek-account-platform/default 的 flow，并监听 credentials/record-updated 失效详情缓存 (src/index.ts:138-151)。profile/balance/未通知奖励经 zod 校验的平台 HTTP 端点读取，401 或业务码 40003 视为凭据过期，删记录并发 deepseek-account/session-expired (src/index.ts:296-315, src/index.ts:329-344, src/protocol.ts:166-234)。登出先删本地记录再后台按指数退避重试撤销 token，撤销失败不恢复本地凭据 (src/index.ts:463-482, src/logout.ts:21-36)。

## Provides
- ctx.deepseekAccount 的平台实现 (浏览器 PKCE 登录、profile/balance/bonus 查询、登出撤销)
- authorization flow: deepseek-account-platform/default
- deepseek-account/session-expired 与 deepseek-account/signed-out 事件

## Depends On (上游依赖)
- `dsh-authorization` [E1+E2] - 登录流程以 authorization flow 形式注册，取消与单飞语义由该 seam 保证
  - 证据: `src/index.ts:12 import type { AuthorizationSession } + src/index.ts:138 ctx.authorization.registerFlow + src/index.ts:426 ctx.authorization.begin + package.json:37 peerDep`
- `dsh-host-webserver` [E1+E2] - 浏览器回调需要宿主 HTTP 服务器上的一个精确路由
  - 证据: `src/index.ts:4 import type {} from '@deepseek-ai/dsh-host-webserver' + src/index.ts:523 ctx.get('webServer') + src/index.ts:539 webServer.register({ kind: 'exact', path: '/oauth/callback' }) + package.json:39 peerDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
