# dsh-client-ui-session

- 包名: `@deepseek-ai/dsh-client-ui-session`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 8
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-session`

## 实现逻辑
作为 Session Controller 与 React 选择器/槽作用域之间的适配层：apply 构造 UiSession，经 ctx.slots.provideRoot 发布根级标准来源 hooks（sessions、sessionStatus）与 keyedHooks.sessionRetainInfo，再 ctx.slots.installScope('session', adapter) 安装会话作用域适配器（src/client/index.ts:670-684）。UiSession 内部实现 useSession/useSessions/useSessionStatus/useSessionRetainInfo 的取值与相等性比较（index.ts:361-380、695-717），并把会话渲染区域绑定到 session-provider.tsx 的 renderSessionArea（index.ts:316）。

## Provides
- 根级标准来源 hooks：useSessions / useSessionStatus / useSessionRetainInfo（含 sessionRetainInfo keyed hook）
- 'session' 槽作用域适配器（ctx.slots.installScope，会话级槽的作用域与标准数据来源）
- 会话渲染区域 renderArea（session-provider.tsx 的 renderSessionArea）
- uiSession.provide()（供域插件发布其会话级 pending-interaction 与状态）

## Depends On (上游依赖)
- `dsh-api-remotes` [编译依赖] - ctx.remote 声明合并
  - 证据: `src/client/index.ts:14 import type {}`
- `dsh-api-session-controller` [E1+E2] - 消费 Session Controller 的列表/绑定/快照与投影接口
  - 证据: `src/client/index.ts:12 import { ISessions, ... } + src/client/index.ts:2-11 import`
- `dsh-client-ui-renderer` [编译依赖] - 引入 ctx.slots 服务声明合并
  - 证据: `src/client/index.ts:29 import type {}`
- `dsh-session` [编译依赖] - 会话身份类型
  - 证据: `src/client/index.ts:13 import type { SessionId }`

## Dependents (下游被依赖)
- `dsh-client-ui-approval` - 发布待决交互供会话 UI 呈现
- `dsh-client-ui-chat` - 向会话 UI 提供 chat hooks 标准位
- `dsh-client-ui-commands` - 会话 UI 声明合并
- `dsh-client-ui-conversation` - 向会话 UI provide 会话/输入 hooks
- `dsh-client-ui-cordis` - 接入会话 UI 集成面
- `dsh-client-ui-goal` - 声明 Session 标准 useProjection 座位
- `dsh-client-ui-input-trigger` - 会话 UI 声明合并
- `dsh-client-ui-jobs` - 会话 UI 声明合并
- `dsh-client-ui-layout` - 引入 ui-session 的声明合并（Session 标准来源类型面）
- `dsh-client-ui-message-feedback` - 引入 ui-session 的 Session 标准来源类型面
- `dsh-client-ui-model-selection` - Session 标准来源类型面
- `dsh-client-ui-open-in-app` - Session 标准来源类型面
- `dsh-client-ui-permission-presets` - Session 标准来源类型面
- `dsh-client-ui-plan` - Session 绑定解析与标准来源
- `dsh-client-ui-schedule` - Session 标准来源类型面
- `dsh-client-ui-settings-general` - 引入会话标准 props 合并（设置外壳在会话上下文渲染）
- `dsh-client-ui-sidebar` - 引入会话标准 props 合并
- `dsh-client-ui-sidebar-browser` - 引入会话标准 props 合并
- `dsh-client-ui-sidebar-documentpreview` - 引入会话标准 props 合并
- `dsh-client-ui-sidebar-files` - 引入会话标准 props 合并
- `dsh-client-ui-sidebar-right` - 引入会话标准 props 合并
- `dsh-client-ui-sidebar-terminal` - 拉入会话 UI 服务的类型合并
- `dsh-client-ui-subagent` - 拉入会话 UI 服务类型合并
- `dsh-client-ui-tool` - 拉入会话 UI 服务类型合并
- `dsh-client-ui-trajectory` - 向会话 UI 提供 trajectory hook
- `dsh-client-ui-user-questions` - 发布待处理问题交互并供 Session UI 消费
- `dsh-client-ui-workflow-run` - 引入会话状态快照与 UI 服务类型
- `dsh-client-ui-workspace` - 拉入会话根标准 hook 类型合并
- `dsh-session-log-export` - 沿用会话视图的类型环境
