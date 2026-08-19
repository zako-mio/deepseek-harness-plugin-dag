# dsh-client-web

- 包名: `@deepseek-ai/dsh-client-web`
- 分组: G26 客户端runtime
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/web`

## 为什么需要它（设计初衷）
Web shell 内核 bootWebShell（模块持有+种子表+两阶段启动+AppRoot 门+app-shell 组装入口），由 apps/web vite 入口消费。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/web-react/README.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-client-web

## 实现逻辑
Web shell kernel（import 底座，无 cordis 行）。AppWebEntry.run() 两阶段启动：① module 面——parseBootManifest 解析 window.__DSH_BOOT__，构建 ClientModuleSystem（modules+staticModules seed 表+loadBundle seams），registerStatic(APP_SHELL_ID, AppShell) 与 MODULES_ID，渲染 AppRoot loading 页；② plugin 面——ctx.plugin(Loader) 后 loader.internal=modules（internal 契约先于任何 entry 注入），订阅 internal/status 投影，await immediately 层 prefetch，创建 [MODULES_ID, ...plugin rows, APP_SHELL_ID] 每行一个 loader entry，loader.await()+assertEntriesActive 全 ACTIVE sweep（fail-loud 列出 pending 缺服务），flip settled。AppRoot 门：boot settled 前只渲染 loading/failure 报告，settled 后调 app-shell 的 renderApp()→ctx.slots.renderSlot('root')。

## Provides
- AppWebEntry（boot kernel）
- AppRoot 门组件
- app-shell 装配 entry（APP_SHELL_ID='@deepseek-ai/dsh-client-app-shell'）
- getStaticModules seed 表
- PLATFORM_MODULES（平台字表）

## Depends On (上游依赖)
- `dsh-client-modules` [编译依赖] - 模块表内核（bootstrap 例外）
  - 证据: `packages/client/web/src/boot.tsx:38-42（import { ClientModuleSystem, parseBootManifest } from '@deepseek-ai/dsh-client-modules/client'）；package.json dependencies`
- `dsh-client-runtime` [编译依赖] - SlotMap 'root' 声明合并（类型面）
  - 证据: `packages/client/web/src/app.tsx:13（import type {} from '@deepseek-ai/dsh-client-runtime/client'）`
- `dsh-client-ui-layout` [运行时依赖] - AppFrame 在 root slot 注册，shell 只做 ctx 级 renderSlot
  - 证据: `packages/client/web/src/app-shell.ts:30（inject ['layout']）`
- `dsh-cordis-host-runner` [运行时依赖] - vendored Loader 挂载与 entry 创建
  - 证据: `packages/client/web/src/boot.tsx:163（await ctx.plugin(Loader)）、:198（loader.create({name})）`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
