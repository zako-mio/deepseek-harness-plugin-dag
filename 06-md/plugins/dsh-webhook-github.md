# dsh-webhook-github

- 包名: `@deepseek-ai/dsh-webhook-github`
- 分组: G48 Webhook
- 拓扑层: Layer 3
- 来源层: L3 其余
- 源码路径: `packages/webhook/webhook-github`

## 实现逻辑
函数插件在 ctx.webServer 上注册一条 exact 路由 (src/index.ts:47-61)。handler 校验 POST 与 JSON Content-Type，读取受限 body 及 x-hub-signature-256/x-github-delivery/x-github-event 头，用 ctx.credentials 解析密钥并经 Octokit Webhooks 校验签名 (src/handler.ts:82-105)。校验通过后构造 VerifiedWebhookDelivery<'github'> 交给 ctx.webhookRuntime.dispatch 做 fire-and-forget 分发 (src/handler.ts:107-119)，并在 types.ts 里向 WebhookEventMap 合并 'github' 事件 (src/types.ts:16-20)。

## Provides
- ctx.webServer 上的 GitHub 签名 webhook 路由
- WebhookEventMap['github'] 事件类型 (dsh-webhook 的 provider 事件族)

## Depends On (上游依赖)
- `dsh-host-webserver` [E1+E2] - 在宿主机 WebServer 上注册 webhook 的 exact 路由
  - 证据: `package.json:37 peerDep + src/handler.ts:13 import type { WebRoute } + src/index.ts:14 inject 'webServer' + src/index.ts:59 ctx.webServer.register`
- `dsh-session` [编译依赖] - 声明式 peer 依赖（webhook 投递与会话生态保持一致）
  - 证据: `package.json:38 peerDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
