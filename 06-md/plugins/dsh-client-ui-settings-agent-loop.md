# dsh-client-ui-settings-agent-loop

- 包名: `@deepseek-ai/dsh-client-ui-settings-agent-loop`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-agent-loop`

## 实现逻辑
浏览器半在 apply 中注册 `settings.agentLoop` 字典并把 AgentLoopCardController 绑定到 Host 侧 `agent-loop` 设置命名空间的 staged form（src/client/index.ts:43-46）；待 Host 服务该命名空间后，经 `ctx.slots.inject('plugins.item')` 把卡片注册进 Plugins 页（src/client/index.ts:47-49）。控制器用 `settingsNumberField('maxParallelToolCalls')` 构造 SettingsFormModel，并把表单状态投影为 store 快照与 actions 注入面（src/client/agent-loop-card-controller.ts:44-59）。卡片按 `view === 'summary'` 输出一行描述，否则渲染只含并行工具调用上限的 SettingsForm（src/client/AgentLoopCard.tsx:20-40）。node half 为空 apply，仅用于让该插件出现在宿主 Loader（src/index.ts:10）。

## Provides
- settings.agentLoop locale 命名空间字典（zh/en 文案）
- plugins.item 槽位条目 id='agent-loop' (order 20)：agent 循环并行工具调用上限设置卡片
- AgentLoopCardFace 注入面（staged form actions + useAgentLoopCard 快照）

## Depends On (上游依赖)
- `dsh-client-locale` [E1+E2] - 注册并绑定本页文案字典
  - 证据: `src/client/index.ts:9 type-only import + src/client/index.ts:43 ctx.locale.bind(NS)`
- `dsh-client-ui-plugin-manager` [E1+E2] - Plugins 页拥有 plugins.item 槽位，本包向其贡献页面
  - 证据: `src/client/index.ts:14 type-only import + src/client/index.ts:47-48 向 plugins.item 注册条目`
- `dsh-client-ui-primitives` [编译依赖] - 复用共享设置表单原语渲染数值字段
  - 证据: `src/client/AgentLoopCard.tsx:4 import SettingsForm/SettingsValueField`
- `dsh-client-ui-renderer` [编译依赖] - 引入 ctx.slots 的 SlotRegistry Context 合并
  - 证据: `src/client/index.ts:15 type-only import`
- `dsh-client-ui-settings` [E1+E2] - 经 configForms 服务取得 agent-loop 命名空间的设置表单 scope
  - 证据: `src/client/index.ts:12 type-only import + src/client/index.ts:45 ctx.configForms.get(AGENT_LOOP_NS)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
