# dsh-cordis-client-runner

- 包名: `@deepseek-ai/dsh-cordis-client-runner`
- 分组: G26 客户端runtime
- 拓扑层: Layer 13
- 来源层: L2 web-app
- 源码路径: `packages/extensions/cordis-client-runner`

## 为什么需要它（设计初衷）
动态双半插件包的浏览器半：把定义加载为实时浏览器插件并回退清理。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/extensions/cordis-client-runner/README.md

## 实现逻辑
动态双半插件包的浏览器半运行引擎（node 半 apply 空，仅让行出现在 Loader）。DynamicCordisPackageRunner：把浏览器半源码 evaluateClientHalf（闭包求值）→ guard facade 包装 → 模块表注册 factory（moduleIdOf: 'dyn/<id>'）→ 创建 loader entry，复用静态插件的 inject 等待/fiber-effect 清理/status 投影；unload=loader entry 移除+factory 失效+样式移除。CordisRunOrchestrator：订阅 remote.dynamicCordisRunner 命名空间与 5 个 forwarded 事件（cordis/request-run 等），驱动 run/approve/decline/startUserRun。ClientCordisInspectRegistry：inspect manifest 同步/query 解析。provideClientTimer 提供 ClientTimerService。

## Provides
- ctx.dynamicCordisRunner（CordisRunnerFace: activeRuns/lastRunError/renderFailures/approve/decline/startUserRun/subscribe/getSnapshot/isLoaded）
- ctx.clientTimer（ClientTimerService）
- ClientCordisInspectRegistry

## Depends On (上游依赖)
- `dsh-api-remotes` [编译依赖] - dynamicCordisRunner Remote 命名空间——声明的注入让页面在 host 半不可达时不加载浏览器半
  - 证据: `packages/extensions/cordis-client-runner/src/client/index.ts:181（inject ['remote','remote.dynamicCordisRunner']）；package.json dsh.client.inject 含 @deepseek-ai/dsh-api-remotes`
- `dsh-client-connection` [编译依赖] - wire 类型
  - 证据: `packages/extensions/cordis-client-runner/src/client/runtime.ts:22（import type { SessionId } from '@deepseek-ai/dsh-client-connection/client'）；peerDependencies`
- `dsh-client-modules` [编译依赖] - 模块表类型与 factory 注册/失效（runtime.ts:156 moduleIdOf）
  - 证据: `packages/extensions/cordis-client-runner/src/client/index.ts:18（import type { ClientModuleSystem } from '@deepseek-ai/dsh-client-modules/client'）`
- `dsh-client-runtime` [编译依赖] - slots 服务与类型
  - 证据: `packages/extensions/cordis-client-runner/src/client/index.ts:19（import type { SlotRegistry } from '@deepseek-ai/dsh-client-runtime/client'）；package.json peerDependencies + dsh.client.inject`
- `dsh-client-ui-theme` [运行时依赖] - 动态包可经 ctx.theme.overrideTokens 挂 token 覆盖层
  - 证据: `packages/extensions/cordis-client-runner/package.json dsh.client.inject 含 @deepseek-ai/dsh-client-ui-theme`

## Dependents (下游被依赖)
- `dsh-client-ui-cordis` - 浏览器侧 cordis runner 服务：运行状态快照与 approval 对账
