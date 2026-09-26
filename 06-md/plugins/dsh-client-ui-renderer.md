# dsh-client-ui-renderer

- 包名: `@deepseek-ai/dsh-client-ui-renderer`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 1
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-renderer`

## 实现逻辑
apply 构造 renderer-owned 的 SlotRegistry（在 ui-slots 的纯 SlotCore 语义之上补上活应用所需部分：'slots/changed' 事件桥、按 caller ctx.effect 收集注册/声明、install()/renderSlot('root')、以及 store 实例轴），并 install(createSlotRenderer())（src/client/index.ts:91-95）。随后经 ctx.reflect.provide('uiRenderer') 暴露 mount(container)：mountApp 优先 hydrate 引导期 DOM，否则 createRoot 渲染（src/client/index.ts:70-85），渲染树由 buildRenderApp 从内建 'root' 槽展开（src/client/app.tsx:17-23）。invariant.ts 另订阅 internal/dispatch 并注入 'invariants'，对槽关系做运行时不变式检查（src/invariant.ts:19-46）。

## Provides
- ctx.slots (SlotRegistry：槽注册/声明、'slots/changed' 事件、renderSlot('root')、store 实例轴与 HMR 卸载级联)
- ctx.uiRenderer.mount (把组装好的应用挂载到给定容器的入口)
- 内建 'root' 槽（唯一由 shell 渲染的根洞，其余槽皆其子）
- 'slots/changed' 事件（槽声明或条目集变化时发布）

## Depends On (上游依赖)
- `dsh-invariants` [E1+E2] - 注册渲染器拥有的运行时不变式检查
  - 证据: `src/invariant.ts:12 import + src/invariant.ts:19 inject ['invariants']`

## Dependents (下游被依赖)
- `dsh-client-locale` - 提供 ctx.slots 服务并安装 LocaleFace 供渲染机器合成 t 座位
- `dsh-client-resources` - 类型面激活 ctx.slots 服务合并，参与渲染机器组装
- `dsh-client-ui-agent-preset` - 引入 ctx.slots 服务声明
- `dsh-client-ui-approval` - 引入 slots 服务声明
- `dsh-client-ui-attachment` - 引入并驱动槽位注册服务
- `dsh-client-ui-brand-official` - 引入并驱动槽位注册服务
- `dsh-client-ui-chat` - 引入 slots 服务声明
- `dsh-client-ui-commands` - 引入 slots 服务声明
- `dsh-client-ui-conversation` - 引入 slots 服务声明
- `dsh-client-ui-cordis` - 接入客户端渲染面类型与能力
- `dsh-client-ui-deliverables` - 引入 slots 服务声明
- `dsh-client-ui-directory-picker-browse` - 注册槽位占用
- `dsh-client-ui-directory-picker-native` - 注册槽位占用
- `dsh-client-ui-goal` - 引入 slots 服务声明
- `dsh-client-ui-input-trigger` - 引入 slots 服务声明
- `dsh-client-ui-jobs` - 引入 slots 服务声明
- `dsh-client-ui-layout` - ctx.slots 渲染组合注册表由 ui-renderer 提供，layout 借此注册/查询槽
- `dsh-client-ui-message-feedback` - ctx.slots 槽注册表由 ui-renderer 提供
- `dsh-client-ui-model-selection` - ctx.slots 槽注册表
- `dsh-client-ui-open-in-app` - ctx.slots 槽注册表
- `dsh-client-ui-permission-presets` - ctx.slots 槽注册表
- `dsh-client-ui-plan` - ctx.slots 槽注册表
- `dsh-client-ui-plugin-manager` - ctx.slots 槽注册表
- `dsh-client-ui-schedule` - ctx.slots 槽注册表
- `dsh-client-ui-session` - 引入 ctx.slots 服务声明合并
- `dsh-client-ui-settings-account` - ctx.slots 槽注册表
- `dsh-client-ui-settings-agent-loop` - 引入 ctx.slots 的 SlotRegistry Context 合并
- `dsh-client-ui-settings-general` - 引入 ctx.slots 合并
- `dsh-client-ui-settings-models` - 引入 ctx.slots 合并
- `dsh-client-ui-settings-plugin-inventory` - 引入 ctx.slots 合并
- `dsh-client-ui-settings-plugins` - 引入 ctx.slots 合并
- `dsh-client-ui-settings-shell` - 引入 ctx.slots 合并
- `dsh-client-ui-settings-subagent` - 引入 ctx.slots 合并
- `dsh-client-ui-settings-web-search` - 引入 ctx.slots 合并
- `dsh-client-ui-shortcuts` - 引入 ctx.slots 合并
- `dsh-client-ui-sidebar` - 引入 ctx.slots 合并
- `dsh-client-ui-sidebar-browser` - 引入 ctx.slots 合并
- `dsh-client-ui-sidebar-documentpreview` - 引入 ctx.slots 合并
- `dsh-client-ui-sidebar-files` - 引入 ctx.slots 合并
- `dsh-client-ui-sidebar-right` - 引入 ctx.slots 合并
- `dsh-client-ui-sidebar-terminal` - 拉入 SlotRegistry 服务合并类型
- `dsh-client-ui-skill` - 拉入 SlotRegistry 服务合并类型
- `dsh-client-ui-subagent` - 拉入渲染/槽服务类型合并
- `dsh-client-ui-theme` - 拉入 SlotRegistry 服务合并类型
- `dsh-client-ui-tool` - 拉入槽/渲染服务类型合并
- `dsh-client-ui-trajectory` - 拉入槽/渲染服务类型合并
- `dsh-client-ui-user-questions` - 拉入槽/渲染服务类型合并
- `dsh-client-ui-workflow-run` - 拉入槽/渲染服务类型合并
- `dsh-client-ui-workspace` - 拉入槽/渲染服务类型合并
- `dsh-client-web` - 交接挂载点给 UI 渲染器，随其替换重挂
- `dsh-cordis-client-runner` - 用 slot 注册表承接动态半向 UI 的贡献
- `dsh-experimental-client-ui-agent-team` - 让注册的组件被渲染管线识别
- `dsh-experimental-client-ui-voice-input` - 让注册组件进入渲染管线
- `dsh-session-log-export` - 沿用客户端渲染层的类型环境
