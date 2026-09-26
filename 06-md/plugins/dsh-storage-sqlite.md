# dsh-storage-sqlite

- 包名: `@deepseek-ai/dsh-storage-sqlite`
- 分组: G40 存储
- 拓扑层: Layer 1
- 来源层: L3 其余
- 源码路径: `packages/storage/storage-sqlite`

## 实现逻辑
注册存储后端 sqlite：SqliteStorageBackend 独占一个 DatabaseSync 连接，在 units 表强制每单元版本戳，并为 descriptor.tables 建立 u_<unit>_<table> 记录表 (src/index.ts:98-123)。单元原语为单条 prepared statement（upsert/delete/selectAll），原子性由 SQLite 保证，不用显式事务也无写队列 (src/unit.ts:27-118)。打开数据库时创建 owner-only 文件、施加 journal_mode，并把布局版本戳入 PRAGMA user_version，非当前版本拒绝 (src/schema.ts:60-107)。

## Provides
- storage 后端 `sqlite` (storage.backend.sqlite 生命周期服务与 kv facet)

## Depends On (上游依赖)
- `dsh-storage` [E1+E2] - 向存储中枢注册 sqlite 后端并提供 kv facet
  - 证据: `src/index.ts:11-12 (import StorageError/UNIT_NAME_RE/storageBackendServiceKey 与类型) + src/index.ts:21 (inject ['storage']) + src/index.ts:161 (ctx.storage.backend.register('sqlite')) + src/schema.ts:12 (import StorageError)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
