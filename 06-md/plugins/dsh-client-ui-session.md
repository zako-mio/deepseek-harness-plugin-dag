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
- `dsh-client-ui-chat` - 把 chat hooks 投影为标准会话 seat
- `dsh-client-ui-commands` - 会话标准 seat 类型
- `dsh-client-ui-conversation` - 提供会话标准 hooks/seat
- `dsh-client-ui-cordis` - 声明会话 UI 面类型，使卡片能落在会话视图上下文
- `dsh-client-ui-goal` - 会话标准 seat 类型
- `dsh-client-ui-input-trigger` - 会话 UI 声明合并
- `dsh-client-ui-jobs` - 会话标准 seat 类型
- `dsh-client-ui-layout` - 会话标准 seat 类型
- `dsh-client-ui-message-feedback` - 引入 ui-session 的 Session 标准来源类型面
- `dsh-client-ui-model-selection` - 会话标准 seat 类型
- `dsh-client-ui-open-in-app` - 会话标准 seat 类型
- `dsh-client-ui-permission-presets` - 会话标准 seat 类型
- `dsh-client-ui-plan` - 会话标准 seat 类型
- `dsh-client-ui-schedule` - 拉入会话根标准 props 合并，供会话头部 seat 的注入签名
- `dsh-client-ui-settings-general` - 拉入会话根标准 props 合并，供 onboarding 协调所需的会话派生事实
- `dsh-client-ui-sidebar` - 拉入会话根标准 props 合并，供侧栏内会话相关 seat 的类型契约
- `dsh-client-ui-sidebar-browser` - 拉入 uiSession 的 Context 合并，标签按 sessionId 作用域渲染
- `dsh-client-ui-sidebar-documentpreview` - 拉入 uiSession 合并，预览按会话作用域
- `dsh-client-ui-sidebar-files` - 拉入 uiSession 合并以按会话渲染
- `dsh-client-ui-sidebar-right` - 跟踪当前屏上会话以切换侧栏呈现
- `dsh-client-ui-sidebar-terminal` - 拉入 uiSession 合并以按会话渲染
- `dsh-client-ui-subagent` - 拉入 uiSession 合并以读取当前会话
- `dsh-client-ui-tool` - 拉入 uiSession/uiConversation 合并以读取会话作用域数据
- `dsh-client-ui-trajectory` - 把 trajectory hook 发布为会话标准 props 的一部分
- `dsh-client-ui-user-questions` - 待答卡片发布到会话级待交互注册表
- `dsh-client-ui-workflow-run` - 拉入 uiSession 合并以按会话渲染面板
- `dsh-client-ui-workspace` - 拉入 uiSession 合并以驱动会话切换
- `dsh-experimental-client-ui-claude-code-mods` - 客户端会话 UI 的声明依赖，保证组合中存在同一份实现
- `dsh-experimental-client-ui-voice-input` - 客户端会话 UI 的声明依赖，保证组合中存在同一份实现
- `dsh-experimental-session-inspector` - 判断当前展示的会话以决定能否把检查器结果揭示到主聊天区
- `dsh-session-log-export` - 沿用会话视图的类型环境
