# dsh-api-gateway

- 包名: `@deepseek-ai/dsh-api-gateway`
- 分组: G02 API 网关与控制器
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/api/gateway`

## 实现逻辑
实现 Typert Remote 的双面传输。Host 侧 TypertGatewayService 注册为 ctx.typertGateway(src/index.ts:199-228)，在 connection 上拦截 /api RPC(src/index.ts:233-239)，并把 /api/remote.mux 的 WebSocket 升级路由挂到 webServer(src/index.ts:240-277, src/stream-protocol.ts:6)。派发时按严格描述符或 SRC 标记解析 endpoint 与参数，经 lookup/context provider 解析后以绑定了 invocation 的 Service 视图调用业务方法(src/index.ts:700-938)。Client 侧 ClientRemoteService 注册 ctx.remote，按生成描述符挂载 remote.<namespace> 并监管可重连的逻辑流(src/client/index.ts:126-200)。

## Provides
- ctx.typertGateway(Host 侧 Typert Remote 派发服务：invoke/stream/registerRemoteEvents，src/index.ts:194-323)
- ctx.remote(Client 侧类型化 Remote 命名空间服务与 $stream/$host，src/client/index.ts:102-116,126-131)
- WebSocket 多路复用路由 /api/remote.mux 与升级处理(src/stream-protocol.ts:6 + src/index.ts:251-262)

## Depends On (上游依赖)
- `dsh-client-connection` [E1+E2] - 复用连接层的 RPC 拦截、Peer 身份与断线重连生命周期
  - 证据: `package.json:66 peerDep + src/index.ts:10-14 import OperatorPeer + src/client/index.ts:11-13 import ConnectionHandle + src/index.ts:233 ctx.inject(['connection'])`
- `dsh-host-webserver` [E1+E2] - 注册 Remote 流的 WebSocket 升级路由
  - 证据: `package.json:72 devDependencies + src/index.ts:16 import type WebUpgradeRoute + src/index.ts:262 webCtx.webServer.registerUpgrade`
- `dsh-typert-registry` [运行时依赖] - Client 面注入 Typert registry，使生成描述符可在页内解析
  - 证据: `package.json:39 dsh.client.inject + src/index.ts:200 static inject = ['typert'] + src/index.ts:329 ctx.typert`

## Dependents (下游被依赖)
- `dsh-api-job-controller` - 客户端 Remote 载体
- `dsh-api-remotes` - 注册转发事件源并挂载 Client Remote 命名空间
- `dsh-api-session-controller` - Client 面通过 Gateway 的 ctx.remote 调用本命名空间
- `dsh-api-terminal-controller` - Client 面经 Gateway 的 ctx.remote 暴露终端命名空间
- `dsh-api-workspace-controller` - Client 面经 Gateway 的 ctx.remote 暴露工作区命名空间
- `dsh-api-workspace-files` - 客户端 Remote 载体
- `dsh-client-product-analytics` - 浏览器端 Remote 调用与流承载
- `dsh-client-ui-open-in-app` - 网关 Remote 类型
- `dsh-client-ui-sidebar-documentpreview` - 拉入网关客户端的 Context/类型合并以承载远程调用面
- `dsh-cordis-host-runner` - 声明 Gateway 接缝类型，使无存活 Client 时 Inspect 查询能快速失败而非等待超时
- `dsh-experimental-client-ui-voice-input` - Remote 流载体失败的错误类型来自网关包
- `dsh-experimental-webworker-runtime` - 隧道上的流式请求由网关的 wireStream 承载
