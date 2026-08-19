# dsh-client-ui-slots

- 包名: `@deepseek-ai/dsh-client-ui-slots`
- 分组: G29 UI底座
- 拓扑层: Layer 0
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-slots`

## 为什么需要它（设计初衷）
Web shell 插槽系统的纯核心：声明合并的 SlotMap、单次 register 组合 API、四共享 props 类型族与 store-seat 类型族。一次 register 调用即完成组件进槽、子槽声明（声明=渲染授权=运行时规格）、store 座位与业务面注册；React-free 且 cordis-free，register 时校验未声明槽/重复声明/跨作用域共享等错误。

发展史：2026-08-10 以 0.0.1-rc.1 随 dsh 第一批客户端包发布；为浏览器 UI 插件体系提供类型安全插槽注册与 renderer 安装契约，实现在 web-react 与 shell boot。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-slots/README.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-client-ui-slots

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
- `dsh-client-ui-jobs` - props 类型与 slot 注册
- `dsh-client-ui-layout` - slot 注册 API 与 SlotMap 合并面
- `dsh-client-ui-message-feedback` - props 类型与 slot 注册
- `dsh-client-ui-renderer` - 声明式slot渲染与快照选择器基座
- `dsh-client-ui-sidebar` - slot 注册与 child 声明
- `dsh-client-ui-tool` - slot 注册 API 与四份 props 类型
- `dsh-client-ui-trajectory` - props 类型与 slot 注册
- `dsh-client-ui-user-questions` - props 类型与 slot 注册
- `dsh-client-ui-workflow-run` - props 类型与 slot 注册 API
- `dsh-client-ui-workspace` - slot 注册与洞占用观察
- `dsh-session-log-export` - inject ['slots','locale']；slots.inject 头部工具槽
