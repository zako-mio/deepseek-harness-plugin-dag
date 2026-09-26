# dsh-session-query-sqlite

- 包名: `@deepseek-ai/dsh-session-query-sqlite`
- 分组: G34 会话检索
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/session-query/session-query-sqlite`

## 实现逻辑
继承抽象 SessionQueryEngine，作为 ctx.sessionQuery 的具体后端：按 openAt 配置在启动或首次检索时打开 SQLite 派生索引（FTS5），并把 live 与 persisted 会话事件索引化 (src/index.ts:203-266, 360-367)。searchSessions/searchEvents 先归一化请求，经 _serialized 串行化、_reconcile 对 live/persisted 语料做稳定观测与增量写入，再用 FTS5 MATCH + highlight() 查询并返回带指纹校验的游标分页 (src/index.ts:268-325, 407-562, 647-708)。query.ts 负责请求归一化、id/cwd/time/type 等谓词编译、FTS 短语转义、snippet 截取与请求指纹 (src/query.ts:100-216, 269-294)。

## Provides
- ctx.sessionQuery (SQLite FTS5 全文检索后端：跨会话/会话内事件检索，继承的精确读与追迹能力)

## Depends On (上游依赖)
- `dsh-session` [E1+E2] - 读取 live 会话（ctx.sessions）并用 SessionHeader/SessionId/SessionSeq 类型构建索引
  - 证据: `src/index.ts:8,12 import; src/index.ts:204 static inject ['sessions']; src/index.ts:503 this.ctx.sessions.list(); package.json:30 peerDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
