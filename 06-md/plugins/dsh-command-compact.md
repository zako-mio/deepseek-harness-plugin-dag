# dsh-command-compact

- 包名: `@deepseek-ai/dsh-command-compact`
- 分组: G10 命令交互
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/compaction/command-compact`

## 为什么需要它（设计初衷）
面向用户的斜杠命令，显式触发会话压缩（compact）。

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-command-compact
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/compaction/command-compact

## 实现逻辑
apply() 用 ctx.effect 管理生命周期：teardown 先 drain 进行中的 handler，再注册 /compact 命令。handler 调 ctx.compaction.compactNow(agent,signal,commandId)，成功返回 shadowedSeqs/shadowedTokenCount；ManualCompactionError 代码映射为人类可读错误。

## Provides
- /compact 命令

## Depends On (上游依赖)
- `dsh-commands` [组合依赖] - /命令注册
  - 证据: `packages/compaction/command-compact/src/index.ts:11,100`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
