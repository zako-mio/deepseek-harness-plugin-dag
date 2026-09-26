# dsh-client-ui-brand-official

- 包名: `@deepseek-ai/dsh-client-ui-brand-official`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-brand-official`

## 实现逻辑
官方品牌占位插件：apply 先在进程环境上判 DSH_CLIENT_BUILD_PROFILE !== 'official' 直接返回，非官方构建不注册任何东西 (src/client/index.ts:17)。官方构建下用嵌套 slots.inject 加 generator 一次性装配两个注册：'sidebar.brand.mark' 落 OfficialBrandMark、'sidebar.brand.name' 落 OfficialBrandName，任一失败则整体回滚 (src/client/index.ts:18-22)。conversation hero 品牌位不在此注册，仍走声明包的动画鱼回退。组件用 ui-primitives 渲染 (src/client/Brand.tsx:1)。

## Provides
- slot: sidebar.brand.mark (官方侧边栏品牌标志，仅 official 构建注册)
- slot: sidebar.brand.name (官方侧边栏品牌名，仅 official 构建注册)

## Depends On (上游依赖)
- `dsh-client-ui-primitives` [编译依赖] - 品牌标志与品牌名的呈现组件
  - 证据: `src/client/Brand.tsx:1 import @deepseek-ai/dsh-client-ui-primitives`
- `dsh-client-ui-renderer` [E1+E2] - 引入并驱动槽位注册服务
  - 证据: `src/client/index.ts:3 merge + src/client/index.ts:18 ctx.slots.inject`
- `dsh-client-ui-sidebar` [E1+E2] - 占据侧边栏品牌槽位
  - 证据: `src/client/Brand.tsx:2 import @deepseek-ai/dsh-client-ui-sidebar/client + src/client/index.ts:18-21 ctx.slots.inject('sidebar.brand.*')`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
