# dsh-client-runtime

- 包名: `@deepseek-ai/dsh-client-runtime`
- 分组: G26 客户端runtime
- 拓扑层: Layer 9
- 来源层: L2 web-app
- 源码路径: `packages/client/runtime`

## 实现逻辑
客户端核心服务层（纯 browser，host apply 空）。SlotRegistry：cordis Service 包装 SlotCore——'slots/changed' 事件桥、register 经 ctx.effect 绑定 caller fiber、install()/renderSlot('root')/installLocale() boot-once、store-instance 轴（handle×scope→实例，session 实例随 scope death 清理）、hostFace 聚合 sessions/workspaces/locale。SessionRuntime：list snapshot store（manager 投影，current 持久化）、Agent scope 树（createScope：no-op fiber+ctx.extend tag，agent id===session id，lazy mint+stage-driven teardown）、SessionBinding 缓存、SessionProvideChannel。WorkspaceRuntime：workspace list + 双 baseline + 初始 selection。apply 启动 connection.start 双流，分发 mux/host 帧到 sessions/workspaces，host/remote-event 帧转 ctx.remote.$dispatch。

## Provides
- ctx.slots（SlotRegistry）
- ctx.sessions（ISessions/SessionRuntime）
- ctx.workspaces（IWorkspaces/WorkspaceRuntime）
- ctx.conversationEvents / ctx.conversationViews
- 事件：slots/changed、connection/reset
- TypertContext agent（registerClient）
- SessionStandardProps/GlobalStandardProps 类型合并（ui-slots）
- createSnapshotStore/defineStore/shallowEqual

## Depends On (上游依赖)
- `dsh-api-remotes` [编译依赖] - 类型面（remote 合并）
  - 证据: `packages/client/runtime/src/client/index.ts:7（import type {} from '@deepseek-ai/dsh-api-remotes/client'）；package.json peerDependencies @deepseek-ai/dsh-api-remotes`
- `dsh-client-connection` [编译依赖] - inject 顺序：connection 先于 runtime 激活
  - 证据: `packages/client/runtime/src/client/index.ts:3（import type { ConnectionHandle } from '@deepseek-ai/dsh-api-remotes/client'；dsh.client.inject 含 @deepseek-ai/dsh-client-connection）`
- `dsh-client-ui-slots` [编译依赖] - SlotCore 纯注册语义/声明账本被 Service 层包装
  - 证据: `packages/client/runtime/src/client/slots.ts:19（import { SlotCore } from '@deepseek-ai/dsh-client-ui-slots'）`
- `dsh-host-apiproxy` [编译依赖] - wire 层常量（search 结果上限）
  - 证据: `packages/client/runtime/src/client/sessions/service.ts:23（import { SESSION_SEARCH_RESULT_LIMIT } from '@deepseek-ai/dsh-host-apiproxy/api'）`
- `dsh-session-projection` [编译依赖] - projection 值类型（projectionValues）
  - 证据: `packages/client/runtime/src/client/sessions/service.ts:27（import type { SessionProjectionMap } from '@deepseek-ai/dsh-session-projection/types'）；package.json dependencies`
- `dsh-typert-registry` [运行时依赖] - 注册 client Agent scope identity
  - 证据: `packages/client/runtime/src/client/index.ts:183（inject ['typert']）、:196（ctx.typert.contexts.registerClient('agent',…)）`

## Dependents (下游被依赖)
- `dsh-client-locale` - ClientContext/类型与 slots 服务
- `dsh-client-ui-conversation` - SessionRuntime 会话/工作区服务、EventDefinition+View 注册表、useProjection/defineStore 运行时
- `dsh-client-ui-cordis` - 客户端运行时与会话上下文
- `dsh-client-ui-deliverables` - EventDefinition 注册表与事件匹配
- `dsh-client-ui-directory-picker-browse` - host 目录列示/创建原语（dsh-host-directory-picker-browse node 半）
- `dsh-client-ui-directory-picker-native` - host 原生目录选择原语（dsh-host-directory-picker-native node 半）
- `dsh-client-ui-goal` - 会话绑定与投影 face
- `dsh-client-ui-input-trigger` - client 运行时上下文与会话面
- `dsh-client-ui-jobs` - jobsBySession 列表镜像（dsh-jobs 注册的会话数据）
- `dsh-client-ui-layout` - runtime 内建 'root' slot 与 reflect.provide 服务发布面
- `dsh-client-ui-message-feedback` - 会话上下文与对象层挂载
- `dsh-client-ui-settings` - SnapshotStore/uSES 状态基建
- `dsh-client-ui-sidebar` - 新会话创建与工作区服务
- `dsh-client-ui-theme` - ClientContext/slots 服务
- `dsh-client-ui-tool` - 会话快照/ToolCallBlock 类型与运行时
- `dsh-client-ui-trajectory` - EventDefinition/View 注册表与会话分页
- `dsh-client-ui-user-questions` - PendingWait 载体（question 等待帧）
- `dsh-client-ui-workflow-run` - EventDefinition/View 注册表与会话快照类型
- `dsh-client-ui-workspace` - 会话列表/搜索/分叉与工作区 CRUD 服务
- `dsh-client-web` - SlotMap 'root' 声明合并（类型面）
- `dsh-client-web-react` - renderer 消费 SlotRendererHost 的 sessions/workspaces/locale/store 面（运行时提供）
- `dsh-cordis-client-runner` - slots 服务与类型
