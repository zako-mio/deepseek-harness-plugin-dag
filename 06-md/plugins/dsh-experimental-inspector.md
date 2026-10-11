# dsh-experimental-inspector

- 包名: `@deepseek-ai/dsh-experimental-inspector`
- 分组: G13 实验特性
- 拓扑层: Layer 13
- 来源层: L3 其余
- 源码路径: `packages/experimental/inspector`

## 实现逻辑
双面插件。Host 面在 ctx.effect 里启动 Inspector Worker，ctx.provide('inspector', createInspectorService(...)) 暴露服务，把 Client bootstrap 注入 index 表、注册 /inspector/devtools 静态资源与 /inspector/devtools/cdp 的 WebSocket 升级代理（先经 connection 鉴权）(src/host/plugin.ts:49-163)。Client 面同样 provide 'inspector'，从 __DSH_INSPECTOR__ 或 bootstrap 路由读取端点后建立到 Worker 的源，并把底部检查器页面注册进 slots/shortcuts/locale (src/client/plugin.ts:50-151)。两侧共享同一套桥接协议编解码与 Cordis 拓扑读取实现 (src/shared/**)，使宿主与浏览器可以互相观测；enable 状态与各项字节/条数上限全部由 Config 校验 (src/index.ts:74-107)。

## Provides
- ctx.inspector (跨 realm 观测发布与 Cordis 拓扑只读查询，Host 与 Client 两面)
- CDP/DevTools 前端资源与 WebSocket 代理路由 (/inspector/devtools 与 /inspector/devtools/cdp)
- 底部检查器 UI 与 shell.bottom 槽位、快捷键贡献

## Depends On (上游依赖)
- `dsh-client-connection` [E1+E2] - bootstrap 端点与 DevTools 路由都要经连接层的鉴权与路由表
  - 证据: `src/host/plugin.ts:9 import type {} from '@deepseek-ai/dsh-client-connection' + src/host/plugin.ts:64 ctx.connection.fetch.register({ path: INSPECTOR_BOOTSTRAP_PATH, ... }) + src/host/plugin.ts:82 ctx.connection.authorizeIndex(req, res) + src/client/plugin.ts:4 import type {} + package.json:61 peerDep`
- `dsh-client-locale` [E1+E2] - 检查器面板文案走客户端字典
  - 证据: `src/client/bottom/page.tsx:11 import type {} from '@deepseek-ai/dsh-client-locale/client' + src/client/bottom/page.tsx:61 ctx.locale.register('inspectorPanel', { zh, en }) + package.json:76 devDep`
- `dsh-client-modules` [编译依赖] - 浏览器端模块装载的声明依赖，保证组合中存在同一份实现
  - 证据: `package.json:60 peerDep`
- `dsh-client-shortcuts` [E1+E2] - 检查器面板的开关快捷键注册在客户端快捷键目录上
  - 证据: `src/client/bottom/keyboard.ts:2 import type { ShortcutCatalogEntry } from '@deepseek-ai/dsh-client-shortcuts/client' + src/client/bottom/page.tsx:71 ctx.shortcuts.register({...}) + src/client/bottom/page.tsx:94 ctx.shortcuts.catalog.getSnapshot() + package.json:72 devDep`
- `dsh-client-ui-layout` [编译依赖] - 面板的布局约束与类型声明来自布局包
  - 证据: `src/client/bottom/page.tsx:9 import type {} from '@deepseek-ai/dsh-client-ui-layout/client' + package.json:71 devDep`
- `dsh-client-ui-primitives` [编译依赖] - 检查器面板的按钮与提示使用客户端基元组件
  - 证据: `src/client/bottom/page.tsx:6 import { Button, IconCloseOutlineRegular, Tooltip } + package.json:75 devDep`
- `dsh-client-ui-renderer` [编译依赖] - 槽位渲染由 renderer 承担，类型面需要其声明
  - 证据: `src/client/bottom/page.tsx:10 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client' + package.json:69 devDep`
- `dsh-host-webserver` [E1+E2] - DevTools 前端资源与 CDP 代理需要宿主 HTTP 服务器的路由与升级钩子
  - 证据: `src/host/plugin.ts:8 import type { IndexInjection } from '@deepseek-ai/dsh-host-webserver' + src/host/plugin.ts:75 ctx.webServer.register({ kind: 'prefix', path: DEVTOOLS_PATH, ... }) + src/host/plugin.ts:111 ctx.webServer.registerUpgrade + src/index.ts:63 export const inject = ['webServer', 'connection'] + package.json:62 peerDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
