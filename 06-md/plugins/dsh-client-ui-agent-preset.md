# dsh-client-ui-agent-preset

- 包名: `@deepseek-ai/dsh-client-ui-agent-preset`
- 分组: G28 设置输入UI
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-agent-preset`

## 实现逻辑
Agent preset 四面体：settings.general.item AgentPresetRow 默认值（index.ts:207-213）、conversation.hero.agentPreset 新会话 chip（:165-169）、header 只读 label（:170-177）、settings.section 'agent-presets' 名录管理/复制/删除/默认 + composition 编辑器（:216-223）。控制器 AgentPresetSettingsController/SectionController/SeatController 经 connection.api 读写 host agent-presets 设置命名空间（settings-store.ts:14 AGENT_PRESET_SETTINGS_NS='agent-presets', :43 writeDefaultPreset）；订阅 settings/document-updated 与 agent-preset/selected 事件。

## Provides
- settings.general.item 'agent-preset' 行
- conversation.hero.agentPreset chip (AgentPresetSeat)
- conversation.session.header.actions 'agent-preset' label
- settings.section 'agent-presets' (AgentPresetSection 名录/编辑器)

## Depends On (上游依赖)
- `dsh-agent-presets` [运行时依赖] - host 名录 roster 与默认 preset 持久化
  - 证据: `packages/client/ui-agent-preset/src/client/settings-store.ts:43 (api.settings.update AGENT_PRESET_SETTINGS_NS), cordis.patch.yml:420-424 (agent-presets host 行 default: standard)`
- `dsh-client-connection` [运行时依赖] - 设置/名录远程调用载体
  - 证据: `packages/client/ui-agent-preset/src/client/index.ts:56-57,103 (connection.api 构造控制器)`
- `dsh-client-ui-conversation` [编译依赖] - 新会话 chip、header label 槽与 session flow
  - 证据: `packages/client/ui-agent-preset/src/client/index.ts:102,165-177 (inject conversation/sessions/workspaces + hero/header 槽)`
- `dsh-client-ui-settings` [编译依赖] - Settings 槽声明与命名空间 scope
  - 证据: `packages/client/ui-agent-preset/src/client/index.ts:21,49,207-223 (type-only import + settings.general.item/settings.section 注册)`
- `dsh-session` [运行时依赖] - 会话行 preset 折入与选中回写
  - 证据: `packages/client/ui-agent-preset/src/client/index.ts:105-115 (sessions.list 快照 + noteAgentPreset)`
- `dsh-workspace` [运行时依赖] - 创作后落新会话
  - 证据: `packages/client/ui-agent-preset/src/client/index.ts:102,163 (inject workspaces + workspaces.startSession)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
