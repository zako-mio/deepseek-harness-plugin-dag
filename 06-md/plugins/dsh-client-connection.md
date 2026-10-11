# dsh-client-connection

- 包名: `@deepseek-ai/dsh-client-connection`
- 分组: G05 客户端运行时
- 拓扑层: Layer 1
- 来源层: L2 web-app
- 源码路径: `packages/client/connection`

## 实现逻辑
以「Host 半 HostConnectionService + 浏览器半 ConnectionHandle」双半实现载体中立的 RPC/Fetch 传输：Host 半在 /api 上挂载带 Host/Origin 信任栅栏与浏览器会话认证的路由，并把每个通过认证的请求归属为唯一的 operator Peer（src/index.ts:122-160、src/rpc-host.ts:63-124）。它还提供通用逻辑通道注册表与精确 Fetch 路由注册表，两者都以调用者 fiber 为归属（src/rpc-host.ts:88-104、src/rpc-host.ts:158-201）。浏览器半用 ConnectionController 维护连接世代与重连状态，对外暴露 ctx.connection，供 API Gateway 等下游读取 isLoopback/generation/rpc 并驱动连接循环（src/client/index.ts:205-311）。

## Provides
- ctx.connection (Host 半：RPC 通道与精确 Fetch 路由注册表、请求信任与认证、operator Peer；浏览器半：连接世代、重连状态与逻辑 RPC 载体)
- connection/request (waterfall 事件，供扩展点包裹已认证的 /api 请求) (src/index.ts:57-68)

## Depends On (上游依赖)
- `dsh-host-webserver` [E1+E2] - 把 /api 传输挂到 Web 服务器的路由表与 index 注入表
  - 证据: `src/index.ts:8 import + src/index.ts:137 ctx.inject(['webServer']) + src/index.ts:156 webServer.register(route)`
- `dsh-llm` [编译依赖] - 浏览器 API 复用 LLM 品牌与类型
  - 证据: `src/client/api.ts:13-14 import`
- `dsh-session` [编译依赖] - 浏览器 API 复用会话/事件类型
  - 证据: `src/client/api.ts:12 import`

## Dependents (下游被依赖)
- `dsh-api-gateway` - 复用连接层的 RPC 拦截、Peer 身份与断线重连生命周期
- `dsh-api-remotes` - 再导出承载层的 Client 类型，使业务包只命名本装配包
- `dsh-api-session-controller` - 媒体引用 HTTP 端点复用连接层的请求鉴权
- `dsh-api-workspace-controller` - Client 面工作区服务依赖承载层的连接生命周期
- `dsh-client-file-upload` - 在共享 /api 通道注册流式上传路由
- `dsh-client-ui-deliverables` - 读取连接世代并对原生打开做认证
- `dsh-client-ui-permission-presets` - 以真实连接世代为目录结算的栅栏
- `dsh-client-ui-schedule` - 连接代际重置时使目录源失效重读
- `dsh-client-ui-settings-general` - 外壳的重连动作与连接状态指示器读连接句柄
- `dsh-experimental-inspector` - bootstrap 端点与 DevTools 路由都要经连接层的鉴权与路由表
- `dsh-experimental-webworker-runtime` - 树内 HTTP 请求的统一入口与共享 fetch handler 来自连接层
- `dsh-host-directory-picker-auto` - 信任策略允许非 loopback 权威时，远程浏览器无法到达宿主 OS 选择器，必须走 browse
- `dsh-host-frontend-static` - 对 index 响应执行浏览器鉴权
- `dsh-host-open-in-app` - 读取信任策略，对未认证/不可信请求返回 401/403
