# dsh-spill-local

- 包名: `@deepseek-ai/dsh-spill-local`
- 分组: G38 溢出存储
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/spill/spill-local`

## 实现逻辑
溢出存储 seam 的宿主机实现 LocalSpillStore：把超长文本以随机名加注入式 encodeSegment 路径安全编码写入会话私有目录（根 0700、文件 0600 独占写），返回路径 locator 与 read/grep 检索提示 (src/index.ts:65-162, src/store.ts:55-131)。构造时经 ctx.effect 启动一次尽力而为的启动清理，回收早于 cleanupPeriodDays 的过期文件、剪除空 session 目录与历史默认根，并由 fiber 保证 dispose 前清理收敛 (src/index.ts:95-101, src/cleanup.ts:274-362)。

## Provides
- ctx.spillStore (宿主机文件系统溢出存储实现：会话隔离私有文件写入 + 启动过期清理)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
