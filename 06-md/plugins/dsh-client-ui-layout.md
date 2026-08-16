# dsh-client-ui-layout

- 包名: `@deepseek-ai/dsh-client-ui-layout`
- 分组: G29 UI底座
- 拓扑层: Layer 13
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-layout`

## 实现逻辑
三栏 AppFrame UI 底座。apply() 内一次 register('root') 贡献 AppFrame 并声明四个 child slot（sidebar/conversation/details/shell.overlay），seat 布局 store（面板几何），inject hook 将 bound actions attach 给 LayoutController 后 ctx.reflect.provide('layout')；第二个 effect 起 ThemePresenter 把 ctx.theme 快照投影到 document.body（theme/change 事件驱动，纯 DOM 写）。

## Provides
- ctx.layout（ILayout: toggleSidebar/openDetails/closeDetails）
- slot 声明: root 的 4 个 child — sidebar(single/root), conversation(single/session-maybe), details(single/session), shell.overlay(list/root)
- AppFrame 三栏组件 + 布局 store（面板几何）
- ThemePresenter（theme→document.body）

## Depends On (上游依赖)
- `dsh-client-runtime` [运行时依赖] - runtime 内建 'root' slot 与 reflect.provide 服务发布面
  - 证据: `index.ts:116-137 ctx.reflect.provide('layout') + slots.register({name:'root'...}) + package.json:47 peerDependencies`
- `dsh-client-ui-slots` [编译依赖] - slot 注册 API 与 SlotMap 合并面
  - 证据: `index.ts:33-85 declare SlotMap merge + store: createLayoutStore`
- `dsh-client-ui-theme` [运行时依赖] - ctx.theme 服务与主题事件流
  - 证据: `index.ts:11 type-only + index.ts:108 inject 'theme' + index.ts:149/150 ctx.theme.getTheme()/on('theme/change')`

## Dependents (下游被依赖)
- `dsh-client-ui-conversation` - 三栏框架提供 conversation/details 父 slot + ctx.layout 面板动作
- `dsh-client-ui-settings-general` - 说明壳归因避免引用环
- `dsh-client-ui-sidebar` - 消费 sidebar 列座位与 ctx.layout 面板动作
- `dsh-client-web` - AppFrame 在 root slot 注册，shell 只做 ctx 级 renderSlot
