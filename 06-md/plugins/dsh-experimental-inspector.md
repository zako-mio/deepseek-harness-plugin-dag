# dsh-experimental-inspector

- 包名: `@deepseek-ai/dsh-experimental-inspector`
- 分组: G13 实验特性
- 拓扑层: Layer 1
- 来源层: L3 其余
- 源码路径: `packages/experimental/inspector`

## 实现逻辑
跨 realm 的运行时 Inspector：Host 面（src/host/plugin.ts:38-62）启动 Inspector Worker、以 `ctx.provide('inspector')` 暴露观察发布服务与只读 Cordis 拓扑查询（src/index.ts:39-50），并通过 `webserver/index-inject` 把 Client bootstrap 注入 index.html。Client 面（src/client/plugin.ts:45-70）读取全局 `__DSH_INSPECTOR__` bootstrap 连接 Worker 并发布浏览器侧观察。共享实现含 bridge(buffers/codec/rpc)、CDP 域代理、cordis 快照投影等（src/index.ts:1-37）。

## Provides
- ctx.inspector (发布 JSON 观察 + 只读 Cordis 运行时拓扑查询)

## Depends On (上游依赖)
- `dsh-host-webserver` [E1+E2] - 向页面注入 Client bootstrap 并在 webserver 生命周期内启动
  - 证据: `src/host/plugin.ts:4 import type { IndexInjection } + src/index.ts:63 inject ['webServer'] + src/host/plugin.ts:49 webserver/index-inject`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
