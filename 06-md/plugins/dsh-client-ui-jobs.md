# dsh-client-ui-jobs

- 包名: `@deepseek-ai/dsh-client-ui-jobs`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-jobs`

## 实现逻辑
在会话头动作带注册一个后台作业列表入口：apply 注册 job 字典后，用 slots.inject 把 JobListAction 以 order 20 注册进 'conversation.session.header.actions'（排在 preset 标签之后）(src/client/index.ts:33-52)。注入面只经 ctx.jobs（jobs 客户端服务）取 hooks.jobs 与 watchRows/observe/kill，不自行持有传输状态；killJob 在返回前把注册表 id 以 JobId 品牌盖回 (src/client/index.ts:43-50)。宿主半为空 apply，仅作 Loader row (src/index.ts:9)。

## Provides
- slot: conversation.session.header.actions#job-list (order 20 的后台作业列表与流式记录面板)
- Locale 命名空间 job
- 上抛 JobListActionProps/JobListInjected 类型

## Depends On (上游依赖)
- `dsh-api-job-controller` [运行时依赖] - 作业注册表、观察流与 kill 的客户端服务
  - 证据: `src/client/JobListAction.tsx:2 + src/client/index.ts:11 (ctx.jobs 服务来源)`
- `dsh-client-locale` [运行时依赖] - 注册作业字典
  - 证据: `src/client/index.ts:12 + src/client/index.ts:34 ctx.locale.register(NS)`
- `dsh-client-ui-conversation` [运行时依赖] - 依赖 Conversation 声明的会话头动作槽
  - 证据: `src/client/JobListAction.tsx:10 + src/client/index.ts:36 (conversation.session.header.actions 槽声明方)`
- `dsh-client-ui-renderer` [编译依赖] - 引入 slots 服务声明
  - 证据: `src/client/index.ts:13 merge`
- `dsh-client-ui-session` [编译依赖] - 会话 UI 声明合并
  - 证据: `src/client/index.ts:14 merge`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/JobListAction.tsx:3 import SessionId from @deepseek-ai/dsh-session`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
