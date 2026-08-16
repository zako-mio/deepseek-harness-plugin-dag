# dsh-attachment-local

- 包名: `@deepseek-ai/dsh-attachment-local`
- 分组: G12 附件
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/attachment/attachment-local`

## 实现逻辑
实现 AttachmentStore 抽象(默认导出)，内容寻址存储于 DSH_HOME/attachments/v1(objects/<2位前缀>/<sha256>)。saveImage 先 inspectMetadata 完整解码校验，再 durable 写入(fsync staging→link→sync)返回 sha256 引用；readImage 校验摘要与元数据；validateImage 只做准入校验。

## Provides
- ctx.attachments(LocalAttachmentStore)
- validateImage/saveImage/readImage
- detectImage/readImageFile 导出

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
