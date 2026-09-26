# dsh-host-webserver

- 包名: `@deepseek-ai/dsh-host-webserver`
- 分组: G20 宿主服务
- 拓扑层: Layer 0
- 来源层: L2 web-app
- 源码路径: `packages/host/webserver`

## 实现逻辑
实现 ctx.webServer 服务（node:http 载体），Service.init 监听 socket 并把命名路由/升级路由/fallback 分派（src/index.ts:125-316）。命名路由支持 exact 与最长前缀匹配，fallback 座位单属主且二次注册抛错（src/index.ts:166-203、319-328）。index 渲染先收集 webserver/index-inject 结构化注入行再套用原始 tapIndex 变换（src/index.ts:336-362），injections.ts 负责行到 markup 的渲染与 boot-ready 结算（src/injections.ts:96-118）。

## Provides
- ctx.webServer (HTTP 载体服务：命名路由/升级路由/fallback 座位/index 注入渲染，src/index.ts:125-365)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-api-gateway` - 注册 WebSocket upgrade 路由
- `dsh-client-connection` - 把 /api 路由和 recovery 注入表挂到 Web carrier 上
- `dsh-client-hmr` - 挂载 /plugins/events SSE 路由
- `dsh-client-modules` - 注册 /plugins bundle 路由并向 index 注入启动脚本与全局图
- `dsh-client-shortcuts` - 把键盘配置注入到服务的页面 index
- `dsh-client-ui-settings-account` - 向 webserver 注入账户联系方式配置
- `dsh-client-ui-settings-models` - Host 侧向浏览器页面注入引导配置全局
- `dsh-client-ui-sidebar-documentpreview` - Host 侧向浏览器页面注入预览配置全局
- `dsh-client-ui-theme` - 向 HTML index 注入 boot 主题样式与脚本
- `dsh-client-web` - 消费 webserver index 注入表以应用脚本/全局注入
- `dsh-deepseek-account-platform` - 注册 /oauth/callback 路由接收浏览器回调
- `dsh-experimental-inspector` - 向页面注入 Client bootstrap 并在 webserver 生命周期内启动
- `dsh-experimental-webworker-runtime` - 使用 webserver 采集 index injections 作为 boot payload
- `dsh-host-directory-picker-auto` - 读取生效绑定 host 作为后端判定事实
- `dsh-host-frontend-static` - 占用其 fallback 座位并渲染 index 注入
- `dsh-host-open-in-app` - 承载 apps/icon/open 三条路由
- `dsh-webhook-github` - 在宿主机 WebServer 上注册 webhook 的 exact 路由
