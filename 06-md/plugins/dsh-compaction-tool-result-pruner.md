# dsh-compaction-tool-result-pruner

- 包名: `@deepseek-ai/dsh-compaction-tool-result-pruner`
- 分组: G21 上下文治理
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/compaction/compaction-tool-result-pruner`

## 为什么需要它（设计初衷）
回放安全、无模型的 head/middle/tail 修剪器，用于压缩工具结果表层节点。

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-compaction-tool-result-pruner
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/compaction/compaction-tool-result-pruner

## 实现逻辑
以 ToolResultPruner 类(extends Service，super(ctx,'toolResultPruner'))默认导出，static inject=['tokenMeter']。pruneSession 遍历 session.surface.nodes 中 tool/result 事件，pruneContent 按 Unicode 码点做 head/middle/tail 截断；超预算的替换先 append 'compaction/prune' 影子定价事件，再 append 同内容裁剪版 'tool/result' 事件并带 surfaceOp:{op:'replace'} 落盘。

## Provides
- ctx.toolResultPruner 服务
- pruneSession 模型无关裁剪
- compaction/prune 影子定价协议
- surfaceOp replace 重写

## Depends On (上游依赖)
- `dsh-llm` [组合依赖] - freezeMessage
  - 证据: `packages/compaction/compaction-tool-result-pruner/src/index.ts:9`
- `dsh-session` [编译依赖] - 读 surface.nodes + append 替换
  - 证据: `packages/compaction/compaction-tool-result-pruner/src/index.ts:138-171`
- `dsh-token-meter` [编译依赖] - estimateMessage 计算 shadowedTokenCount
  - 证据: `packages/compaction/compaction-tool-result-pruner/src/index.ts:47,165`

## Dependents (下游被依赖)
- `dsh-compaction-basic` - 可选 pruneSession(压缩前先裁剪)
