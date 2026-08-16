# dsh-session-query-sqlite

- 包名: `@deepseek-ai/dsh-session-query-sqlite`
- 分组: G07 会话持久化
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/session-query/session-query-sqlite`

## 实现逻辑
以 SqliteSessionQueryEngine 类(extends SessionQueryEngine)实现 ctx.sessionQuery 的 SQLite FTS5 后端，static inject=['sessions']。搜索前 _reconcile 做双源观察：live 源折叠 ctx.sessions.list()，持久化源通过可选 ctx.inject(['sessionPersistence']) 的 listSnapshots 对比 revision、inspect 装载变更日志；searchSessions/searchEvents 返回带实例指纹的游标分页。

## Provides
- ctx.sessionQuery 服务
- SQLite FTS5 全文检索索引
- launcherSessionQueryPath 可选槽位

## Depends On (上游依赖)
- `dsh-session` [编译依赖] - static inject sessions; observeLive
  - 证据: `packages/session-query/session-query-sqlite/src/index.ts:197`

## Dependents (下游被依赖)
- `dsh-acp-demo` - ctx.plugin(SqliteSessionQueryEngine) 挂载 SQLite 会话查询索引
- `dsh-tool-session-query` - 宿主装配：session-query-sqlite 提供本工具依赖的 ctx.sessionQuery 服务实现
