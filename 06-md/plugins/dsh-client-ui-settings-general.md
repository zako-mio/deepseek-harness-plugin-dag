# dsh-client-ui-settings-general

- 包名: `@deepseek-ai/dsh-client-ui-settings-general`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 13
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-general`

## 实现逻辑
设置外壳与无归属文案插件。Host 半用 schemastery 声明 welcomeNoticeVersion 这一 volatile 配置，并把本 fiber 以 settings.configure({auto:false}) 挂到 settings 服务上 (src/index.ts:15-23)。浏览器半占据 ui-sidebar 的 sidebar.settings 洞并一次性声明 settings.launcher/trigger/header/action/close/section/onboarding 七个槽 (src/client/index.ts:198-212)，同时把 settings.section 与 settings.onboarding 的注册台账投影为以「槽版本 + locale revision」为缓存键的 uSES 可观察源，订阅两处变更 (src/client/index.ts:117-172)。General 段注册 developer-tools 开关行与版本行 (src/client/index.ts:76-86)；本地设置文档动作仅在 remote.$host.isLoopback 时创建并跟随共享镜像的 hasDocument (src/client/index.ts:102-111, src/client/settings-document-store.ts:43-51)；桌面更新徽标从 globalThis.dshDesktop.updates 桥接 (src/client/index.ts:89-95)。

## Provides
- 声明设置外壳槽位：settings.launcher / settings.trigger / settings.header / settings.action / settings.close / settings.section / settings.onboarding（各功能据此注册自己的设置入口、导航段与引导步骤）
- 声明 General 段的内层列表槽 settings.general.item（供各功能注册设置行）

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 用 Remote 的 $host 事实判断是否 loopback，从而决定是否提供本地文档动作
  - 证据: `src/client/index.ts:12 import type {} from '@deepseek-ai/dsh-api-remotes/client' + src/client/index.ts:102 ctx.remote.$host.isLoopback`
- `dsh-client-connection` [E1+E2] - 外壳的重连动作与连接状态指示器读连接句柄
  - 证据: `src/client/index.ts:13 import ConnectionHandle + src/client/index.ts:88 ctx.get('connection')`
- `dsh-client-locale` [E1+E2] - 注册 settings 字典（外壳 chrome + General 文案）并跟随 locale revision 刷新导航标签
  - 证据: `src/client/index.ts:21 import type {} from '@deepseek-ai/dsh-client-locale/client' + src/client/index.ts:87 ctx.locale.register(NS, { zh, en })`
- `dsh-client-shortcuts` [E1+E2] - 注册 settings.open 快捷键命令并把命令目录暴露给外壳显示
  - 证据: `src/client/index.ts:27 import ShortcutCommandId + src/client/index.ts:126 ctx.shortcuts.catalog + src/client/index.ts:179 ctx.shortcuts.register({ id: 'settings.open' ... })`
- `dsh-client-ui-primitives` [编译依赖] - 设置面板复用连接指示器、模态层工具与关闭顶层弹窗的原语
  - 证据: `src/client/SettingsRoot.tsx:21 import ConnectionIndicatorState + src/client/index.ts:15 import closeTopModal + package.json:62 devDependencies`
- `dsh-client-ui-renderer` [编译依赖] - 拉入 SlotRegistry 服务合并，使槽声明与注册在此编译单元可用
  - 证据: `src/client/index.ts:22 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-session` [编译依赖] - 拉入会话根标准 props 合并，供 onboarding 协调所需的会话派生事实
  - 证据: `src/client/index.ts:23 import type {} from '@deepseek-ai/dsh-client-ui-session/client'`
- `dsh-client-ui-settings` [E1+E2] - Developer Tools 行与本地文档动作经共享配置表单镜像读写
  - 证据: `src/client/index.ts:19 import type {} from '@deepseek-ai/dsh-client-ui-settings/client' + src/client/index.ts:79-80 ctx.configForms.developerTools.enabled / setEnabled`
- `dsh-client-ui-sidebar` [编译依赖] - 外壳占据 ui-sidebar 声明的 sidebar.settings 洞（另有 sidebar.toggle.badge）
  - 证据: `src/client/shell-contract.ts:15 import type {} from '@deepseek-ai/dsh-client-ui-sidebar/client' + src/client/index.ts:175 ctx.slots.inject('sidebar.settings', ...)`
- `dsh-settings` [E1+E2] - Host 半把欢迎提示版本这一偏好登记进 settings 服务，供浏览器半经配置表单读取
  - 证据: `src/index.ts:2 import type {} from '@deepseek-ai/dsh-settings' + src/index.ts:23 ctx.inject(['settings'], child => child.settings.configure({ auto: false }, ctx.fiber))`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
