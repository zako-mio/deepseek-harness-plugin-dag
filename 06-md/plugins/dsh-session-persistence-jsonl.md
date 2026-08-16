# dsh-session-persistence-jsonl

- 包名: `@deepseek-ai/dsh-session-persistence-jsonl`
- 分组: G07 会话持久化
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/session/session-persistence-jsonl`

## 实现逻辑
以 JsonlSessionPersistence 类(extends SessionPersistence implements PersistenceBackend)作为默认导出插件，static inject=['sessions']。构造时实例化 PersistenceCoordinator，由协调器安装写路径监听(session/created 捕获 header、session/event 入缓冲、session/flush drain、session/disposed retire)；后端实现 JSONL 追加式日志存储 + zstd 帧压缩 + 崩溃修复(link/unlink 原子发布)。

## Provides
- ctx.sessionPersistence 服务
- PersistenceCoordinator 写路径监听
- JSONL 追加式日志 + zstd + 崩溃修复
- locate/readRaw/listSnapshots

## Depends On (上游依赖)
- `dsh-session` [运行时依赖] - 订阅 session/created|event|flush|disposed 事件源
  - 证据: `packages/session/session-persistence/src/coordinator.ts:1118-1132`

## Dependents (下游被依赖)
- `dsh-acp-demo` - ctx.plugin(JsonlSessionPersistence) 挂载 JSONL 会话持久化
