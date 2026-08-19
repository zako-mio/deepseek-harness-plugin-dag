# dsh-api-gateway

- 包名: `@deepseek-ai/dsh-api-gateway`
- 分组: G02 类型契约
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/api/gateway`

## 为什么需要它（设计初衷）
Typert Remote Host 分派器与客户端 API 端点，是 api 能力族的 RPC 网关（dsh-api-remotes 的底层实现）。

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-api-gateway
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/api

## 实现逻辑
Typert Remote 双向网关：Host 端 TypertGatewayService(ctx.typertGateway，static inject=['typert']) 把 '/api/<namespace>/<method>' RPC 派发到 live cordis Service——先 ctx.typert.local 严格 descriptor，缺省时经 collectSrcClaims 反射构建 SRC descriptor；Client 端 ClientRemoteService(ctx.remote，inject=['typert','connection']) 安装 direct/scoped 方法到 RemoteNamespaceService，经 connection.rpc.call('/api',...) 转发，支持 $on/$dispatch 远程事件订阅。

## Provides
- ctx.typertGateway(Host 派发器)
- ctx.remote(Client Remote 命名空间)
- connection.rpc.intercept('/api')
- Client 远程事件 $on/$dispatch

## Depends On (上游依赖)
- `dsh-typert-registry` [运行时依赖] - descriptor 权威来源
  - 证据: `packages/api/gateway/src/index.ts:91,117-135`

## Dependents (下游被依赖)
- `dsh-api-remotes` - client 面声明依赖网关 client（remote 装配需要其类型面）
- `dsh-host-apiproxy` - E3 override：row id api-gateway 覆盖 base 层 api-gateway 行（name 换为 dsh-host-apiproxy）
