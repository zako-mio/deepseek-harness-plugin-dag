# dsh-client-ui-agent-preset

- 包名: `@deepseek-ai/dsh-client-ui-agent-preset`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-agent-preset`

## 实现逻辑
浏览器半用 AgentPresetSettingsController/AgentPresetSectionController/AgentPresetSeatController 三个控制器驱动同一份 preset 名册：apply 先把 ctx.configForms.developerTools 作为唯一门控（关闭时清空暂存并重算所有 seat）(src/client/index.ts:104-111)，再经 ctx.inject(['slots','conversation','sessions','uiWorkspace']) 向 'conversation.hero.agentPreset' 注册新会话 chip、向 'conversation.session.header.actions' 以 order -10 注册会话头只读标签 (src/client/index.ts:153-196)，最后以 order 20 向 'settings.section' 注册名册设置段 (src/client/index.ts:223-230)。名册与默认值经 ctx.remote 读取 settings、并在 settings/document-updated 与 connection/reset 时统一 refresh (src/client/index.ts:127-145)。宿主半为空 apply，仅让插件出现在 Loader (src/index.ts:9)。

## Provides
- slot: conversation.hero.agentPreset (新会话界面的 preset 选择 chip，注入 agentPresetSeat/developerTools hooks)
- slot: conversation.session.header.actions#agent-preset (order -10 的会话头只读 preset 标签)
- slot: settings.section#agent-presets (General settings 中的 preset 名册段：选择、设为默认、组合只读视图、进入 Creator)
- Locale 命名空间 settings.agentPreset (zh/en 字典，经 LocaleNamespaceMap 合并声明)
- 导出类型 AgentPresetSeatState/AgentPresetSectionState/AgentPresetSettingsState 与 writeDefaultPreset

## Depends On (上游依赖)
- `dsh-agent-preset-registry` [编译依赖] - 消费 preset 组合类型与 display 文案
  - 证据: `src/client/AgentPresetLabel.tsx:17 import @deepseek-ai/dsh-agent-preset-registry/types + src/client/locales.ts:114-115`
- `dsh-api-remotes` [E1+E2] - 读取 preset 名册并订阅设置文档变更
  - 证据: `src/client/index.ts:26-28 ctx.remote merge + src/client/index.ts:136 ctx.remote.$on('settings/document-updated')`
- `dsh-api-session-controller` [E1+E2] - 按会话解析 binding 与保留态以决定 seat 归属
  - 证据: `src/client/index.ts:20-21 SessionBinding 类型 + src/client/index.ts:83-86 ctx.sessions.binding/retainInfo`
- `dsh-client-locale` [E1+E2] - 注册并绑定 settings.agentPreset 字典
  - 证据: `src/client/index.ts:24-25 ctx.locale merge + src/client/index.ts:122 ctx.locale.register('settings.agentPreset')`
- `dsh-client-ui-conversation` [E1+E2] - 获取 conversation.hero.*/session.header.actions 槽声明与 conversation 作用域
  - 证据: `src/client/AgentPresetLabel.tsx:16 import @deepseek-ai/dsh-client-ui-conversation/client + src/client/index.ts:153 ctx.inject(['slots','conversation',...])`
- `dsh-client-ui-primitives` [编译依赖] - 复用基础 UI 组件渲染 chip 与设置行
  - 证据: `src/client/AgentPresetLabel.tsx:14 import @deepseek-ai/dsh-client-ui-primitives`
- `dsh-client-ui-renderer` [编译依赖] - 引入 ctx.slots 服务声明
  - 证据: `src/client/index.ts:31 import @deepseek-ai/dsh-client-ui-renderer/client`
- `dsh-client-ui-settings` [E1+E2] - 向设置壳注册 agent-presets 段
  - 证据: `src/client/index.ts:30 SlotMap merge + src/client/index.ts:223 ctx.slots.inject('settings.section')`
- `dsh-client-ui-workspace` [E1+E2] - Creator 模式起草后落到新会话
  - 证据: `src/client/index.ts:32-33 ctx.uiWorkspace merge + src/client/index.ts:174 scope.uiWorkspace.startSession()`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/index.ts:22 import SessionId from @deepseek-ai/dsh-session/types`

## Dependents (下游被依赖)
- `dsh-client-ui-settings-plugin-inventory` - 借用预设字典解析内置 agent 预设显示名
