# dsh-client-ui-slots

- 包名: `@deepseek-ai/dsh-client-ui-slots`
- 分组: G29 UI底座
- 拓扑层: Layer 0
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-slots`

## 实现逻辑
slot 渲染桥梁/注册表纯核心（零运行时依赖，仅 React 类型）。定义 SlotMap（owners 经 declare module 合并）、LocaleNamespaceMap、SlotKind(single/list/keyed/chain)、SlotScope(root/session-maybe/session)、SlotEntryDef、ChildrenDecl、四份 props share 类型（PropsRuntime/PropsLocale/PropsRenderSlots/PropsStore）与 store 座位（defineStore/BoundActions/HostObservable）。不注册任何 slot/service，是所有 UI 插件 slot 注册的类型与 API 底座。

## Provides
- SlotMap/LocaleNamespaceMap 声明合并面
- SlotRegistry 注册 API（slots.inject/register/subscribe/entries）
- 四份 props share 类型系统 + store 座位类型（defineStore 声明）
- resolveSlotLabel/InjectFace/PropsLocale 等工具类型

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-client-runtime` - SlotCore 纯注册语义/声明账本被 Service 层包装
- `dsh-client-ui-conversation` - SlotRegistry 注册/dispatch 与四份 props 类型底座
- `dsh-client-ui-deliverables` - slot 注册与 props 类型
- `dsh-client-ui-directory-picker-browse` - slot 注册 API
- `dsh-client-ui-directory-picker-native` - slot 注册 API
- `dsh-client-ui-jobs` - props 类型与 slot 注册
- `dsh-client-ui-layout` - slot 注册 API 与 SlotMap 合并面
- `dsh-client-ui-message-feedback` - props 类型与 slot 注册
- `dsh-client-ui-sidebar` - slot 注册与 child 声明
- `dsh-client-ui-tool` - slot 注册 API 与四份 props 类型
- `dsh-client-ui-trajectory` - props 类型与 slot 注册
- `dsh-client-ui-user-questions` - props 类型与 slot 注册
- `dsh-client-ui-workflow-run` - props 类型与 slot 注册 API
- `dsh-client-ui-workspace` - slot 注册与洞占用观察
- `dsh-client-web-react` - slot 契约类型（HostObservable/SlotRendererHost/StoredEntry/LocaleFace）
- `dsh-session-log-export` - inject ['slots','locale']；slots.inject 头部工具槽
