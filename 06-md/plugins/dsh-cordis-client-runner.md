# dsh-cordis-client-runner

- 包名: `@deepseek-ai/dsh-cordis-client-runner`
- 分组: G14 宿主扩展
- 拓扑层: Layer 10
- 来源层: L2 web-app
- 源码路径: `packages/extensions/cordis-client-runner`

## 实现逻辑
以「浏览器侧动态包引擎」实现：Host 半边是空 apply，浏览器半边经 exports 的 ./client 子路径与 package.json 的 dshClient 声明发布 (src/index.ts:8-9)。客户端 apply 先 provideClientTimer 补齐浏览器版 timer Service，再建 ClientCordisInspectRegistry、注册 clientInspectProviders，并通过 ctx.remote 同步 manifest 与回传查询结果 (src/client/index.ts:188-204)。随后建 DynamicCordisPackageRunner（闭包求值→guard 门面→模块表→loader 条目，见 src/client/runtime.ts:1-28、src/client/evaluator.ts:1-45、src/client/guard.ts:1-50）与 CordisRunOrchestrator，把合并后的运行面以 ctx.provide('dynamicCordisRunner', face) 暴露，并订阅 cordis/request-run、cordis/request-run-resolved、cordis/dynamic-retract、cordis/inspect-query 与 cordis/inspect-query-resolved 五个转发事件 (src/client/index.ts:206-308)。

## Provides
- ctx.dynamicCordisRunner (浏览器侧运行编排与页面本地加载状态：活动运行、失败、批准/拒绝、用户发起运行、订阅与快照)
- ctx.timer (浏览器端 ClientTimerService，保持与 Host TimerService 相同的 timeout/interval/throttle/debounce 公共 API)
- ctx.cordisInspect (浏览器侧 Inspect Provider 注册表、manifest 发布与 Host 查询应答)

## Depends On (上游依赖)
- `cordis-plugin-loader` [编译依赖] - 复用 Loader 机制为动态包创建/移除条目，从而获得 inject 门控、fiber 效应清理与状态投影
  - 证据: `src/client/runtime.ts:18 import Loader + package.json:48 devDep + src/client/index.ts:182 inject 'loader'`
- `dsh-api-remotes` [E1+E2] - 经 Remote 命名空间与 Host 侧做双向调用：同步 inspect manifest、解析查询、运行 Host 半、取客户端源码、结算用户运行与上报渲染/门面失败
  - 证据: `src/client/index.ts:17 import .../client + src/client/index.ts:182 inject 'remote'/'remote.dynamicCordisRunner' + src/client/index.ts:192 ctx.remote.dynamicCordisRunner.syncInspectManifest`
- `dsh-client-modules` [编译依赖] - 把动态包求值后的工厂座入浏览器模块表，使 loader 条目能像静态插件一样加载
  - 证据: `src/client/index.ts:18 import ClientModuleSystem + src/client/runtime.ts:23 import .../client + src/client/index.ts:209 ctx.get('modules')`
- `dsh-client-ui-renderer` [编译依赖] - 取得 SlotRegistry 类型与渲染面接缝，使动态包注册的 slot 条目挂到调用方 fiber 上
  - 证据: `src/client/index.ts:19 import SlotRegistry + src/client/runtime.ts:24 import .../client + package.json:51 devDep`
- `dsh-client-ui-theme` [编译依赖] - 在浏览器门面中把主题覆写来源钉到包 id，并向 Client Inspect 暴露主题能力
  - 证据: `src/client/guard.ts:19 import ThemeRuntime + src/client/providers.ts:6 type import + package.json:52 devDep`

## Dependents (下游被依赖)
- `dsh-client-ui-cordis` - 读取浏览器侧动态包的加载状态与活动运行，并把面板上的批准/运行/停止动作委托给运行面
