# dsh-client-connection

- 包名: `@deepseek-ai/dsh-client-connection`
- 分组: G05 客户端运行时
- 拓扑层: Layer 2
- 来源层: L2 web-app
- 源码路径: `packages/client/connection`

## 实现逻辑
Host 侧 `HostConnectionService` 提供载体中立的 RPC 与 Fetch 注册表，并在有 `webServer` 时把 `/api` 路由挂到 Web 服务器，经 Host/Origin 信任栅栏与持久浏览器认证后才放行 (src/index.ts:124-162, src/rpc-host.ts:63-113)。浏览器侧 `installConnection` 装配 `ctx.connection`，把 `ConnectionController` 的连接/重连循环、generation 状态与通用 RPC 通道以 getSnapshot/subscribe 观察面暴露，并在 online/offline 时更新可用性 (src/client/index.ts:205-311)。两侧通过 `__DSH_CONNECTION_RECOVERY__` 全局与 `connection/request` waterfall 协同。

## Provides
- ctx.connection (Host 侧 Connection 传输与 RPC/Fetch 注册表；浏览器侧连接 generation 与恢复循环句柄)
- connection/request waterfall 事件 (允许对已认证 /api 请求做准入/包装)
- OperatorPeer 与 rpc/schema 导出 (RpcId、transportError、rpcMessageSchema 等)

## Depends On (上游依赖)
- `dsh-host-webserver` [E1+E2] - 把 /api 路由和 recovery 注入表挂到 Web carrier 上
  - 证据: `src/index.ts:8 + src/index.ts:139 ctx.inject(['webServer']) + src/index.ts:158 webCtx.webServer.register`
- `dsh-llm` [编译依赖] - 共享 LLM 相关品牌与类型，用于客户端 API 类型面
  - 证据: `src/client/api.ts:13-14`
- `dsh-scope` [编译依赖] - 构造 OperatorPeer 的作用域语义
  - 证据: `src/operator-peer.ts:10`
- `dsh-session` [编译依赖] - 共享客户端 SessionId/SessionEvent/StreamChunk 等协议类型
  - 证据: `src/client/api.ts:12`

## Dependents (下游被依赖)
- `dsh-api-gateway` - 承载 /api RPC 与对等 Peer 身份
- `dsh-api-remotes` - 客户端连接类型再导出
- `dsh-api-session-controller` - 媒体引用与客户端连接
- `dsh-client-file-upload` - 在 Connection 的 fetch 注册表上挂原始字节上传路由
- `dsh-client-ui-deliverables` - 原生打开请求经连接层发送
- `dsh-client-ui-permission-presets` - 目录结算以连接世代为围栏
- `dsh-client-ui-schedule` - 连接世代相关类型面
- `dsh-client-ui-settings-general` - 取连接状态用于重连入口与桌面更新徽标
- `dsh-experimental-webworker-runtime` - 从树中取得共享 fetch handler 供 tunnel 直连
- `dsh-host-frontend-static` - 对 index 响应执行浏览器鉴权
- `dsh-host-open-in-app` - 每条路由的信任栅栏与浏览器鉴权
