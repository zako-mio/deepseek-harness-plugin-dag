# dsh-experimental-client-ui-voice-input

- 包名: `@deepseek-ai/dsh-experimental-client-ui-voice-input`
- 分组: G13 实验特性
- 拓扑层: Layer 16
- 来源层: L3 其余
- 源码路径: `packages/experimental/client-ui-voice-input`

## 实现逻辑
Host 半边为空 `apply()`，行为在浏览器侧（src/index.ts:3）。Client 入口把生成的 speech Remote contribution 经 `ctx.remote.$mount` 挂载为实验命名空间，然后注册 UI（src/client/index.ts:13-14、src/client/mount.ts:60-65）：locale 字典、录音集合生命周期、readiness 观察、composer `conversation.input.activity` 的 VoiceInput 槽，以及 voice-input bundle 的配置/激活槽（src/client/mount.ts:19-51）。动作层把 transcribe/configure/prepare 委派给 `ctx.remote.speech`（src/client/mount.ts:33-40）。

## Provides

## Depends On (上游依赖)
- `dsh-api-gateway` [编译依赖] - 经网关检测语音后端可用性
  - 证据: `src/client/readiness.ts:3 import '@deepseek-ai/dsh-api-gateway/client'`
- `dsh-api-remotes` [E1+E2] - 在 Client 注册实验 Remote 贡献
  - 证据: `src/client/mount.ts:3 import '@deepseek-ai/dsh-api-remotes/client' + src/client/mount.ts:17 inject 'remote' + src/client/mount.ts:61 remote.$mount`
- `dsh-client-locale` [E1+E2] - 注册语音相关中英文文案
  - 证据: `src/client/mount.ts:5 import '@deepseek-ai/dsh-client-locale/client' + src/client/mount.ts:17 inject 'locale' + src/client/mount.ts:20 locale.register`
- `dsh-client-ui-conversation` [编译依赖] - 在输入区渲染麦克风控件
  - 证据: `src/client/VoiceInput.tsx:4 import '@deepseek-ai/dsh-client-ui-conversation/client' + src/client/mount.ts:7 import`
- `dsh-client-ui-plugin-manager` [E1+E2] - 跳转到 voice-input 插件 bundle 进行模型准备
  - 证据: `src/client/VoiceSetupDialog.tsx:4 import '@deepseek-ai/dsh-client-ui-plugin-manager/client' + src/client/mount.ts:17 inject 'pluginNavigation' + src/client/mount.ts:26 openBundle`
- `dsh-client-ui-primitives` [编译依赖] - 复用基础 UI 组件
  - 证据: `src/client/PreparationCard.tsx:3 + src/client/VoiceInput.tsx:13 + src/client/VoiceSetupDialog.tsx:2 import '@deepseek-ai/dsh-client-ui-primitives'`
- `dsh-client-ui-renderer` [编译依赖] - 让注册组件进入渲染管线
  - 证据: `src/client/mount.ts:6 import '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-experimental-api-speech-to-text` [编译依赖] - 挂载并调用 speech Remote 命名空间
  - 证据: `src/client/index.ts:3 import '@deepseek-ai/dsh-experimental-api-speech-to-text/remote' + src/client/mount.ts:4 import`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
