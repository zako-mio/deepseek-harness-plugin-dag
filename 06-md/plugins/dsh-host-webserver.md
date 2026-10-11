# dsh-host-webserver

- 包名: `@deepseek-ai/dsh-host-webserver`
- 分组: G19 宿主服务
- 拓扑层: Layer 0
- 来源层: L2 web-app
- 源码路径: `packages/host/webserver`

## 实现逻辑
实现宿主 Web 服务器服务：默认导出 WebServer 继承 cordis Service 并注册为 ctx.webServer (src/index.ts:261, src/index.ts:557)。它基于 node:http 建立监听（tls 配置齐全时改用 node:https，证书与私钥在绑定前一次性读取、失败即拒绝启动），对外提供 register（精确/前缀路由）、registerUpgrade、registerFallback（唯一兜底座位）、tapIndex（原始 HTML 变换）四类注册，均返回 disposer (src/index.ts:334-386)。index 渲染先把 webserver/index-inject 事件收集到的结构化注入行渲染进 HTML，再依次应用 tapIndex 变换 (src/index.ts:528-554, src/injections.ts:96-119)。

## Provides
- ctx.webServer（WebServer 服务：register / registerUpgrade / registerFallback / tapIndex / applyIndexTaps / collectIndexInjections / renderIndex）
- webserver/index-inject 事件（收集结构化 index 注入行表）
- isLoopbackHost 等主机判定与 renderIndexInjections / IndexInjection 类型的再导出

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-api-gateway` - 注册 Remote 流的 WebSocket 升级路由
- `dsh-client-connection` - 把 /api 传输挂到 Web 服务器的路由表与 index 注入表
- `dsh-client-hmr` - 提供 /plugins/events SSE 路由
- `dsh-client-modules` - 注入 boot 图与 bootstrap 脚本并服务 bundle 路由
- `dsh-client-shortcuts` - 向页面注入快捷键配置全局量
- `dsh-client-ui-settings-account` - Host 半借 webserver 的 index-inject 钩子把公开联系配置注入页面初始化数据
- `dsh-client-ui-settings-models` - Host 半借 webserver 的 index-inject 钩子把 credentialOnboarding 注入页面 global
- `dsh-client-ui-sidebar-documentpreview` - Host 半把预览配置注入浏览器页面索引
- `dsh-client-ui-theme` - 把启动期主题与字体注入浏览器页面索引
- `dsh-client-web` - 消费 webserver index 注入表以应用脚本/全局注入
- `dsh-deepseek-account-platform` - 浏览器回调需要宿主 HTTP 服务器上的一个精确路由
- `dsh-experimental-inspector` - DevTools 前端资源与 CDP 代理需要宿主 HTTP 服务器的路由与升级钩子
- `dsh-experimental-webworker-runtime` - 页面 boot 所需的 index 注入表由树内 webserver 收集
- `dsh-host-directory-picker-auto` - 读取生效的绑定地址，并用 loopback 判定决定是否可能使用 native 选择器
- `dsh-host-frontend-static` - 占用其 fallback 座位并渲染 index 注入
- `dsh-host-open-in-app` - 承载三条路由并取得路由 disposer
- `dsh-webhook-github` - 在宿主机 WebServer 上注册 webhook 的 exact 路由
