# dsh-client-modules

- 包名: `@deepseek-ai/dsh-client-modules`
- 分组: G26 客户端runtime
- 拓扑层: Layer 6
- 来源层: L2 web-app
- 源码路径: `packages/client/modules`

## 实现逻辑
双面插件。node 半：增量扫描 host Loader 条目的 package.json 中 dsh.client（platform=web）声明，按 exports['./client'] 解析 bundle 路径，sha1 短哈希做 rev，组合 window.__DSH_BOOT__ 图（WebBootEntry/WebBootGraph），serveBundle 提供 /plugins/<id>/client.js(+.map)，tapIndex 注入 boot manifest，并提供 clientModuleHost 服务（graph()/clientPath()/rebuilt()/onRebuilt()/onGraphChanged()）。browser 半：懒 CJS 模块表（ClientModuleSystem）——执行 bundle 只注册 factory，materialization 才跑副作用；提供 ctx.modules，被 vendored Loader 作为 internal 契约消费。

## Provides
- clientModules 服务（ctx 合并）
- window.__DSH_BOOT__ 注入
- /plugins/<id>/client.js 路由
- ctx.modules（ClientModuleLoader, browser）
- dsh.client 声明解析（inject/immediately/platform）

## Depends On (上游依赖)
- `dsh-cordis-host-runner` [运行时依赖] - fiber 构造/处置标记 dirty 名字，增量扫描 loader entries
  - 证据: `packages/client/modules/src/index.ts:218（ctx.on('internal/plugin',…)）`
- `dsh-host-webserver` [编译依赖] - 注册 /plugins 前缀路由与 tapIndex 注入
  - 证据: `packages/client/modules/src/index.ts:32（import type dsh-host-webserver）；Service.inject = ['webServer','loader']（:185）`

## Dependents (下游被依赖)
- `dsh-client-hmr` - node 半消费 clientModules 服务的 graph()/clientPath()/onGraphChanged()/onRebuilt() 与 rebuilt() 重哈希钩子
- `dsh-client-web` - 模块表内核（bootstrap 例外）
- `dsh-cordis-client-runner` - 模块表类型与 factory 注册/失效（runtime.ts:156 moduleIdOf）
