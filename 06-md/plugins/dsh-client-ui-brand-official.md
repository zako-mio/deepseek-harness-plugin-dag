# dsh-client-ui-brand-official

- 包名: `@deepseek-ai/dsh-client-ui-brand-official`
- 分组: G29 UI底座
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-brand-official`

## 为什么需要它（设计初衷）
将官方DeepSeek品牌视觉从通用sidebar/conversation slot中解耦为独立插件，按official构建profile选择性注入，使非官方部署可替换品牌而不改UI框架代码。

发展史：RC8 新增

## 实现逻辑
纯浏览器UI插件(node半apply为空占位)。浏览器半 src/client/index.ts:14 apply 在 DSH_CLIENT_BUILD_PROFILE==='official' 时调用 ctx.slots.inject 将官方品牌注入三个brand slot(sidebar.brand.mark/name、conversation.hero.brand.mark)，每slot register一个React组件；Brand.tsx:12 OfficialBrandMark 用 ui-primitives 的 FishLogo 渲染鲸鱼标志，OfficialBrandName 渲染名称字标。装配于 cordis.patch.yml:213-214(E3)。

## Provides
- ctx.slots 品牌slot填充(sidebar.brand.mark/name、conversation.hero.brand.mark)
- 官方鱼标志FishLogo与名称字标BrandWordmark的React呈现
- 仅official构建profile生效的brand占位

## Depends On (上游依赖)
- `dsh-client-runtime` [运行时依赖] - 注入品牌slot所需slots注册表
  - 证据: `src/client/index.ts:14 apply(ctx); peerDependencies`
- `dsh-client-ui-conversation` [编译依赖] - 填充会话Hero品牌slot contract
  - 证据: `src/client/index.ts:21 注册conversation.hero.brand.mark`
- `dsh-client-ui-primitives` [运行时依赖] - 复用官方品牌图形组件
  - 证据: `Brand.tsx:1 import BrandWordmark, FishLogo`
- `dsh-client-ui-sidebar` [编译依赖] - 填充侧边栏品牌slot contract
  - 证据: `src/client/index.ts:19 注册sidebar.brand.* slot`

## Dependents (下游被依赖)
- `dsh-web-app` - web-app装配官方品牌
