# dsh-client-ui-agent-preset

- 包名: `@deepseek-ai/dsh-client-ui-agent-preset`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-agent-preset`

## 实现逻辑
浏览器半在同一份 preset 名册上挂三个面：新会话页的 preset chip（conversation.hero.agentPreset）、会话头的只读标签（conversation.session.header.actions）与设置区段（settings.section）（src/client/index.ts:208-274）。它用 AgentPresetSeatController/SectionController/SettingsController 分别维护选择、名册与默认值，按 SessionBinding 缓存 seat，并在 Developer tools 关闭时清空 staged 选择（src/client/index.ts:77-128）。设置文档更新与 connection/reset 触发整体 refresh（src/client/index.ts:151-175）。

## Provides

## Depends On (上游依赖)
- `dsh-agent-preset-registry` [编译依赖] - 读取 preset 名册与展示信息
  - 证据: `src/client/AgentPresetLabel.tsx:17 import + src/client/locales.ts:126`
- `dsh-api-remotes` [E1+E2] - 订阅设置文档更新并做 Remote 调用
  - 证据: `src/client/index.ts:28 import type + src/client/index.ts:163 ctx.remote.$on('settings/document-updated')`
- `dsh-api-session-controller` [E1+E2] - 按会话绑定解析 preset 状态
  - 证据: `src/client/index.ts:21 import type + src/client/index.ts:91 ctx.sessions.binding`
- `dsh-client-locale` [E1+E2] - 注册 settings.agentPreset 字典
  - 证据: `src/client/index.ts:25 import type + src/client/index.ts:130 ctx.locale.register('settings.agentPreset')`
- `dsh-client-ui-conversation` [编译依赖] - 占用 conversation.hero 与 header 槽位声明
  - 证据: `src/client/AgentPresetLabel.tsx:16 import type + src/client/AgentPresetSeat.tsx:22`
- `dsh-client-ui-plugin-manager` [编译依赖] - 在 plugins.add.actions 提供创建入口
  - 证据: `src/client/CreatePluginMenuItem.tsx:5 import`
- `dsh-client-ui-primitives` [编译依赖] - 复用基础控件渲染名册行
  - 证据: `src/client/AgentPresetLabel.tsx:14 import`
- `dsh-client-ui-renderer` [编译依赖] - 渲染器槽位服务类型
  - 证据: `src/client/index.ts:31 import type`
- `dsh-client-ui-settings` [编译依赖] - 占用 settings.section 声明
  - 证据: `src/client/index.ts:30 import type`
- `dsh-client-ui-workspace` [E1+E2] - 创建并落地新会话
  - 证据: `src/client/index.ts:33 import type + src/client/index.ts:204 ctx.uiWorkspace.startSession`
- `dsh-session` [编译依赖] - SessionId 类型
  - 证据: `src/client/index.ts:22 import type`

## Dependents (下游被依赖)
- `dsh-client-ui-settings-plugin-inventory` - 拉入 settings.agentPreset 字典命名空间合并，使预置名可经该字典解析
