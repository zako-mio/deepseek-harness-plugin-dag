# dsh-client-web

- 包名: `@deepseek-ai/dsh-client-web`
- 分组: G05 客户端运行时
- 拓扑层: Layer 2
- 来源层: L3 其余
- 源码路径: `packages/client/web`

## 实现逻辑
Web 壳库入口导出 `AppWebEntry`、静态模块表与 index 注入应用器 (src/index.ts:9-12)。`AppWebEntry.run` 等待 boot-ready、从 `__ModuleLoader__` 创建模块系统与 manifest、预取 immediate 层，再以 `bootClient` 组装 Cordis Loader 激活全部客户端条目，最后用 `mountClient` 交接渲染器 (src/boot.ts:49-103)。`bootClient` 把 Loader 挂到模块系统并逐行 create、await，随后 `assertEntriesActive` 审计失败/待服务条目并抛聚合错误 (src/boot-client.ts:36-89)；`mountClient` 以 `uiRenderer` 依赖 fiber 挂载应用 (src/mount.ts:19-24)。

## Provides
- AppWebEntry (Web 壳启动入口：模块系统+HMR 交接+应用挂载)
- 客户端静态模块表与平台模块词表 (PLATFORM_MODULES/PRELOADED_CLIENT_EXTERNALS)
- bootClient/assertEntriesActive/mountClient 组装与激活审计
- applyIndexInjections (消费 webserver index 注入表)

## Depends On (上游依赖)
- `cordis-plugin-loader` [E1+E2] - 在浏览器端挂载 Loader 并逐行激活客户端插件
  - 证据: `src/boot-client.ts:8 + src/boot-client.ts:38 ctx.plugin(Loader) + src/boot-client.ts:40 loader.internal`
- `dsh-client-modules` [编译依赖] - 以客户端模块系统作为 loader.internal 并消费其 manifest/图
  - 证据: `src/boot.ts:11 + src/boot-client.ts:9`
- `dsh-client-ui-dockkit` [编译依赖] - 种子静态模块表内联 dockkit 布局库
  - 证据: `src/seed.ts:17`
- `dsh-client-ui-primitives` [编译依赖] - 种子静态模块表内联 UI 原语库
  - 证据: `src/seed.ts:16`
- `dsh-client-ui-renderer` [E1+E2] - 交接挂载点给 UI 渲染器，随其替换重挂
  - 证据: `src/mount.ts:7 + src/mount.ts:20 ctx.inject(['uiRenderer'])`
- `dsh-host-webserver` [编译依赖] - 消费 webserver index 注入表以应用脚本/全局注入
  - 证据: `src/apply-injections.ts:7`

## Dependents (下游被依赖)
- `dsh-experimental-webworker-runtime` - 复用 Client web 侧的 index injection 定义
