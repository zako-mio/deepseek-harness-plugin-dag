# dsh-attachment-local

- 包名: `@deepseek-ai/dsh-attachment-local`
- 分组: G03 附件
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/attachment/attachment-local`

## 实现逻辑
以 `LocalAttachmentStore extends AttachmentStore` 实现本地持久化附件后端：构造时把存储根定为 `DSH_HOME/attachments/v1`，并从 Config 解析图像字节/像素/张数限额与归一化策略，建立 `CompressionLimiter` 并发闸 (src/index.ts:147-201)。图像经 `prepareImageFile` → `commitPreparedImageFile` 落盘，读取分别走 `readImageFile`、`readRequestImageFile`，并用 `SharedRequest` 对同一 variantId 做 in-flight 去重与取消传播 (src/index.ts:207-287)。文件类附件走 verbatim 流式写入/读取 (src/index.ts:232-246)，底层实现分散在 store.ts/file-store.ts/request-image.ts/normalization.ts/sharp.ts。

## Provides
- 本地附件存储后端 (AttachmentStore 服务实现，内容寻址持久化到 $DSH_HOME/attachments/v1)
- 图像限额与归一化能力 (imageLimits、normalizationPolicy，供上层做请求体容量校验)
- 图像归一化与请求级变体工具 (normalizeImage、prepareImageFile、readRequestImageFile、requestImageVariantId)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
