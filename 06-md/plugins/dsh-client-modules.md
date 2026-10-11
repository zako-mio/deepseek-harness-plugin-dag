# dsh-client-modules

- 包名: `@deepseek-ai/dsh-client-modules`
- 分组: G05 客户端运行时
- 拓扑层: Layer 1
- 来源层: L2 web-app
- 源码路径: `packages/client/modules`

## 实现逻辑
双面包：Node 半扫描 Loader 条目中声明 dsh.client 的包，按模块图顺序组装 window.__DSH_BOOT__ 入口图，向 webServer 的 index 注入表贡献注册门面、预载与 bootstrap 脚本，并提供 ctx.clientModules（HMR Node 半的注册/通知面）；扫描按 internal/plugin 脏标记增量 flush，无全量重扫路径（src/index.ts:1-49、src/index.ts:624-654）。浏览器半由 shell 内核在 cordis 之前构建懒加载 CJS 模块表，插件面把它作为 ctx.modules 暴露给 Loader（src/client/index.ts:39-67）。

## Provides
- ctx.clientModules (Web 客户端模块图注册表：图查询、artifact 基线、rebuilt 通知)
- ctx.modules (浏览器端模块系统，作为 vendored Loader 的 internal seam)

## Depends On (上游依赖)
- `cordis-plugin-loader` [E1+E2] - 读取 Loader 条目并接管其 internal 模块系统
  - 证据: `src/index.ts:34 import + src/index.ts:597 inject ['loader'] + src/client/index.ts:54 inject ['loader']`
- `dsh-host-webserver` [E1+E2] - 注入 boot 图与 bootstrap 脚本并服务 bundle 路由
  - 证据: `src/index.ts:35 import type + src/index.ts:654 webserver/index-inject`

## Dependents (下游被依赖)
- `dsh-client-hmr` - 读取客户端模块图与 artifact 基线并发布 bundle 重建
- `dsh-client-ui-settings-plugin-inventory` - 清单页需读客户端模块图条目状态并可触发重试
- `dsh-client-web` - 以客户端模块系统作为 loader.internal 并消费其 manifest/图
- `dsh-cordis-client-runner` - 把动态包求值后的工厂座入浏览器模块表，使 loader 条目能像静态插件一样加载
- `dsh-experimental-inspector` - 浏览器端模块装载的声明依赖，保证组合中存在同一份实现
- `dsh-experimental-webworker-runtime` - 浏览器模块装载的声明依赖，保证组合中存在同一份实现
