# dsh-client-ui-attachment

- 包名: `@deepseek-ai/dsh-client-ui-attachment`
- 分组: G29 UI底座
- 拓扑层: Layer 1
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-attachment`

## 为什么需要它（设计初衷）
纯 React 附件原子组件（零 cordis 依赖）：草稿图片轨、消息图片画廊与原始图灯箱。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-attachment/package.json

## 实现逻辑
附件渲染 atoms（零 cordis）。AttachmentRail（composer 草稿图片轨）、MessageImage/ImageGallery（聊天历史图片画廊）、ImageLightbox（原图灯箱）、DropOverlay（全页拖放遮罩）；owners 经自己 locale 命名空间解析文案传入（无应用状态读取）。作为纯 React 底座被 ui-conversation 消费。

## Provides
- AttachmentRail
- ImageGallery/MessageImage
- ImageLightbox
- DropOverlay
- ImageLoader/MessageImageLabels 等类型

## Depends On (上游依赖)
- `dsh-client-ui-primitives` [编译依赖] - 基础 atoms
  - 证据: `package.json:31 dependencies`

## Dependents (下游被依赖)
- `dsh-client-ui-conversation` - 图片 draft rail/lightbox/overlay 渲染 atoms
