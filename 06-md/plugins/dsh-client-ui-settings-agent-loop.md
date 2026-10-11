# dsh-client-ui-settings-agent-loop

- 包名: `@deepseek-ai/dsh-client-ui-settings-agent-loop`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-agent-loop`

## 实现逻辑
agent-loop 插件设置页（浏览器半）。apply 绑定 settings.agentLoop 字典，从 ctx.configForms 取 agent-loop 命名空间的表单构造 AgentLoopCardController，并只在 Host 仍服务该命名空间时经 slots.inject('plugins.item') 注册页面（order 30），命名空间不被服务则页面上毫无痕迹 (src/client/index.ts:42-49)。卡片在 summary 视图只渲染一行描述，否则渲染仅含一个数值字段 maxParallelToolCalls 的 SettingsForm，其 overridden/invalid/reset 文案全部取自字典 (src/client/AgentLoopCard.tsx:20-40)。Host 半是空 apply，仅为让插件出现在 host cordis.yml / Loader 中，本包不注册任何命名空间 (src/index.ts:10)。

## Provides

## Depends On (上游依赖)
- `dsh-client-locale` [E1+E2] - 页面文案必须经 locale 服务注册并按命名空间绑定翻译
  - 证据: `src/client/index.ts:9 import type {} from '@deepseek-ai/dsh-client-locale/client' + src/client/index.ts:43-44 ctx.locale.bind(NS) / ctx.locale.register(NS, { zh, en })`
- `dsh-client-ui-plugin-manager` [E1+E2] - 页面必须注册进 Plugins 页声明的 plugins.item 槽，注册失败即加载报错
  - 证据: `src/client/AgentLoopCard.tsx:3 import type {} from '@deepseek-ai/dsh-client-ui-plugin-manager/client' + src/client/index.ts:47 ctx.slots.inject('plugins.item', ...)`
- `dsh-client-ui-primitives` [编译依赖] - 设置页复用共享的 SettingsForm 与数值字段控件
  - 证据: `src/client/AgentLoopCard.tsx:4 import SettingsForm/SettingsValueField + package.json:53 devDependencies`
- `dsh-client-ui-renderer` [编译依赖] - 拉入 SlotRegistry 服务合并，使槽注册与 slots.inject 在此编译单元可用
  - 证据: `src/client/index.ts:15 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-settings` [E1+E2] - 读取 agent-loop 命名空间的共享配置表单并做暂存/保存
  - 证据: `src/client/index.ts:12 import type {} from '@deepseek-ai/dsh-client-ui-settings/client' + src/client/index.ts:45 ctx.configForms.get(AGENT_LOOP_NS)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
