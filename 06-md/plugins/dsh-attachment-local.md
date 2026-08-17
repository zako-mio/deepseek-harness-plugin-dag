# dsh-attachment-local

- 包名: `@deepseek-ai/dsh-attachment-local`
- 分组: G12 附件
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/attachment/attachment-local`

## 为什么需要它（设计初衷）
dsh-attachment 的私有本地实现：DSH_HOME 下基于内容寻址(sha256:)的对象存储，含崩溃安全(原子硬链接发布+目录同步)、图片解码准入校验、只允许所有者访问。会话日志只含引用与校验元数据、不含宿主路径，保证重启/fork 后历史图片可持久回放。

发展史：位于 packages/attachment/attachment-local，2026-08-10 首批发布，0.1.0-rc.6 转公开。依赖 sharp 处理图片，dsh-attachment 定义身份/校验抽象，本包提供本地存储后端。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/attachment/attachment-local/README.zh.md
- https://registry.npmjs.org/@deepseek-ai/dsh-attachment-local

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
