# dsh-host-open-in-app

- 包名: `@deepseek-ai/dsh-host-open-in-app`
- 分组: G19 宿主服务
- 拓扑层: Layer 2
- 来源层: L2 web-app
- 源码路径: `packages/host/open-in-app`

## 实现逻辑
为 Web GUI 宿主提供「在外部应用中打开工作区」的三条 webServer 路由：GET /open-in-app/apps 返回探测到的应用 id、GET /open-in-app/icon/<id> 前缀路由返回 PNG 图标、POST /open-in-app/open 校验绝对目录后启动应用 (src/index.ts:193-310)。应用可用性与图标各自惰性解析并缓存一次，启动返回 missing 时只刷新该条目并重试一次 (src/index.ts:154-183, src/index.ts:295-303)。每条路由先经 connection.requestRejection 信任闸门，open 路由另做 content-type、64 KiB 请求体上限与 JSON 字段校验 (src/index.ts:184-191, src/index.ts:88-135, src/index.ts:250-283)。

## Provides
- webServer 上的 GET /open-in-app/apps、GET /open-in-app/icon/<id>、POST /open-in-app/open 三条路由
- ./shared 子路径导出的路由常量与 wire 载荷类型（与浏览器侧包共用）

## Depends On (上游依赖)
- `dsh-client-connection` [运行时依赖] - 读取信任策略，对未认证/不可信请求返回 401/403
  - 证据: `src/index.ts:47 static inject ['webServer','connection','subprocess'] + src/index.ts:85 Reflect.get(ctx, 'connection')（package.json 未声明该依赖）`
- `dsh-host-webserver` [E1+E2] - 承载三条路由并取得路由 disposer
  - 证据: `src/index.ts:27 import type {} from '@deepseek-ai/dsh-host-webserver' + src/index.ts:193 ctx.webServer.register`

## Dependents (下游被依赖)
- `dsh-client-ui-open-in-app` - 复用应用图标路由常量
