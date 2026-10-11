# dsh-experimental-speech-to-text-sensevoice

- 包名: `@deepseek-ai/dsh-experimental-speech-to-text-sensevoice`
- 分组: G13 实验特性
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/experimental/speech-to-text-sensevoice`

## 实现逻辑
函数式插件，向 speechToText 注册一个本地 SenseVoice 提供者：提供者信息含 id、host-local 位置、语言列表、下载源与磁盘/内存/耗时估算，准备与转写都委托给 SenseVoiceWorker (src/index.ts:20-41)。激活期只校验路径必须是绝对路径、modelOrigin(s) 必须是合法 URL，不做任何下载或模型加载；注册后 worker.inspect() 只检查磁盘缓存 (src/index.ts:20-35)。全部部署可变项（数据根、模型目录、精度、线程数、VAD 阈值、各类超时、音频/响应字节上限等）都由 Config 在激活期校验 (src/config.ts:56-81)。

## Provides
- ctx.speechToText 的 SenseVoice 本地提供者 (providerId 注册、准备/下载、转写)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
