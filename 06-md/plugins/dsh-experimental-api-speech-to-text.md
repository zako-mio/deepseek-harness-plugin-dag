# dsh-experimental-api-speech-to-text

- 包名: `@deepseek-ai/dsh-experimental-api-speech-to-text`
- 分组: G13 实验特性
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/experimental/api-speech-to-text`

## 实现逻辑
`SpeechController` 继承 `TypertRemoteService`（命名空间 speech）（src/index.ts:28-37），把 Host 的 `ctx.speechToText` 以 authenticated Remote 暴露给 Client：`catalog()`/`follow()` 读 provider 与就绪快照，`configure/prepare/cancelPreparation` 透传，`transcribe()` 先做 base64 规范性与字节上限校验、`validateWave` 校验录音，再委派识别并映射为稳定 RemoteError（src/index.ts:43-110）。

## Provides
- Remote 命名空间 speech (catalog/follow/configure/prepare/cancelPreparation/transcribe)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-experimental-client-ui-voice-input` - 挂载并调用 speech Remote 命名空间
