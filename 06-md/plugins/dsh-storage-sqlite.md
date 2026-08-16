# dsh-storage-sqlite

- 包名: `@deepseek-ai/dsh-storage-sqlite`
- 分组: G35 会话存储变体
- 拓扑层: Layer 2
- 来源层: L3 其余
- 源码路径: `packages/storage/storage-sqlite`

## 实现逻辑
SQLite 存储后端：SqliteStorageBackend implements StorageBackend，只提供 kv facet（document-per-row: key TEXT PRIMARY KEY / value TEXT NOT NULL, STRICT 表）。apply() 在 storage 中枢 ctx.storage.backend.register('sqlite', backend) 注册 + ctx.provide(storageBackendServiceKey('sqlite')) 暴露后端生命周期服务键，disposer 先 unregister 再 close（inject ['storage']）。openUnit() 校验 UNIT_NAME_RE（unit/table 名）+ 防 double-open（units Map 同步占位）+ units 表 per-unit version 印章校验（不匹配即 StorageError version-mismatch）+ CREATE TABLE IF NOT EXISTS 建记录表。schema.ts 与 session-persistence-sqlite/session-query-sqlite 同构 open 序列（owner-only 建库、PRAGMA foreign_keys/journal_mode=wal、user_version=1 版本印章、零迁移拒绝非当前版本）。close() 幂等关闭所有 unit 并释放连接。config 仅 path（:memory: 支持）+ journalMode。

## Provides
- storage.backend 'sqlite' 后端（kv facet: KvUnit open）
- storageBackendServiceKey('sqlite') 后端生命周期服务键
- per-unit version 印章 + UNIT_NAME_RE 校验 + double-open 防护
- SqliteKvUnit（key/value STRICT 表）

## Depends On (上游依赖)
- `dsh-storage` [运行时依赖] - 存储中枢：后端注册表 + 服务键提供
  - 证据: `packages/storage/storage-sqlite/src/index.ts:11-12 StorageError/UNIT_NAME_RE/storageBackendServiceKey + StorageBackend/KvFacet；21 inject ['storage']；161 ctx.storage.backend.register('sqlite', backend)；167 ctx.provide(storageBackendServiceKey)`
- `dsh-storage-json` [组合依赖] - 后端注册模式参照：与 json 后端并列的 kv facet 后端实现
  - 证据: `storage-sqlite 为 storage-json 同插槽的 SQLite 变体（storage-json/src/index.ts:107 同样 register('json') 模式）`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
