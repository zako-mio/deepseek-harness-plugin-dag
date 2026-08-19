# dsh-session-query-sqlite

- 包名: `@deepseek-ai/dsh-session-query-sqlite`
- 分组: G07 会话持久化
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/session-query/session-query-sqlite`

## 为什么需要它（设计初衷）
解决会话历史检索缺少高性能全文搜索的问题：作为 ctx.sessionQuery 的 SQLite 具体提供方，用 FTS5(unicode61) 实现 searchSessions/searchEvents 两个全文方法，支持跨会话/会话内分页、元数据过滤与实时+持久化双层语料库对账。其核心价值是为插件与工具提供不加载完整日志的可检索会话历史，并严格规避注入（FTS5 语法当数据、参数化谓词、谓词预算）。

发展史：承接 2026-07-10 session-query-service 与 2026-07-23 unified-session-query-service 两次架构统一后，成为首个/默认的具体后端（packages/session-query/session-query-sqlite），与抽象服务 session-query 分离，采用「继承精确读取+自有全文实现」的分层结构。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/session-query/session-query-sqlite/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/implemented/feature/2026-07-10-sqlite-session-query-provider.md

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
