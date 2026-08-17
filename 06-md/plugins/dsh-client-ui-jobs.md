# dsh-client-ui-jobs

- 包名: `@deepseek-ai/dsh-client-ui-jobs`
- 分组: G27 会话交互UI
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-jobs`

## 为什么需要它（设计初衷）
会话头后台任务列表：从 session/jobs 帧镜像实时注册表状态，展示后台 job 进度。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-jobs/package.json

## 实现逻辑
session-header 后台作业列表。JobListAction 注册进 conversation.session.header.actions（id=job-list, order=20 位于 subagent catalog 之后）；数据完全来自 sessions list 镜像的 jobsBySession（useSessions(state => state.jobsBySession[sessionId])），不发任何 RPC、不持自身状态（仅 popover 可见性）；按 live/settled 排序渲染状态点（running/stopping/completed/killed/failed）+ 时长。

## Provides
- conversation.session.header.actions id=job-list(JobListAction)

## Depends On (上游依赖)
- `dsh-client-locale` [编译依赖] - job 命名空间字典
  - 证据: `index.ts:9 type-only + index.ts:29 locale.register`
- `dsh-client-runtime` [运行时依赖] - jobsBySession 列表镜像（dsh-jobs 注册的会话数据）
  - 证据: `index.ts:7 ClientContext + JobListAction.tsx:95 useSessions(state => state.jobsBySession[sessionId]) + JobListAction.tsx:2 JobView`
- `dsh-client-ui-conversation` [编译依赖] - 消费 header actions 座位声明
  - 证据: `index.ts:30-39 注册 conversation.session.header.actions + JobListAction.tsx:6 type-only + package.json:54 peerDependencies`
- `dsh-client-ui-primitives` [编译依赖] - 状态点/图标 atoms
  - 证据: `JobListAction.tsx:3 StateDot,IconChevronDownOutline14`
- `dsh-client-ui-slots` [编译依赖] - props 类型与 slot 注册
  - 证据: `JobListAction.tsx:4 PropsLocale/PropsRuntime/TranslateNS`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
