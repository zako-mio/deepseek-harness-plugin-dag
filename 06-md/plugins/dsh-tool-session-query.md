# dsh-tool-session-query

- 包名: `@deepseek-ai/dsh-tool-session-query`
- 分组: G34 会话检索
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/session-query/tool-session-query`

## 实现逻辑
向模型注册五个会话检索工具（session_search/session_event_search/session_trace/session_event_trace/session_event_read），并注入 systemPrompt 章节引导用法 (src/index.ts:56-122)。operations.ts 在 workspace 授权下调用 ctx.sessionQuery 的 searchSessions/searchEvents/traceSession/traceEvent/readEvent，用 collectPages 翻页累积至 maxResults 并对本会话裁剪到当前 step 边界 (src/operations.ts:55-277)。workspace-access.ts 以调用者会话 cwd 为边界做目标授权与可见谱系投影，service-boundary.ts 把服务错误翻译为模型安全的 HarnessError 并记录诊断 (src/workspace-access.ts:75-135, src/service-boundary.ts:99-141)。

## Provides
- 模型工具 session_search/session_event_search/session_trace/session_event_trace/session_event_read (workspace 授权的会话历史检索与读取)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 读取调用者 Agent 会话的 header 与边界投影类型
  - 证据: `src/workspace-access.ts:14 import type { TurnBoundaryProjection }`
- `dsh-llm` [编译依赖] - 用 HarnessError 承载模型安全的错误码与拒绝语义
  - 证据: `src/operations.ts:8 import HarnessError; src/service-boundary.ts:8 import HarnessError; src/workspace-access.ts:9 import HarnessError`
- `dsh-session` [编译依赖] - 用 SessionSeq 品牌化事件序号、用 SessionId 标识目标会话
  - 证据: `src/operations.ts:9-10 import SessionSeq/SessionId`
- `dsh-session-projection` [E1+E2] - 读取调用者会话的 turnBoundary 投影以裁剪本会话检索范围
  - 证据: `src/workspace-access.ts:20 import type {}; src/workspace-access.ts:67 ctx.sessionProjections.stateOf(agent.session, 'turnBoundary')`
- `dsh-system-prompt` [运行时依赖] - 注入会话检索工具的使用引导段落
  - 证据: `src/index.ts:19 inject ['systemPrompt']; src/index.ts:59 ctx.systemPrompt.section`
- `dsh-tools` [E1+E2] - 注册工具定义并消费工具运行上下文
  - 证据: `src/index.ts:10 import; src/index.ts:19 inject ['tools']; src/index.ts:65 ctx.tools.register; src/operations.ts:18 import ToolRunContext`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
