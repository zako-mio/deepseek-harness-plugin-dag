# dsh-session-projection-cache

- 包名: `@deepseek-ai/dsh-session-projection-cache`
- 分组: G25 宿主服务
- 拓扑层: Layer 3
- 来源层: L2 web-app
- 源码路径: `packages/session/session-projection-cache`

## 实现逻辑
持久化投影缓存 ctx.sessionProjectionCache：storageDomain 打开 session_projcache 域（sessions 表）；订阅 session/event（turn/end 强制点+count/interval 节流写后置）与 session/disposed（detach 强制点）；冷读阶梯=缓存行→persistence readFrom 尾部→registry restore→fail-soft 写回；写前经 sessions.flush 持久化屏障。

## Provides
- ctx.sessionProjectionCache（SessionProjectionCache 服务）

## Depends On (上游依赖)
- `dsh-session` [编译依赖] - Session/SessionEvent 类型与 snapshotJsonValue
  - 证据: `packages/session/session-projection-cache/package.json:40; src/index.ts:17-18`
- `dsh-session-projection` [编译依赖] - ProjectionCheckpoint/Snapshot 类型
  - 证据: `packages/session/session-projection-cache/package.json:42; src/index.ts:22`
- `dsh-storage-domain` [编译依赖] - KvTable 类型与域表
  - 证据: `packages/session/session-projection-cache/package.json:43; src/index.ts:23`

## Dependents (下游被依赖)
- `dsh-host-apiproxy` - Context merge（ctx.sessionProjectionCache）
