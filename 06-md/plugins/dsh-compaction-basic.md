# dsh-compaction-basic

- 包名: `@deepseek-ai/dsh-compaction-basic`
- 分组: G21 上下文治理
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/compaction/compaction-basic`

## 实现逻辑
以 BasicCompactionEngine 类(extends CompactionEngine)默认导出，static inject=['llm','tokenMeter','sessions']。auto 时注册 agent/pre-step 压力压缩、agent/request-error 溢出恢复(CONTEXT_WINDOW_EXCEEDED)、agent/status idle 重置。compactIfNeeded 用 ctx.tokenMeter.measure 定价，可选 ctx.get('toolResultPruner') 先裁剪，再 compactSurfaceRegion(append compaction/start|summary|end + user/message surfaceOp replace)；summarize 经 ctx.llm.stream() 复用 KV 前缀缓存。

## Provides
- ctx.compaction 服务
- agent/pre-step 自动压力压缩
- agent/request-error context-overflow 恢复
- compaction/start|summary|end 事件 + surfaceOp replace

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - 订阅 agent/pre-step|request-error|status
  - 证据: `packages/compaction/compaction-basic/src/index.ts:147,179`
- `dsh-compaction-tool-result-pruner` [编译依赖] - 可选 pruneSession(压缩前先裁剪)
  - 证据: `packages/compaction/compaction-basic/src/index.ts:281,309`
- `dsh-llm` [编译依赖] - summarizeWithLlm 经 ctx.llm.stream()
  - 证据: `packages/compaction/compaction-basic/src/summarizer.ts:121-164`
- `dsh-session` [运行时依赖] - 订阅 session/event + append compaction 事件
  - 证据: `packages/compaction/compaction-basic/src/index.ts:173; region.ts:189-215,462-463`
- `dsh-token-meter` [编译依赖] - measure 定价压力/收敛
  - 证据: `packages/compaction/compaction-basic/src/index.ts:104,267`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
