# dsh-experimental-speech-to-text-sensevoice

- 包名: `@deepseek-ai/dsh-experimental-speech-to-text-sensevoice`
- 分组: G13 实验特性
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/experimental/speech-to-text-sensevoice`

## 实现逻辑
本地 SenseVoice 识别 provider：`apply()` 先校验 dataRoot/modelDirectory/vadModelPath 必须是绝对路径、model origin 合法，再创建 `SenseVoiceWorker` 并注册到 `ctx.speechToText.register`（info/preparation/transcribe），激活时只调用 `worker.inspect()` 检查磁盘缓存、不下载也不加载模型（src/index.ts:20-41）。识别工作进程经 `ctx.subprocess` 执行（src/recognizer.ts:262），卸载时反注册并 await worker.dispose（src/index.ts:36-40）。

## Provides
- SpeechProvider 注册 (host-local SenseVoiceSmall 识别器)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
