# dsh-client-ui-settings-plugin-inventory

- 包名: `@deepseek-ai/dsh-client-ui-settings-plugin-inventory`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-plugin-inventory`

## 实现逻辑
浏览器半把只读 Host 插件清单注册为 Plugins 设置段的 tab（`settings.plugins.tab` id='all' order 10，src/client/index.ts:56-63）。注入面提供 list()（经 `ctx.remote.pluginInventory.list()`，src/client/index.ts:37-43）、presetName()（经 agent-preset 字典解析内置预设名，src/client/index.ts:46-48）、resolveText 以及 clientSync 快照与重试（src/client/index.ts:49-54）。组件按 agent 预设组与全局平面两组渲染可折叠插件卡片，含搜索、启用状态标签与 Fiber 阶段指示（src/client/PluginInventorySettingsTab.tsx:236-579）。node half 为空 apply（src/index.ts:4）。

## Provides
- settings.pluginInventory locale 命名空间字典
- settings.plugins.tab 槽位条目 id='all' (order 10)：只读 Host 插件清单 tab（预设分组 + 全局平面 + 搜索 + 客户端模块同步状态）

## Depends On (上游依赖)
- `dsh-agent-preset-registry` [编译依赖] - 复用共享的预设显示名折叠逻辑
  - 证据: `src/client/index.ts:12 import { presetDisplayText }`
- `dsh-api-remotes` [E1+E2] - 获取 Host 插件清单快照
  - 证据: `src/client/PluginInventorySettingsTab.tsx:4 import type PluginInventorySnapshot + src/client/index.ts:38 ctx.remote.pluginInventory.list()`
- `dsh-client-locale` [E1+E2] - 注册并绑定本 tab 文案
  - 证据: `src/client/index.ts:3 type-only import + src/client/index.ts:34 ctx.locale.register`
- `dsh-client-modules` [E1+E2] - 读取客户端模块加载状态并触发重试
  - 证据: `src/client/index.ts:4 type-only import + src/client/index.ts:52 ctx.modules.entries.state`
- `dsh-client-ui-agent-preset` [E1+E2] - 借用预设字典解析内置 agent 预设显示名
  - 证据: `src/client/index.ts:10 type-only import + src/client/index.ts:46 ctx.locale.bind('settings.agentPreset')`
- `dsh-client-ui-primitives` [编译依赖] - 复用菜单、状态点与标签原语
  - 证据: `src/client/PluginInventorySettingsTab.tsx:13 import Menu/StateDot/Tag`
- `dsh-client-ui-renderer` [编译依赖] - 引入 ctx.slots 合并
  - 证据: `src/client/index.ts:7 type-only import`
- `dsh-client-ui-settings` [E1+E2] - 复用 Plugins 设置段的 tab 槽声明
  - 证据: `src/client/index.ts:6 type-only import + 经 settings.plugins.tab 槽协作（src/client/index.ts:56）`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
