# dsh-subprocess-local

- 包名: `@deepseek-ai/dsh-subprocess-local`
- 分组: G42 子进程
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/subprocess/subprocess-local`

## 实现逻辑
本地子进程能力 seam 的 provider：LocalSubprocessRuntime 继承 SubprocessRuntime（src/index.ts:59-85），按平台选择 linux-scope / windows-job / fallback 三种受管进程范围（src/index.ts:213-232），提供普通进程 spawn（src/spawn.ts:454-492）与 node-pty 终端 spawn（src/index.ts:264-329）。它负责 per-stream stdio 处置、输出 tail-keep 与 spill 文件（src/spawn.ts:267-446）、凭据清洗环境（src/spawn.ts:44-54），并在 JS 可观察的 host 退出时同步终止仍存活的进程范围（src/index.ts:77-105）。

## Provides
- ctx.subprocess（本地实现：受管进程范围 spawn、终端 spawn、可执行文件解析与退出清理）

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-subprocess-ssh` - 复用本地输出收集器实现远程收集快照
