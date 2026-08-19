# dsh-client-ui-renderer

- 包名: `@deepseek-ai/dsh-client-ui-renderer`
- 分组: G29 UI底座
- 拓扑层: Layer 10
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-renderer`

## 为什么需要它（设计初衷）
统一承载浏览器React渲染骨架(原web-react的React glue)并新增应用根装配与uiRenderer挂载面，成为无框架boot kernel与React UI之间的唯一装配入口。

发展史：RC8 新增(取代 dsh-client-web-react)

## 实现逻辑
纯浏览器插件(immediately=true)。浏览器半 src/client/index.ts:78 调用 ctx.slots.install(createSlotRenderer()) 安装slot渲染器，并通过 ctx.reflect.provide('uiRenderer') 提供 mount 服务：挂载应用根并返回卸载disposer。app.tsx:22 buildRenderApp 构建整棵应用树：SessionDocumentTitle 经 bindSnapshotSelector 订阅会话标题，主布局为 ctx.slots.renderSlot('root',{})；mountApp 通过 hydrateRoot 保留框架无关的启动DOM(data-dsh-boot)。装配于 cordis.patch.yml:191-192(E3)。

## Provides
- ctx.uiRenderer.mount(container) 应用挂载服务
- slot渲染器(createSlotRenderer)安装
- 应用根root slot渲染+DocumentTitle
- 启动DOM hydration

## Depends On (上游依赖)
- `dsh-client-runtime` [运行时依赖] - 依赖slots注册表与sessions服务装配应用
  - 证据: `src/client/index.ts:41 inject ['slots','sessions']`
- `dsh-client-ui-slots` [运行时依赖] - 声明式slot渲染与快照选择器基座
  - 证据: `scoped-slots.tsx:11 import SlotRenderer`

## Dependents (下游被依赖)
- `dsh-web-app` - web-app装配渲染器
