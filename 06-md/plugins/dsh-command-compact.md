# dsh-command-compact

- 包名: `@deepseek-ai/dsh-command-compact`
- 分组: G07 上下文压缩
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/compaction/command-compact`

## 实现逻辑
面向人类的 `/compact` 命令插件：注入 commands 与 compaction 两个 seam，在 apply() 中通过 ctx.commands.register 注册无参数命令，把调用转发给 ctx.compaction.compactNow(agent, signal, commandId)（src/index.ts:101-106、src/index.ts:67）。执行结果按 ManualCompactionError 的封闭错误码（busy/cancelled/changed/summary/commit/persistence）映射为简洁的人类可读文案（src/index.ts:24-56）。使用 ctx.effect 管理生命周期，注册前先 yield 一个 drain 回调等待在途 handler 结算，避免拆卸期新调用进入（src/index.ts:97-107）。

## Provides

## Depends On (上游依赖)
- `dsh-commands` [E1+E2] - 承载 `/compact` 命令的注册面与命令调用/结果类型，命令必须注册进 commands 注册表才能被人类命令适配器看见
  - 证据: `src/index.ts:7 import CommandDefinitionId + src/index.ts:9 import type CommandInvocation/CommandResult + src/index.ts:12 inject 'commands' + src/index.ts:101 ctx.commands.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
