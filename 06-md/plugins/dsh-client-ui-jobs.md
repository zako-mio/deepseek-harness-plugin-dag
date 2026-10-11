# dsh-client-ui-jobs

- 包名: `@deepseek-ai/dsh-client-ui-jobs`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-jobs`

## 实现逻辑
浏览器半只注册会话头动作：把 JobListAction 挂到 conversation.session.header.actions，注入面从 ctx.jobs 取状态快照、按会话 watchRows/observe，并把 brand 复原后调用 ctx.jobs.kill（src/client/index.ts:33-52）。该插件自身不持有传输状态，任务名册与观察流全部来自 jobs 客户端服务。

## Provides

## Depends On (上游依赖)
- `dsh-api-job-controller` [编译依赖] - 任务控制器服务类型
  - 证据: `src/client/JobListAction.tsx:3 import + src/client/index.ts:11 import type`
- `dsh-client-locale` [E1+E2] - 注册 job 字典
  - 证据: `src/client/index.ts:12 import + src/client/index.ts:34 ctx.locale.register(NS)`
- `dsh-client-ui-conversation` [编译依赖] - 占用 header actions 槽位声明
  - 证据: `src/client/JobListAction.tsx:11 import`
- `dsh-client-ui-renderer` [编译依赖] - 渲染器槽位服务类型
  - 证据: `src/client/index.ts:13 import type`
- `dsh-client-ui-session` [编译依赖] - 会话标准 seat 类型
  - 证据: `src/client/index.ts:14 import type`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/JobListAction.tsx:4 import`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
