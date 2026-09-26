# dsh-client-ui-settings-general

- 包名: `@deepseek-ai/dsh-client-ui-settings-general`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 13
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-general`

## 实现逻辑
浏览器半渲染 `sidebar.settings` 槽位的设置外壳 SettingsRoot，并声明 settings.launcher/trigger/header/action/close/section/onboarding 等子槽（src/client/index.ts:198-212）；它把 `settings.section` 与 `settings.onboarding` 台账投影为有序导航行/步骤快照（src/client/index.ts:129-172）。无主设置项也在此注册：Developer Tools 行（src/client/index.ts:76-82）、Current version 行（src/client/index.ts:84-86）、仅在 loopback 连接下启用的本地设置文档动作（src/client/index.ts:102-104、220-228）、sidebar.toggle.badge 桌面更新指示（src/client/index.ts:92-95），以及 `settings.open` 快捷键（src/client/index.ts:179-196）。node half 定义 volatile 配置 welcomeNoticeVersion 并经 settings 服务 configure（src/index.ts:15-23）。

## Provides
- sidebar.settings 槽位占用者：设置面板外壳 SettingsRoot，声明 settings.launcher/trigger/header/action/close/section/onboarding 子槽
- settings.section 条目 id='general' (order 0) 及 settings.general.item 子槽（developer-tools order 15、current-version order 100）
- settings.trigger / settings.header / settings.close 单例实现与 settings.action 条目 id='open-document'
- sidebar.toggle.badge 槽的桌面更新徽标
- settings locale 命名空间字典（外壳 + General 文案）
- settings.open 快捷键命令（primary+,）
- Host 侧 settings 命名空间配置项 welcomeNoticeVersion（volatile）

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 判断 loopback 以决定是否注册本地设置文档动作
  - 证据: `src/client/index.ts:12 type-only import + src/client/index.ts:102 ctx.remote.$host.isLoopback`
- `dsh-client-connection` [E1+E2] - 取连接状态用于重连入口与桌面更新徽标
  - 证据: `src/client/shell-contract.ts:9 import type ConnectionState + src/client/index.ts:88 ctx.get('connection')`
- `dsh-client-locale` [E1+E2] - 注册 settings 字典并投影本地化标签
  - 证据: `src/client/index.ts:21 type-only import + src/client/index.ts:100 ctx.locale.bind(NS)`
- `dsh-client-shortcuts` [E1+E2] - 注册设置打开命令并展示快捷键目录
  - 证据: `src/client/shell-contract.ts:20 import type ShortcutCatalogEntry + src/client/index.ts:126 ctx.shortcuts.catalog, src/client/index.ts:179 ctx.shortcuts.register`
- `dsh-client-ui-primitives` [编译依赖] - 复用共享原语关闭顶层模态并渲染设置行
  - 证据: `src/client/index.ts:15 import closeTopModal`
- `dsh-client-ui-renderer` [编译依赖] - 引入 ctx.slots 合并
  - 证据: `src/client/index.ts:22 type-only import`
- `dsh-client-ui-session` [编译依赖] - 引入会话标准 props 合并（设置外壳在会话上下文渲染）
  - 证据: `src/client/index.ts:23 type-only import`
- `dsh-client-ui-settings` [E1+E2] - 设置槽声明与 configForms 镜像由 ui-settings 提供
  - 证据: `src/client/index.ts:19 type-only import + src/client/index.ts:103 ctx.configForms.describe()`
- `dsh-client-ui-sidebar` [编译依赖] - 引用 sidebar 的 SlotMap 与 owner props 类型以渲染该槽占位
  - 证据: `src/client/shell-contract.ts:15 type-only import（SlotMap 'sidebar.settings'）`
- `dsh-settings` [E1+E2] - Host 侧把欢迎版本配置挂到 settings 服务
  - 证据: `src/index.ts:2 type-only import + src/index.ts:23 ctx.inject(['settings']) → child.settings.configure`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
