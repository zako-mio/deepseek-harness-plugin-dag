# dsh-cordis-client-runner

- 包名: `@deepseek-ai/dsh-cordis-client-runner`
- 分组: G14 宿主扩展
- 拓扑层: Layer 10
- 来源层: L2 web-app
- 源码路径: `packages/extensions/cordis-client-runner`

## 实现逻辑
浏览器半的动态包运行器：用 DynamicCordisPackageRunner 与 CordisRunOrchestrator 把模型写的前端源码经 closure→guard→module table→loader entry 装载成活的 cordis 插件，并把审批、宿主半调用、客户端代码拉取都折叠为 remote 调用 (src/client/index.ts:206-278)。运行结果面通过 ctx.provide('dynamicCordisRunner', face) 暴露活动运行、渲染失败、审批与快照 (src/client/index.ts:279-291)，页面激活时不预载任何动态包。另注册客户端 Cordis Inspect provider 并把 manifest 同步给宿主、路由 inspect 查询 (src/client/index.ts:190-204, 303-308)。

## Provides
- ctx.dynamicCordisRunner (客户端动态插件运行面：装载/停止浏览器半、审批、渲染失败上报与页面快照)
- ctx.cordisInspect (客户端 Inspect provider 注册与查询路由)

## Depends On (上游依赖)
- `cordis-plugin-loader` [E1+E2] - 把求值后的动态包注册为 loader entry 并管理其生命周期
  - 证据: `src/client/index.ts:182 inject 'loader' + src/client/runtime.ts:18 import`
- `dsh-api-remotes` [E1+E2] - 跨平面调用宿主半运行、获取客户端代码与上报失败
  - 证据: `src/client/index.ts:211-277 ctx.remote.* 调用 + src/client/index.ts:17 import`
- `dsh-client-modules` [E1+E2] - 提供浏览器侧模块系统以装载动态包入口
  - 证据: `src/client/index.ts:182 inject 'modules' + src/client/runtime.ts:23 import`
- `dsh-client-ui-renderer` [E1+E2] - 用 slot 注册表承接动态半向 UI 的贡献
  - 证据: `src/client/index.ts:182 inject 'slots' + src/client/guard.ts:18 import`
- `dsh-client-ui-theme` [编译依赖] - 动态半渲染时读取主题令牌
  - 证据: `src/client/guard.ts:19 import + src/client/providers.ts:6 import`

## Dependents (下游被依赖)
- `dsh-client-ui-cordis` - 读取客户端运行面快照并驱动审批、启动与停止
