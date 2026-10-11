# dsh-experimental-client-ui-cot-translation

- 包名: `@deepseek-ai/dsh-experimental-client-ui-cot-translation`
- 分组: G13 实验特性
- 拓扑层: Layer 15
- 来源层: L3 其余
- 源码路径: `packages/experimental/client-ui-cot-translation`

## 实现逻辑
Host 侧 TypertRemoteService ctx.cotTranslation 暴露两个 Remote：limits 返回已接受偏好、可用提供者与单次请求字符上限；translate 先按当前偏好校验 provider/targetLanguage，再调 ctx.translator.translate，遇 TRANSLATION_SESSION_INACTIVE 时经 ctx.sessionController.resolveAgent 激活会话后重试一次，失败一律收敛为不含原文的 RemoteError (src/index.ts:46-101)。偏好由 schemastery volatile 字段承载，并用 settings.configure({ auto: false }) 让部署值成为权威 (src/index.ts:31-39)。浏览器侧把 Remote 挂到 conversation.chat.reasoning.body 与 plugins.bundle.config 槽位，用 client-store 快照保存偏好/上限/可用提供者，并在设置、LLM 适配器、凭据等更新事件与 connection/reset 上失效重读 (src/client/mount.ts:22-111)。translation.ts 把推理文本按空行与字符上限切段，串行请求、按生命周期控制器取消并缓存已译片段 (src/client/translation.ts:20-113)。

## Provides
- ctx.cotTranslation Remote 服务 (limits/translate：展示中推理文本的机器翻译)
- conversation.chat.reasoning.body 与 plugins.bundle.config 槽位 UI (译文展示与偏好表单)
- RemoteError 分类: cotTranslation/failed

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - Remote 命名空间的挂载与调用由 api-remotes 提供
  - 证据: `src/client/mount.ts:4 import type {} from '@deepseek-ai/dsh-api-remotes/client' + src/client/mount.ts:125 ctx.remote.$mount(contribution) + src/client/mount.ts:96 ctx.remote.cotTranslation.translate + package.json:74 devDep`
- `dsh-api-session-controller` [E1+E2] - 未激活会话需要先走 GUI 激活流程才能翻译
  - 证据: `src/index.ts:7 import type {} from '@deepseek-ai/dsh-api-session-controller' + src/index.ts:74 ctx.sessionController.resolveAgent(spec.sessionId) + package.json:63 peerDep`
- `dsh-client-locale` [E1+E2] - 译文区与表单文案走客户端字典
  - 证据: `src/client/mount.ts:5 import type {} from '@deepseek-ai/dsh-client-locale/client' + src/client/mount.ts:83 ctx.locale.register(NS, { en, zh }) + package.json:75 devDep`
- `dsh-client-ui-chat` [编译依赖] - 译文挂在推理正文槽位，需要 chat 侧的槽位与类型声明
  - 证据: `src/client/mount.ts:6 import type {} from '@deepseek-ai/dsh-client-ui-chat/client' + src/client/TranslationBody.tsx:5 import from '@deepseek-ai/dsh-client-ui-chat/client' + package.json:78 devDep`
- `dsh-client-ui-plugin-manager` [E1+E2] - 偏好表单注册进 bundle 配置页，表单作用域由 configForms 服务提供
  - 证据: `src/client/mount.ts:9 import type {} from '@deepseek-ai/dsh-client-ui-plugin-manager/client' + src/client/mount.ts:81 ctx.configForms.get<CotTranslationPreferences>('cot-translation') + src/client/TranslationSettings.tsx:2 import type {} + package.json:79 devDep`
- `dsh-client-ui-primitives` [编译依赖] - 译文按钮与表单控件使用客户端基元组件
  - 证据: `src/client/TranslationBody.tsx:3 import { Button, IconLoadingOutlineRegular } + src/client/TranslationSettings.tsx:5 import + package.json:80 devDep`
- `dsh-client-ui-renderer` [编译依赖] - 槽位渲染由 renderer 承担，类型面需要其声明
  - 证据: `src/client/mount.ts:7 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client' + package.json:81 devDep`
- `dsh-client-ui-settings` [编译依赖] - 设置页面的槽位与类型声明来自 settings UI 包
  - 证据: `src/client/mount.ts:8 import type {} from '@deepseek-ai/dsh-client-ui-settings/client' + package.json:82 devDep`
- `dsh-session` [编译依赖] - 翻译请求携带会话身份，会话未激活时才需要激活
  - 证据: `src/client/mount.ts:3 import type { SessionId } from '@deepseek-ai/dsh-session/types' + package.json:62 peerDep`
- `dsh-settings` [E1+E2] - 翻译偏好是设置文档的一部分，并声明部署值为权威
  - 证据: `src/index.ts:6 import type {} from '@deepseek-ai/dsh-settings' + src/index.ts:38 child.settings.configure({ auto: false }, ctx.fiber) + package.json:60 peerDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
