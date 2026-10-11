# dsh-experimental-client-ui-voice-input

- 包名: `@deepseek-ai/dsh-experimental-client-ui-voice-input`
- 分组: G13 实验特性
- 拓扑层: Layer 15
- 来源层: L3 其余
- 源码路径: `packages/experimental/client-ui-voice-input`

## 实现逻辑
浏览器侧插件把语音 Remote 挂到 ctx.remote.$mount，并在 conversation.input.activity、plugins.bundle.config、plugins.bundle.activation 三个槽位分别注册输入按钮、准备卡片与设置引导 (src/client/mount.ts:20-68)。录音由 client/audio.ts 的 Recording 统一持有，插件卸载时全部释放，麦克风设备选择存于 client-store (src/client/mount.ts:22-35)。readiness.ts 用一个可重连的 Remote 流镜像 Host 的语音目录与连接状态，传输失败只写 error 字段而不改写 Host 就绪状态 (src/client/readiness.ts:20-39)。Host 侧入口为空实现，仅作浏览器插件发现 (src/index.ts:1-3)。

## Provides
- conversation.input.activity / plugins.bundle.config / plugins.bundle.activation 槽位的语音输入 UI
- 麦克风设备选择与录音生命周期 (client-store + Recording)
- 语音目录就绪镜像 (speech.follow 流)

## Depends On (上游依赖)
- `dsh-api-gateway` [编译依赖] - Remote 流载体失败的错误类型来自网关包
  - 证据: `src/client/readiness.ts:3 import { RemoteStreamCarrierError } from '@deepseek-ai/dsh-api-gateway/client' + package.json:51 peerDep`
- `dsh-api-remotes` [E1+E2] - Remote contribution 的挂载由 api-remotes 提供
  - 证据: `src/client/mount.ts:3 import type {} from '@deepseek-ai/dsh-api-remotes/client' + src/client/mount.ts:64 ctx.remote.$mount(contribution) + package.json:39 peerDep`
- `dsh-api-session-controller` [编译依赖] - 客户端会话控制器的声明依赖，保证组合中存在同一份实现
  - 证据: `package.json:40 peerDep`
- `dsh-client-locale` [E1+E2] - 录音与准备流程的全部文案走客户端字典
  - 证据: `src/client/mount.ts:5 import type {} from '@deepseek-ai/dsh-client-locale/client' + src/client/mount.ts:21 ctx.locale.register(NS, { zh, en }) + package.json:41 peerDep`
- `dsh-client-ui-conversation` [编译依赖] - 输入区活动槽位与转写文本插入会话输入框需要会话 UI 的类型面
  - 证据: `src/client/VoiceInput.tsx:4 import type { TokenSpan } from '@deepseek-ai/dsh-client-ui-conversation/client' + src/client/mount.ts:7 import type {} + package.json:42 peerDep`
- `dsh-client-ui-plugin-manager` [E1+E2] - 「打开设置」跳转到 bundle 配置页，依赖插件导航服务
  - 证据: `src/client/mount.ts:13 import type {} from '@deepseek-ai/dsh-client-ui-plugin-manager/client' + src/client/mount.ts:28 ctx.pluginNavigation.openBundle('@deepseek-ai/dsh-experimental-voice-input-bundle') + package.json:53 peerDep`
- `dsh-client-ui-primitives` [编译依赖] - 麦克风按钮、波形与卡片使用客户端基元组件
  - 证据: `src/client/PreparationCard.tsx:3 import from '@deepseek-ai/dsh-client-ui-primitives' + src/client/VoiceInput.tsx:15 import + package.json:43 peerDep`
- `dsh-client-ui-renderer` [编译依赖] - 槽位渲染由 renderer 承担，类型面需要其声明
  - 证据: `src/client/mount.ts:6 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client' + package.json:44 peerDep`
- `dsh-client-ui-session` [编译依赖] - 客户端会话 UI 的声明依赖，保证组合中存在同一份实现
  - 证据: `package.json:45 peerDep`
- `dsh-experimental-api-speech-to-text` [E1+E2] - 转写、配置与准备流程经该 Remote 命名空间进入 Host
  - 证据: `src/client/index.ts:3 import speechRemote from '@deepseek-ai/dsh-experimental-api-speech-to-text/remote' + src/client/mount.ts:36 ctx.remote.speech.transcribe(request, signal) + src/client/mount.ts:4 import type {} from '.../remote' + package.json:49 peerDep`
- `dsh-session` [编译依赖] - 转写结果归属会话，类型面需要会话包声明
  - 证据: `package.json:47 peerDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
