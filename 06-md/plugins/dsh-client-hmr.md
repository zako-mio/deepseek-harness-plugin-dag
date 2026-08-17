# dsh-client-hmr

- 包名: `@deepseek-ai/dsh-client-hmr`
- 分组: G26 客户端runtime
- 拓扑层: Layer 7
- 来源层: L2 web-app
- 源码路径: `packages/client/hmr`

## 为什么需要它（设计初衷）
仅开发环境的热重载驱动：SSE 重建帧 → 失效/预取 → 经 vendored Loader 入口做 fiber 切换，加速客户端插件开发。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/hmr/package.json

## 实现逻辑
双面插件。node 半：以 500ms 间隔 stat-poll 扫描 clientModules.graph() 中每个行 id 的 client bundle 文件（polling 设计——网络挂载无 inotify），mtime/size 变化时调 ctx.clientModules.rebuilt(id) 触发重哈希，并注册 /plugins/events SSE 通道（连接时推 graph 帧、重建时推 rebuilt 帧）。browser 半：EventSource 订阅同一 SSE，收到 rebuilt 帧后按 invalidate→prefetch→registry.delete→drain 旧 fiber→removeOwnedStyles→entry.refresh() 顺序热交换插件 fiber（registry-first teardown 避免 Loader 自处置标记 disabled）。串行队列防帧交错。无回滚策略。

## Provides
- /plugins/events SSE 通道（graph/rebuilt 帧，PluginsEventFrame）

## Depends On (上游依赖)
- `dsh-client-modules` [编译依赖] - node 半消费 clientModules 服务的 graph()/clientPath()/onGraphChanged()/onRebuilt() 与 rebuilt() 重哈希钩子
  - 证据: `packages/client/hmr/src/index.ts:16-17（import type dsh-client-modules）；package.json peerDependencies @deepseek-ai/dsh-client-modules`
- `dsh-host-webserver` [编译依赖] - node 半通过 ctx.webServer.register 挂 SSE 路由（:166-179）
  - 证据: `packages/client/hmr/src/index.ts:17（import type dsh-host-webserver）；peerDependencies @deepseek-ai/dsh-host-webserver`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
