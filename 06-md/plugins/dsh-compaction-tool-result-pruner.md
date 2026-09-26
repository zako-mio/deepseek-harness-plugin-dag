# dsh-compaction-tool-result-pruner

- 包名: `@deepseek-ai/dsh-compaction-tool-result-pruner`
- 分组: G07 上下文压缩
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/compaction/compaction-tool-result-pruner`

## 实现逻辑
无模型、可重放的工具结果裁剪服务 ToolResultPruner：按字符预算把超预算的文段替换为 head+marker+tail，按 Unicode 码点切分以免劈开代理对（src/index.ts:83-122、src/index.ts:68-74）。pruneSession 对当前表面的全部 tool/result 节点做一次稳定快照裁剪，并为每个被遮蔽节点先追加一条 compaction/prune 影子价格事件（经 tokenMeter 计价），再追加带 surfaceOp=replace 的替换事件（src/index.ts:136-182）。配置阈值在加载期校验 head+marker+tail ≤ threshold（src/config.ts:36-65）。

## Provides
- ctx.toolResultPruner (确定性工具结果裁剪服务：按字符预算裁剪并写 compaction/prune 影子价格事件)

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 构造不可变的替换工具结果消息并复用其内容块/调用 id 类型
  - 证据: `src/index.ts:9 import freezeMessage + src/index.ts:10 import type ContentBlock + src/types.ts:1 import type ToolCallId`
- `dsh-session` [编译依赖] - 读取当前表面节点并按 surfaceOp 替换/追加会话事件，实现可重放的裁剪事务
  - 证据: `src/index.ts:11 import type Session/SessionEvent/SessionSeq/ToolResultMessage + src/types.ts:2 import type SessionSeq + src/index.ts:160 session.append('compaction/prune')`
- `dsh-token-meter` [E1+E2] - 为每个被遮蔽节点计价以写入影子价格事件，使纯消费者无需保留逐节点状态即可扣减
  - 证据: `src/index.ts:15 type-only import + src/index.ts:47 static inject ['tokenMeter'] + src/index.ts:163 this.ctx.tokenMeter.estimateMessage`

## Dependents (下游被依赖)
- `dsh-compaction-basic` - 可选地先执行无模型工具结果裁剪降低压力，再决定是否摘要；缺少该插件时保持可独立组合
