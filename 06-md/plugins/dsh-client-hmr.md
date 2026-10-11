# dsh-client-hmr

- 包名: `@deepseek-ai/dsh-client-hmr`
- 分组: G05 客户端运行时
- 拓扑层: Layer 2
- 来源层: L2 web-app
- 源码路径: `packages/client/hmr`

## 实现逻辑
Host 半按固定间隔 stat 轮询 clientModules 图里每个客户端 bundle，检测到 mtime/ctime/size 变化就调用 ctx.clientModules.rebuilt(id) 触发重建代际（src/index.ts:92-141、src/index.ts:143-156），并在 /plugins/events 上开 SSE 通道广播 graph 与 rebuilt 帧（src/index.ts:158-207）。浏览器半订阅同一条 SSE，把 graph 帧交给 ctx.modules.entries.sync、把 rebuilt 帧交给 entries.reload（src/client/index.ts:18-46）。

## Provides

## Depends On (上游依赖)
- `dsh-client-modules` [E1+E2] - 读取客户端模块图与 artifact 基线并发布 bundle 重建
  - 证据: `src/index.ts:15 import type + src/index.ts:27 inject ['clientModules'] + src/index.ts:77 ctx.clientModules.rebuilt(id)`
- `dsh-host-webserver` [E1+E2] - 提供 /plugins/events SSE 路由
  - 证据: `src/index.ts:16 import type + src/index.ts:27 inject ['webServer'] + src/index.ts:181 ctx.webServer.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
