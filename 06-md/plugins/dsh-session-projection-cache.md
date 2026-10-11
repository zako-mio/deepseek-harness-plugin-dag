# dsh-session-projection-cache

- 包名: `@deepseek-ai/dsh-session-projection-cache`
- 分组: G31 会话核心
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/session/session-projection-cache`

## 实现逻辑
把投影单元状态持久化为「每会话一条记录」的 checkpoint 缓存：Service.init 打开 session_projcache 域（per-record 布局、version 7、compatibleVersions [3,4,5,6]、invalidRecords backup-and-skip）并装好写路径 (src/spec.ts:100-107, src/index.ts:117-122)。写侧是 write-behind：会话创建、turn/end、会话销毁三个必写点，外加 writeEveryEvents 计数与 writeIntervalMs 定时两个节流触发；写入前先 flush 会话日志，形成「缓存永不超前于日志」的耐久屏障 (src/index.ts:256-272, src/index.ts:311-362)。读侧提供 cachedSnapshot/cachedPredecessorTitle 的零 I/O 列表视图、hydratePrepared 的就地水合、coldSnapshot 的整日志冷读并 fail-soft 回写 (src/index.ts:161-191, src/index.ts:222-245, src/index.ts:287-306)。记录以 formatVersion/createdAt/cwd/isSeeded/inheritedEventCount 做身份匹配，ver 不匹配的行读取时直接丢弃而非迁移，域层 schema 失败则备份旁置 (src/index.ts:404-469, src/spec.ts:29-58)。

## Provides
- ctx.sessionProjectionCache (投影 checkpoint 的持久缓存服务：列表零 I/O 视图、就地水合、冷读回写)
- session_projcache 域声明 (projectionCacheDomainSpec / checkpointRecord / checkpointIdentity)

## Depends On (上游依赖)
- `dsh-session` [E1+E2] - 以 SessionId/SessionHeader 做身份匹配，并在写缓存前 flush 会话日志
  - 证据: `package.json:36 peerDep + src/index.ts:22 import SessionLogOffset；src/index.ts:266 ctx.sessions.flush(session)`
- `dsh-session-projection` [E1+E2+E3] - 由注册表提供 checkpoint/restore/viewCheckpoint/hydrate 等折叠原语
  - 证据: `package.json:37 peerDep + src/index.ts:33 import type ProjectionCheckpoint；src/index.ts:105 static inject 'sessionProjections'；packages/bundle/base/cordis.patch.yml:167-168 先装注册表、:191-192 后装缓存`
- `dsh-storage-domain` [E1+E2] - 打开 session_projcache 域并持有 per-record 键值表
  - 证据: `package.json:38 peerDep + src/index.ts:34 import type KvTable；src/index.ts:118 ctx.storageDomain.open(projectionCacheDomainSpec)`

## Dependents (下游被依赖)
- `dsh-api-session-controller` - 迁移待完成时返回缓存投影提示
- `dsh-session-reference` - 对冷会话从持久投影缓存回答标题，无需打开其日志
