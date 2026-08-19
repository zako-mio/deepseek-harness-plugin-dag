# dsh-client-web-react

- 包名: `@deepseek-ai/dsh-client-web-react`
- 分组: G26 客户端runtime
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/client/web-react`

## 为什么需要它（设计初衷）
Web GUI 浏览器侧的 React 胶水库（createSlotRenderer/SessionProvider/bindSnapshotSelector/useInvoke），供宿主 UI 插件渲染工具卡与交互。

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-client-web-react
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/web-react/README.zh.md

## 实现逻辑
Shell 侧 React 胶水（import 底座，无 cordis 行）。createSlotRenderer：返回 SlotRenderer{renderRoot}——HostContext.Provider+SessionMaybeProvider+RootOutlet；renderer 由 runtime 的 ctx.slots.install 安装（app-shell 行执行）。createSlotRenderer 内部 SlotOutlet 用 useSyncExternalStore 订阅 host.subscribe(key)/getVersion + useLocaleRevision，SlotErrorBoundary 按 entry 隔离崩溃（SlotAssemblyError rethrow，其余走 onEntryError）。bindSnapshotSelector：唯一 hook 构造器——useSyncExternalStoreWithSelector 把裸 observable 源绑成类型化 selector hook（subscribe/getSnapshot 闭包缓存，Object.is 相等）。SessionProvider/SessionMaybeProvider：订阅 host.sessions.provideInfo，key={sessionId} 重建 session 子树，session-maybe 有 adoption 语义。useInvoke：异步动作稳定 trigger+pending（per-hook 外部 store）。

## Provides
- createSlotRenderer（SlotRenderer）
- bindSnapshotSelector（uSES 桥）
- SessionProvider / SessionMaybeProvider
- useInvoke
- SlotErrorBoundary/SlotOwnershipError/StaleAuthorizationError/SlotAssemblyError
- observableHook/maybeObservableHook/projectionHook

## Depends On (上游依赖)
- `dsh-client-locale` [运行时依赖] - t 座位绑定与 locale 切换重渲染
  - 证据: `packages/client/web-react/src/scoped-slots.tsx:227-241（localeSeat 调 face.bind(ns)+getSnapshot().revision）`
- `dsh-client-runtime` [运行时依赖] - renderer 消费 SlotRendererHost 的 sessions/workspaces/locale/store 面（运行时提供）
  - 证据: `packages/client/web-react/src/scoped-slots.tsx:353-355（host.sessions.list / host.workspaces.list 标准 hook）、:417-424（host.storeOf 解 store）、:405-415（host.locale t 座位）`
- `dsh-client-ui-slots` [编译依赖] - slot 契约类型（HostObservable/SlotRendererHost/StoredEntry/LocaleFace）
  - 证据: `packages/client/web-react/src/index.ts:2（import type { SnapshotSelectorHook } from '@deepseek-ai/dsh-client-ui-slots'）；src/scoped-slots.tsx:6-11（import SlotOwnershipError, SlotRendererHost 等）`

## Dependents (下游被依赖)
- `dsh-client-web` - shell 装配渲染器与 uSES 绑定
