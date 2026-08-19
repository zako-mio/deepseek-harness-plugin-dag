# dsh-attachment-local

- 包名: `@deepseek-ai/dsh-attachment-local`
- 分组: G12 附件
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/attachment/attachment-local`

## 为什么需要它（设计初衷）
dsh-attachment 的私有本地实现：DSH_HOME 下基于内容寻址(sha256:)的对象存储，含崩溃安全(原子硬链接发布+目录同步)、图片解码准入校验、只允许所有者访问。会话日志只含引用与校验元数据、不含宿主路径，保证重启/fork 后历史图片可持久回放。

发展史：RC8 拦截超大尺寸图片(维度上限)

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/attachment/attachment-local/README.zh.md
- https://registry.npmjs.org/@deepseek-ai/dsh-attachment-local

## 实现逻辑
image.ts:47-54 新增 DecodedImageLimits(maxPixels + maxDimension 独立边长限制); :57-69 detectImage 在原有解码像素上限外新增每边维度上限，超限抛 IMAGE_DIMENSION_TOO_LARGE，拦截超大尺寸图片。

## Provides
- ctx.attachments(LocalAttachmentStore)
- validateImage/saveImage/readImage
- detectImage/readImageFile 导出

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
