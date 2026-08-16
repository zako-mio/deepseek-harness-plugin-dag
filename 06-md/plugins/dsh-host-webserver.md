# dsh-host-webserver

- 包名: `@deepseek-ai/dsh-host-webserver`
- 分组: G25 宿主服务
- 拓扑层: Layer 0
- 来源层: L2 web-app
- 源码路径: `packages/host/webserver`

## 实现逻辑
node:http 服务器 + ctx.webServer 服务：exact/prefix 路由表 register、upgrade 路由 registerUpgrade、单占用 fallback 兜底座 registerFallback、index 变换 tapIndex；监听即激活，bind host/port 来自行配置表达式（webStartup 提供）；不感知 harness 概念、不打印 URL。

## Provides
- ctx.webServer（WebServer：register/registerUpgrade/registerFallback/tapIndex，port/host getter）

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-client-connection` - /api 前缀路由与 registerUpgrade 的宿主
- `dsh-client-hmr` - node 半通过 ctx.webServer.register 挂 SSE 路由（:166-179）
- `dsh-client-modules` - 注册 /plugins 前缀路由与 tapIndex 注入
- `dsh-host-directory-picker-auto` - Context merge（ctx.webServer）
- `dsh-host-frontend-static` - HTTP 服务器与 index taps 注册
- `dsh-web-app` - Context merge（ctx.webServer）
