# dsh-session-projection-cache

- 包名: `@deepseek-ai/dsh-session-projection-cache`
- 分组: G33 会话核心
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/session/session-projection-cache`

## 实现逻辑
SessionProjectionCache（ctx.sessionProjectionCache）在 session_projcache 域持久化每个投影单元的状态检查点：init 打开域并装写回路径（src/index.ts:104-122），在 session/created、turn/end、session/disposed 三个强制点以及计数/间隔节流触发下做 fail-soft 写（src/index.ts:311-375）。读面提供 cachedSnapshot/cachedPredecessorTitle/hydratePrepared/coldSnapshot，只有 (header 生命周期身份 + 继承 cut + 行 ver) 全部匹配才采信缓存行（src/index.ts:136-306）。spec.ts 定义 per-record 布局的域与 (identity, rows) 记录 schema（src/spec.ts:101-108）。

## Provides
- ctx.sessionProjectionCache (投影单元状态的持久化检查点与冷/热读加速)

## Depends On (上游依赖)
- `dsh-session` [E1+E2] - 以会话身份/日志水位作为缓存行匹配依据并做持久化屏障
  - 证据: `src/index.ts:22 import + src/spec.ts:16 import + src/index.ts:266 ctx.sessions.flush`
- `dsh-session-projection` [E1+E2] - 对注册单元做 checkpoint/restore/hydrate 并查看缓存行
  - 证据: `src/index.ts:33 type import + src/index.ts:105 static inject + src/index.ts:204 ctx.sessionProjections.viewCheckpoint`
- `dsh-storage-domain` [E1+E2] - 以域表承载每会话一条检查点记录
  - 证据: `src/index.ts:34 type import + src/spec.ts:18 import + src/index.ts:118 ctx.storageDomain.open`

## Dependents (下游被依赖)
- `dsh-api-session-controller` - 投影缓存类型面
- `dsh-session-reference` - 对冷会话从持久投影缓存回答标题，无需打开其日志
