# dsh-experimental-ptc-runtime-python

- 包名: `@deepseek-ai/dsh-experimental-ptc-runtime-python`
- 分组: G13 实验特性
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/experimental/ptc-runtime-python`

## 实现逻辑
`PythonPtcRuntime` 继承 `PtcRuntime` 并注册为 `ctx.ptcRuntime`（language=python，src/index.ts:804-816），以 fresh `python3` 子进程执行模型程序：binding 调用走 fd-3 JSON-lines，stdout/stderr 留给程序自身输出，bootstrap 内提供 asyncio 顶层 await（src/index.ts:1-11）。containment 由 RLIMIT_CPU/RLIMIT_AS、墙钟超时、SIGTERM→grace→SIGKILL 进程组构成，所有上限在 load 时验证（src/index.ts:804-879）；包还拥有并导出 fd-3 wire 协议的编解码与敌意帧校验器，供所有消费方共享词表（src/index.ts:26-39）。

## Provides
- ctx.ptcRuntime (python 子进程隔离的 PTC 运行时后端)
- fd-3 wire 协议编解码/校验器 (validateChildFrame 等)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
