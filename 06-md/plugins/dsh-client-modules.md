# dsh-client-modules

- 包名: `@deepseek-ai/dsh-client-modules`
- 分组: G05 客户端运行时
- 拓扑层: Layer 1
- 来源层: L2 web-app
- 源码路径: `packages/client/modules`

## 实现逻辑
Node 半增量扫描 Loader 中声明 `dsh.client` 的包（`internal/plugin` 事件触发 microtask flush，激活期同步 flush 同一实现），按模块图拓扑排序组合 `window.__DSH_BOOT__` 条目图 (src/index.ts:596-657, 501-533)。它按行读取并缓存客户端 bundle、生成 revision 化的 combo 脚本与 source map、注册 `/plugins` 路由并惰性生成响应体 (src/index.ts:434-459, 1128-1156)，同时提供 `clientModules` 服务（rebuilt/onRebuilt/onGraphChanged）作为 HMR Node 半的注册与通知面 (src/index.ts:706-756)。

## Provides
- ctx.clientModules (ClientModuleRegistry：graph/artifactBaseline/rebuilt/onRebuilt/onGraphChanged/clientPath/fetchBundle)
- /plugins 路由 (revision 化 combo 脚本与 source map 及包本地 chunk)
- window.__DSH_BOOT__ 条目图与 index 注入行 (bootInjections)
- 客户端模块 HTTP 路由与模块表身份 (供 web 壳消费)

## Depends On (上游依赖)
- `cordis-plugin-loader` [E1+E2] - 以 Loader 行为输入扫描 dsh.client 声明并解析包真实位置
  - 证据: `src/index.ts:34 + src/index.ts:597 static inject 'loader' + src/index.ts:639 ctx.loader.entries()`
- `dsh-host-webserver` [E1+E2] - 注册 /plugins bundle 路由并向 index 注入启动脚本与全局图
  - 证据: `src/index.ts:35 + src/index.ts:653 ctx.inject(['webServer']) + src/index.ts:649 webCtx.webServer.register`
- `dsh-invariants` [运行时依赖] - 注册包级不变量，校验模块注册表随 fiber 释放而清理
  - 证据: `src/invariant.ts:8 + src/invariant.ts:15 inject 'invariants' + src/invariant.ts:44 ctx.invariants.register`

## Dependents (下游被依赖)
- `dsh-client-hmr` - 读取客户端模块图与 artifact 基线，并把重建事件反馈回图
- `dsh-client-ui-settings-plugin-inventory` - 读取客户端模块加载状态并触发重试
- `dsh-client-web` - 以客户端模块系统作为 loader.internal 并消费其 manifest/图
- `dsh-cordis-client-runner` - 提供浏览器侧模块系统以装载动态包入口
