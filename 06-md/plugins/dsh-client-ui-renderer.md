# dsh-client-ui-renderer

- 包名: `@deepseek-ai/dsh-client-ui-renderer`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 0
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-renderer`

## 实现逻辑
浏览器 UI 渲染器：apply 构造 SlotRegistry、安装 slot 渲染器，并以 ctx.reflect.provide 暴露 ctx.uiRenderer.mount(container) 挂载点 (src/client/index.ts:89-97)。挂载时若容器内已有 [data-dsh-boot] 预置 DOM 则用 hydrateRoot 接管，否则 createRoot + flushSync 渲染，使启动期的无框架加载 DOM 无缝交接给 React (src/client/index.ts:60-83)。应用树整体只渲染内置 root 槽 (src/client/app.tsx:19-21)。SlotRegistry 在纯 SlotCore 之上补上 slots/changed 事件桥、经调用方 ctx.effect 做注册与声明的 fiber 回收、以及 handle×scope 的 store 实例缓存 (src/client/registry.ts:1-11,161)。uSES 桥 bindSnapshotSelector 是全客户端栈唯一的 hook 构造点 (src/client/bind.ts:20-25)。

## Provides
- ctx.uiRenderer (应用挂载面 mount(container)：由无框架的 web 启动内核在客户端插件名册就绪后调用)
- ctx.slots (渲染器自有的 SlotRegistry 组合注册表：slot 声明、注册、渲染与 store 实例生命周期的唯一服务)
- 内置 'root' 槽的渲染契约（shell 自身渲染的唯一顶层槽，其它 seat 由 ui-layout 在其内部声明）

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-client-locale` - 提供 ctx.slots 服务并安装 LocaleFace 供渲染机器合成 t 座位
- `dsh-client-resources` - 类型面激活 ctx.slots 服务合并，参与渲染机器组装
- `dsh-client-ui-agent-preset` - 渲染器槽位服务类型
- `dsh-client-ui-approval` - 引入 slots 服务声明
- `dsh-client-ui-attachment` - 引入并驱动槽位注册服务
- `dsh-client-ui-brand-official` - 引入并驱动槽位注册服务
- `dsh-client-ui-chat` - 渲染器槽位服务类型
- `dsh-client-ui-commands` - 渲染器槽位服务类型
- `dsh-client-ui-conversation` - 渲染器槽位服务类型
- `dsh-client-ui-cordis` - 声明渲染面类型，保证本包插件的客户端渲染接缝类型完整
- `dsh-client-ui-deliverables` - 渲染器槽位服务类型
- `dsh-client-ui-directory-picker-browse` - 注册槽位占用
- `dsh-client-ui-directory-picker-native` - 注册槽位占用
- `dsh-client-ui-goal` - 渲染器槽位服务类型
- `dsh-client-ui-input-trigger` - 引入 slots 服务声明
- `dsh-client-ui-jobs` - 渲染器槽位服务类型
- `dsh-client-ui-layout` - 渲染器槽位服务类型
- `dsh-client-ui-message-feedback` - ctx.slots 槽注册表由 ui-renderer 提供
- `dsh-client-ui-model-selection` - 渲染器槽位服务类型
- `dsh-client-ui-open-in-app` - 渲染器槽位服务类型
- `dsh-client-ui-permission-presets` - 渲染器槽位服务类型
- `dsh-client-ui-plan` - 渲染器槽位服务类型
- `dsh-client-ui-plugin-manager` - 渲染器槽位服务类型
- `dsh-client-ui-schedule` - 拉入 SlotRegistry 服务合并，使 ctx.slots.inject/register 在此编译单元可用
- `dsh-client-ui-session` - 引入 ctx.slots 服务声明合并
- `dsh-client-ui-settings-account` - 拉入 SlotRegistry 服务合并，使槽注册在此编译单元可用
- `dsh-client-ui-settings-agent-loop` - 拉入 SlotRegistry 服务合并，使槽注册与 slots.inject 在此编译单元可用
- `dsh-client-ui-settings-general` - 拉入 SlotRegistry 服务合并，使槽声明与注册在此编译单元可用
- `dsh-client-ui-settings-models` - 拉入 SlotRegistry 服务合并，使槽声明与注册在此编译单元可用
- `dsh-client-ui-settings-plugin-inventory` - 拉入 SlotRegistry 服务合并，使槽注册在此编译单元可用
- `dsh-client-ui-settings-plugins` - 引入 ctx.slots 合并
- `dsh-client-ui-settings-session-log` - 拉入 SlotRegistry 服务合并，使槽注册在此编译单元可用
- `dsh-client-ui-settings-shell` - 拉入 SlotRegistry 服务合并，使槽注册与 slots.inject 在此编译单元可用
- `dsh-client-ui-settings-subagent` - 拉入 SlotRegistry 服务合并，使槽注册与 slots.inject 在此编译单元可用
- `dsh-client-ui-settings-web-search` - 拉入 SlotRegistry 服务合并，使槽注册与 slots.inject 在此编译单元可用
- `dsh-client-ui-shortcuts` - 拉入 SlotRegistry 服务合并，使槽注册在此编译单元可用
- `dsh-client-ui-sidebar` - 拉入 SlotRegistry 服务合并，使槽注册与 entriesOfSlot/subscribe 在此编译单元可用
- `dsh-client-ui-sidebar-browser` - ctx.slots 服务与槽渲染机制来自 renderer
- `dsh-client-ui-sidebar-documentpreview` - ctx.slots 服务与槽渲染由 renderer 提供
- `dsh-client-ui-sidebar-files` - ctx.slots 服务由 renderer 提供
- `dsh-client-ui-sidebar-right` - ctx.slots 服务由 renderer 提供
- `dsh-client-ui-sidebar-terminal` - ctx.slots 服务由 renderer 提供
- `dsh-client-ui-skill` - ctx.slots 服务由 renderer 提供
- `dsh-client-ui-subagent` - ctx.slots 服务由 renderer 提供
- `dsh-client-ui-theme` - ctx.slots 服务由 renderer 提供
- `dsh-client-ui-tool` - ctx.slots 服务由 renderer 提供
- `dsh-client-ui-trajectory` - ctx.slots 服务由 renderer 提供
- `dsh-client-ui-user-questions` - ctx.slots 服务由 renderer 提供
- `dsh-client-ui-workflow-run` - ctx.slots 服务由 renderer 提供
- `dsh-client-ui-workspace` - ctx.slots 服务由 renderer 提供
- `dsh-client-web` - 交接挂载点给 UI 渲染器，随其替换重挂
- `dsh-cordis-client-runner` - 取得 SlotRegistry 类型与渲染面接缝，使动态包注册的 slot 条目挂到调用方 fiber 上
- `dsh-experimental-client-ui-agent-team` - 让注册的组件被渲染管线识别
- `dsh-experimental-client-ui-claude-code-mods` - 槽位渲染由 renderer 承担，类型面需要其声明
- `dsh-experimental-client-ui-cot-translation` - 槽位渲染由 renderer 承担，类型面需要其声明
- `dsh-experimental-client-ui-voice-input` - 槽位渲染由 renderer 承担，类型面需要其声明
- `dsh-experimental-inspector` - 槽位渲染由 renderer 承担，类型面需要其声明
- `dsh-experimental-session-inspector` - 槽位渲染由 renderer 承担，类型面需要其声明
- `dsh-session-log-export` - 沿用客户端渲染层的类型环境
