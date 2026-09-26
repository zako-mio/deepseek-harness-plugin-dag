# dsh-session-persistence-jsonl

- 包名: `@deepseek-ai/dsh-session-persistence-jsonl`
- 分组: G33 会话核心
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/session/session-persistence-jsonl`

## 实现逻辑
JsonlSessionPersistence 继承 SessionPersistence（注册 ctx.sessionPersistence），以每会话目录下的不可变 generation 文件存 header 与连续事件：create/open 返回带 per-handle 变更链的句柄，读取统一做 fail-closed 校验（src/index.ts:245-577）。写入经 format.ts 编码（默认带校验和的 zstd 帧）、lease.ts 用内核 flock（Windows 具名 semaphore）保证跨进程单写者（src/lease.ts:58-134），storage.ts 负责 live 事件路由与 flush 屏障（src/storage.ts:534-566）。历史 generation 经 format catalog 与 v3→v4 迁移在显式写打开时发布（src/index.ts:579-714），worker 校验由 migration-verifier.ts 承担（src/index.ts:47）。

## Provides
- ctx.sessionPersistence (JSONL 会话持久化后端：不可变 generation 文件、内核写锁与迁移)

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 复用消息组装/流展开与 errorChain 工具
  - 证据: `src/generation.ts:30 import + src/storage.ts:13 import`
- `dsh-session` [编译依赖] - 复用 SESSION_FORMAT_VERSION、SessionId/SessionLogOffset 与 Session 类型
  - 证据: `src/index.ts:36 import + src/lease.ts:36 import + src/catalog-migration.ts:9 import`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
