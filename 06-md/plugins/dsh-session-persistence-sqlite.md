# dsh-session-persistence-sqlite

- 包名: `@deepseek-ai/dsh-session-persistence-sqlite`
- 分组: G35 会话存储变体
- 拓扑层: Layer 2
- 来源层: L3 其余
- 源码路径: `packages/session/session-persistence-sqlite`

## 为什么需要它（设计初衷）
SQLite 持久会话后端：SessionEvent 1:1 映射 events 行，事务化 append、延迟实体化、pristine schema 门控、WAL 模式。

发展史：RC8 SQLite 数据结构不兼容(SCHEMA 15→17)，存储格式变更需重建数据库

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/session/session-persistence-sqlite/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/session

## 实现逻辑
物理存储重构为 schema-17: schema.ts:13 SCHEMA_VERSION 15→17; schema.sql:25-26 events.data/source_event_seqs 由 TEXT 改为 ANY(支持BLOB)。codec.ts:44 新增 packChunkRuns 将连续assistant/chunk增量(<1MiB、≤1024条)打包进单行; compression.ts:9,31 用 node:zlib zstd 压缩>4KiB载荷。store.ts:192-193 appendBatch 按打包记录插入，显著降低行数/存储体积。index.ts:41-42 新增 busyTimeoutMs 配置; schema.ts:265 validateSchemaForMutation 每次变更校验表结构。⚠️ 因表 data 列类型与 packed 行变化，与 rc7 数据库不兼容，需重建。

## Provides
- ctx.sessionPersistence 的 SQLite 后端实现（PersistenceBackend<number>）
- 单库 sessions+events 表 + store 身份（store_id/incarnation/revision）
- PersistenceCoordinator 写路径（会话事件合写/追写）
- seek-capable loadStoredFrom + torn-tail 崩溃尾部语义
- SCHEMA_VERSION=15 / journalMode 可配

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 打包StreamChunk类型
  - 证据: `package.json:37 新增llm依赖`
- `dsh-session` [编译依赖] - 会话事件/头类型契约与 sessions 服务注入
  - 证据: `packages/session/session-persistence-sqlite/src/index.ts:23 SessionEvent/SurfaceEventType/SessionId/SessionHeader/SessionPreparation 类型；schema.ts:13；static inject ['sessions'](102)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
