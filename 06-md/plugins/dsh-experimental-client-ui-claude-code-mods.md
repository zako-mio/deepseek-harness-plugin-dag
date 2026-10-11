# dsh-experimental-client-ui-claude-code-mods

- 包名: `@deepseek-ai/dsh-experimental-client-ui-claude-code-mods`
- 分组: G13 实验特性
- 拓扑层: Layer 12
- 来源层: L3 其余
- 源码路径: `packages/experimental/client-ui-claude-code-mods`

## 实现逻辑
浏览器侧插件：把桥接服务的 Remote contribution 挂到 ctx.remote.$mount，并在 conversation.input.dock 槽位注册 band 组件 (src/client/mount.ts:117-131, src/client/mount.ts:95-108)。每个会话持有一个 BandStore，用 ctx.remote.claudeCodeMods.watchBand 流持续喂快照，pressBand 回传按钮点击并把结果写回 store；流结束即释放，下次订阅重开 (src/client/mount.ts:55-75, src/client/mount.ts:102-106)。Band.tsx 递归渲染 mod 序列化的 Text/Button/Box 节点，按钮点击映射为 actionId 的 press，失败时显示本地化提示，hotkey 只作提示 (src/client/Band.tsx:70-129)。Host 侧入口为空实现，仅用于浏览器插件发现 (src/index.ts:1-4)。

## Provides
- conversation.input.dock 槽位的 mods band UI
- claude-code-mods 本地化命名空间 (LocaleNamespaceMap 扩展)

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - Remote contribution 的挂载与 remote 服务由 api-remotes 提供
  - 证据: `src/client/mount.ts:4 import type {} from '@deepseek-ai/dsh-api-remotes/client' + src/client/mount.ts:118 ctx.remote.$mount(contribution) + package.json:52 peerDep`
- `dsh-api-session-controller` [编译依赖] - 客户端类型面需要会话控制器声明以取得会话身份
  - 证据: `src/client/mount.ts:5 import type {} from '@deepseek-ai/dsh-api-session-controller/client' + package.json:53 peerDep`
- `dsh-client-locale` [E1+E2] - band 文案走客户端字典而非硬编码
  - 证据: `src/client/mount.ts:6 import type {} from '@deepseek-ai/dsh-client-locale/client' + src/client/mount.ts:78 ctx.locale.register(NS, { zh, en }) + package.json:54 peerDep`
- `dsh-client-ui-conversation` [编译依赖] - 类型面需要会话 UI 声明以定位输入区槽位
  - 证据: `src/client/mount.ts:7 import type {} from '@deepseek-ai/dsh-client-ui-conversation/client' + package.json:55 peerDep`
- `dsh-client-ui-primitives` [编译依赖] - 客户端基元组件的声明依赖，保证组合中存在同一份实现
  - 证据: `package.json:56 peerDep`
- `dsh-client-ui-renderer` [编译依赖] - 槽位渲染由 renderer 承担，类型面需要其声明
  - 证据: `src/client/mount.ts:8 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client' + package.json:57 peerDep`
- `dsh-client-ui-session` [编译依赖] - 客户端会话 UI 的声明依赖，保证组合中存在同一份实现
  - 证据: `package.json:58 peerDep`
- `dsh-experimental-claude-code-mods` [E1+E2] - band 数据与按键回传都来自桥接服务的 Remote 命名空间
  - 证据: `src/client/index.ts:4 import modsRemote from '@deepseek-ai/dsh-experimental-claude-code-mods/remote' + src/client/mount.ts:58 ctx.remote.claudeCodeMods.watchBand(sessionId, controller.signal) + src/client/Band.tsx:3 import type { SurfaceSnapshot } + package.json:60 peerDep`
- `dsh-session` [编译依赖] - band 按 SessionId 归属与缓存
  - 证据: `src/client/mount.ts:11 import type { SessionId } from '@deepseek-ai/dsh-session/types' + package.json:61 peerDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
