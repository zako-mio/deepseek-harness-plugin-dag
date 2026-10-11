# dsh-session-persistence-jsonl

- 包名: `@deepseek-ai/dsh-session-persistence-jsonl`
- 分组: G31 会话核心
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/session/session-persistence-jsonl`

## 实现逻辑
实现 SessionPersistence seam 的 JSONL 后端：以「项目目录/会话目录/不可变世代文件」布局存放 header 行与连续事件，create/open 返回句柄，读取统一走 fail-closed 校验与身份核对 (src/index.ts:1-7, src/index.ts:320-425, src/index.ts:1524-1551)。写入端以临时文件 + fsync + link()（而非 rename，避免并发覆写）原子发布，追加失败按先前长度回滚，torn 尾部先截断再耐久重写恢复出的事件 (src/index.ts:1186-1245, src/index.ts:1334-1384, src/storage.ts:319-343)。跨进程写独占交给内核：POSIX 用 flock(session.lock) 且校验 inode 未换、Windows 用命名信号量，竞争映射为 SessionAlreadyOwnedError (src/lease.ts:70-116)。历史格式世代先 prepare 再由写打开 publish，子会话目录事实经 catalog 收集，当前文件校验隔离在 worker 线程，源身份变化即拒绝 (src/index.ts:631-721, src/catalog-migration.ts:31-92, src/migration-verifier.ts:1-60)。句柄把 live 事件按 200ms 窗口缓冲后经同一变更链落盘，并把 session/event、session/flush、session/disposed 接到路由、刷盘与关闭 (src/storage.ts:36-36, src/storage.ts:274-316, src/storage.ts:534-566)。

## Provides
- ctx.sessionPersistence (JSONL 文件后端实现：世代文件存储、句柄读写、内核写锁与历史格式迁移)
- session_projcache 之外的持久化物理层原语 (zstd 帧容器、torn 尾修复、POSIX/Win32 原子发布)

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 错误链格式化与 assistant 流展开以比对恢复后的行
  - 证据: `package.json:36 dep + src/storage.ts:13 import errorChain；src/generation.ts:30 import BlockAssembler/expandAssistantStream`
- `dsh-session` [E1+E2] - 读写 SessionHeader/SessionEvent 并按会话 id 路由 live 事件
  - 证据: `package.json:31 peerDep + src/index.ts:36-37 import SESSION_FORMAT_VERSION/SessionEvent；src/storage.ts:535 ctx.on('session/event')`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
