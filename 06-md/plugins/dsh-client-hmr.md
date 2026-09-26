# dsh-client-hmr

- 包名: `@deepseek-ai/dsh-client-hmr`
- 分组: G05 客户端运行时
- 拓扑层: Layer 2
- 来源层: L2 web-app
- 源码路径: `packages/client/hmr`

## 实现逻辑
Host 侧以单一定时器 stat-poll 每个 graph 行的客户端 bundle（设计上用轮询，因网络挂载无 inotify），元数据变化即调 `clientModules.rebuilt(id)` 发布新 generation (src/index.ts:68-156)。同时注册 `/plugins/events` SSE 路由，把 graph 变化与 rebuilt 帧广播给浏览器 (src/index.ts:158-207)。另发布 invariant 伴生插件，以 StatWatcher 计数基线校验 bundle 轮询器随 fiber 销毁而终止 (src/invariant.ts:31-59)。

## Provides
- 客户端 bundle 变更的 stat 轮询监测与 clientModules.rebuilt 触发
- /plugins/events SSE 频道 (graph 与 rebuilt 帧广播)
- client-hmr-invariant 伴生不变量 (StatWatcher 泄漏检测)

## Depends On (上游依赖)
- `dsh-client-modules` [E1+E2] - 读取客户端模块图与 artifact 基线，并把重建事件反馈回图
  - 证据: `src/index.ts:15 + src/index.ts:27 inject 'clientModules' + src/index.ts:148 ctx.clientModules.onGraphChanged`
- `dsh-host-webserver` [E1+E2] - 挂载 /plugins/events SSE 路由
  - 证据: `src/index.ts:16 + src/index.ts:27 inject 'webServer' + src/index.ts:181 ctx.webServer.register`
- `dsh-invariants` [运行时依赖] - 注册包级不变量，检查 bundle 监视器不被泄漏
  - 证据: `src/invariant.ts:7 + src/invariant.ts:14 inject 'invariants' + src/invariant.ts:59 ctx.invariants.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
