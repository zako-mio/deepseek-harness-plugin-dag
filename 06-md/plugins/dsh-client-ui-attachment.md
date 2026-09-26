# dsh-client-ui-attachment

- 包名: `@deepseek-ai/dsh-client-ui-attachment`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 17
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-attachment`

## 实现逻辑
纯呈现插件：apply 只依赖 slots，把 ComposerAttachments 注册进 'conversation.input.attachments'，把 MessageImages 分别注册进 'conversation.message.images'、'conversation.trajectory.images' 与 'tool.call.images' 四个洞 (src/client/index.ts:16-33)。拖拽逻辑是独立的文档级监听器 installDocumentDropEvents，以 dragDepth 计数判断拖入/拖出、用 webkitGetAsEntry 识别目录，并在 drop 时回调 onAddFiles(files, directories) (src/client/drop-events.ts:9-87)。图片渲染用 dsh-attachment 的 ImageAttachmentRef 与 primitives 完成 (src/MessageImage.tsx:2-5)。宿主半为空 apply (src/index.ts)。

## Provides
- slot: conversation.input.attachments (输入框附件条 ComposerAttachments)
- slot: conversation.message.images (消息图片画廊 MessageImages)
- slot: conversation.trajectory.images (轨迹视图图片画廊)
- slot: tool.call.images (工具调用图片画廊，复用消息画廊渲染器)
- 组件 AttachmentRail/DropOverlay/FileCard 与文档级文件拖放监听器 installDocumentDropEvents

## Depends On (上游依赖)
- `dsh-client-ui-chat` [E1+E2] - 依赖 Chat 视图声明的 conversation.message.images 槽
  - 证据: `src/client/MessageImages.tsx:1 import @deepseek-ai/dsh-client-ui-chat/client + src/client/index.ts:3 type merge`
- `dsh-client-ui-conversation` [E1+E2] - 占据 composer/message/trajectory 图片槽位
  - 证据: `src/client/drop-events.ts:2 ComposerAttachmentsProps + src/client/index.ts:16-27 ctx.slots.inject('conversation.*')`
- `dsh-client-ui-primitives` [编译依赖] - 附件卡片与图片画廊的基础组件
  - 证据: `src/FileCard.tsx:1 import @deepseek-ai/dsh-client-ui-primitives`
- `dsh-client-ui-renderer` [E1+E2] - 引入并驱动槽位注册服务
  - 证据: `src/client/index.ts:5 merge + src/client/index.ts:16 ctx.slots.inject`
- `dsh-client-ui-tool` [E1+E2] - 占据工具调用图片槽
  - 证据: `src/client/index.ts:6 merge + src/client/index.ts:30 ctx.slots.inject('tool.call.images')`
- `dsh-client-ui-trajectory` [E1+E2] - 占据轨迹视图图片槽
  - 证据: `src/client/index.ts:7 merge + src/client/index.ts:24 ctx.slots.inject('conversation.trajectory.images')`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
