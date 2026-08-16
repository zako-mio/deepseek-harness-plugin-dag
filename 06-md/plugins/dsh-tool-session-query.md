# dsh-tool-session-query

- 包名: `@deepseek-ai/dsh-tool-session-query`
- 分组: G35 会话存储变体
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/session-query/tool-session-query`

## 实现逻辑
模型面向、工作区授权的会话历史搜索/读取工具：apply() 注册 5 个工具到 ctx.tools + 一个 systemPrompt section（order 113，'tool:session-query' 指南，inject ['tools','systemPrompt','sessionQuery']）。工具：session_search（跨会话最强匹配事件）、session_event_search（单会话事件搜索）、session_trace（会话血统/祖先后代）、session_event_trace（事件血统）、session_event_read（未删节事件+相邻 raw 摘要），均 TEXT_OUTPUT 渲染。operations.ts：executeSessionSearch 先 workspaceAccess.callerOf 取调用者 cwd（无 cwd 即 SESSION_QUERY_TOOL_UNAUTHORIZED），authorizeSessionIds 授权父会话/命中会话，经 serviceBoundary.call 包装后调 ctx.sessionQuery.searchSessions/searchEvents/traceSession/traceEvent/readEvent（cursor 分页 collectPages，maxSearchResults=100 默认封顶，searchTimeoutMs=30s 协作超时）；workspace 作用域（cwd filter）强制注入。isConcurrencySafe 标记只读工具。

## Provides
- ctx.tools 注册 5 个工具：session_search/session_event_search/session_trace/session_event_trace/session_event_read
- ctx.systemPrompt section 'tool:session-query'（order 113 使用指南）
- 工作区授权（cwd 作用域 + authorizeSessionIds）与 cursor 分页 collectPages
- TEXT_OUTPUT 文本渲染（presentation.formatSessionSearch 等）

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - HarnessError 错误契约（工作区未授权报错）
  - 证据: `packages/session-query/tool-session-query/src/operations.ts:8 HarnessError（SESSION_QUERY_TOOL_UNAUTHORIZED）`
- `dsh-session` [编译依赖] - SessionId branded 类型与会话头（cwd）
  - 证据: `packages/session-query/tool-session-query/src/operations.ts:9 SessionId 类型；package.json:36`
- `dsh-session-query-sqlite` [组合依赖] - 宿主装配：session-query-sqlite 提供本工具依赖的 ctx.sessionQuery 服务实现
  - 证据: `package.json devDependencies:55 dsh-session-query-sqlite（集成宿主）＋ base/cordis.patch.yml:117-118 装配 session-query-sqlite 提供 ctx.sessionQuery`
- `dsh-system-prompt` [运行时依赖] - 系统提示 section 注册：模型面向的工具使用指南
  - 证据: `packages/session-query/tool-session-query/src/index.ts:20 inject ['systemPrompt']；60-64 ctx.systemPrompt.section({name:'tool:session-query', order:113})；package.json:39`
- `dsh-tools` [运行时依赖] - 工具注册表：defineTool 契约与注册
  - 证据: `packages/session-query/tool-session-query/src/index.ts:20 inject ['tools']；66-122 ctx.tools.register(defineTool(...))；package.json:41`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
