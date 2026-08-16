# dsh-session-persistence-sqlite

- 包名: `@deepseek-ai/dsh-session-persistence-sqlite`
- 分组: G35 会话存储变体
- 拓扑层: Layer 2
- 来源层: L3 其余
- 源码路径: `packages/session/session-persistence-sqlite`

## 实现逻辑
SQLite 持久会话存储后端：SqliteSessionPersistence extends dsh-session-persistence 的 SessionPersistence 抽象类，实现 PersistenceBackend<number>（static inject ['sessions']）。openDb() 异步建目录(0o700)+owner-only 建库文件(0o600)+openDatabase 应用 schema（persistence_state/store_id 单例身份 + sessions 元数据 + events 1:1 行，SCHEMA_VERSION=15，APP_ID=0x44534850，journal_mode=wal 默认）；storeIdentity 由 file:dev:ino:birthtimeNs 或 memory: 复合。写路径全部委托 PersistenceCoordinator（session/created|event|flush|disposed 监听→缓冲/合写/追写），locate() 返回 undefined（无独立 per-session 工件）；create/append/prepare/load/inspect/readFrom 为 coordinator 直通；后端钩子 loadStored/readStoredRevision/loadStoredFrom 实现 seek-capable 后缀读（SQL seq>=fromSeq 直接选取）与 torn-tail 标记（scanRows 返回需删除的 seq）。supportsRawArtifacts=false；与 JSONL 后端同样具备 crash-tail-on-load 语义。

## Provides
- ctx.sessionPersistence 的 SQLite 后端实现（PersistenceBackend<number>）
- 单库 sessions+events 表 + store 身份（store_id/incarnation/revision）
- PersistenceCoordinator 写路径（会话事件合写/追写）
- seek-capable loadStoredFrom + torn-tail 崩溃尾部语义
- SCHEMA_VERSION=15 / journalMode 可配

## Depends On (上游依赖)
- `dsh-session` [编译依赖] - 会话事件/头类型契约与 sessions 服务注入
  - 证据: `packages/session/session-persistence-sqlite/src/index.ts:23 SessionEvent/SurfaceEventType/SessionId/SessionHeader/SessionPreparation 类型；schema.ts:13；static inject ['sessions'](102)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
