# dsh-api-gateway

- 包名: `@deepseek-ai/dsh-api-gateway`
- 分组: G02 API 网关与控制器
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/api/gateway`

## 实现逻辑
Host 侧 TypertGatewayService 继承 Service 并实现 TypertGateway，构造时向 connection 注册 /api RPC 拦截器、向 webServer 注册 WebSocket 多路复用路由 /api/remote.mux（存在 appReady 时等待其就绪再监听）(src/index.ts:226-277)。invoke/stream 经 prepareInvocation 解析 Typert 描述符（严格定义或 SRC 回退）、校验精确参数、解析 lookup/context provider，再以 Reflect.apply 调用业务方法并把结果编码为 RPC 结果 (src/index.ts:345-410, 686-877)。registerRemoteEvents 消费应用选定的唯一事件源：emit 通知广播给各客户端，Agent 作用域 waterfall 以事件 id 关联并在收到结果后继续/取消 (src/index.ts:285-311, 463-655)。客户端侧 apply() 安装 ClientRemoteService，暴露 ctx.remote 与 $stream/$host (src/client/index.ts:140-199)。

## Provides
- ctx.typertGateway（Typert Remote Host 调度器：invoke/stream/registerRemoteEvents 与载体无关的 wireStream 适配）
- ctx.remote（客户端侧生成式 Remote 命名空间服务，以及 $stream / $host 事实）
- WebSocket 多路复用端点 /api/remote.mux 与转发事件流端点 $events / $events/result

## Depends On (上游依赖)
- `dsh-client-connection` [E1+E2] - 承载 /api RPC 与对等 Peer 身份
  - 证据: `src/index.ts:14 import + src/index.ts:233 connection.rpc.intercept`
- `dsh-host-webserver` [运行时依赖] - 注册 WebSocket upgrade 路由
  - 证据: `src/index.ts:16 import type + src/index.ts:261 webServer.registerUpgrade`

## Dependents (下游被依赖)
- `dsh-api-job-controller` - 客户端 Remote 载体
- `dsh-api-remotes` - 注册转发事件源并使用客户端 Remote 载体
- `dsh-api-session-controller` - 客户端 Remote 载体与失败类型
- `dsh-api-terminal-controller` - 客户端 Remote 载体
- `dsh-api-workspace-controller` - 客户端 Remote 载体
- `dsh-api-workspace-files` - 客户端 Remote 载体
- `dsh-client-ui-open-in-app` - 引入 gateway 客户端的 ctx.remote 声明合并
- `dsh-client-ui-sidebar-documentpreview` - 引入网关客户端面与其类型合并
- `dsh-experimental-client-ui-voice-input` - 经网关检测语音后端可用性
- `dsh-experimental-webworker-runtime` - 把 typert 流经 tunnel 转发到页面
