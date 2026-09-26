# dsh-deepseek-account-platform

- 包名: `@deepseek-ai/dsh-deepseek-account-platform`
- 分组: G10 凭据与授权
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/credentials/deepseek-account-platform`

## 实现逻辑
`PlatformAccount` 继承 `DeepSeekAccount`（src/index.ts:84-85），以 PKCE 实现 DeepSeek Platform 网页登录：注册 authorization flow（src/index.ts:138-146），`run()` 生成 verifier/challenge+state、在 webServer 注册 `/oauth/callback` 时序安全校验回调、交换 token 后经 `session.commit` 写 grant 记录（src/index.ts:509-599）。grant 以 issuer 绑定 provider origin，失效或拒 token 即删除记录并广播 `deepseek-account/session-expired`/`signed-out`（src/index.ts:329-344、372-388）。profile/余额/未通知奖励经 `details.ts`/`protocol.ts` 的 zod 校验与 65KB 响应上限读取（src/details.ts:62-70、src/protocol.ts:166-234）。

## Provides
- ctx.credentials 记录 (deepseek-account-platform/default 与 /device 的 grant)
- 事件 deepseek-account/session-expired, deepseek-account/signed-out

## Depends On (上游依赖)
- `dsh-authorization` [E1+E2] - 把浏览器 PKCE 登录注册为授权流程并驱动一次尝试
  - 证据: `src/index.ts:12 import AuthorizationSession + src/index.ts:85 inject + src/index.ts:138 registerFlow + src/index.ts:413 begin`
- `dsh-host-webserver` [E1+E2] - 注册 /oauth/callback 路由接收浏览器回调
  - 证据: `src/index.ts:4 import type {} from '@deepseek-ai/dsh-host-webserver' + src/index.ts:510 ctx.get('webServer') + src/index.ts:526 webServer.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
