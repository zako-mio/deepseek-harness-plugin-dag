# dsh-experimental-ptc-runtime-python

- 包名: `@deepseek-ai/dsh-experimental-ptc-runtime-python`
- 分组: G13 实验特性
- 拓扑层: Layer 4
- 来源层: L3 其余
- 源码路径: `packages/experimental/ptc-runtime-python`

## 实现逻辑
PtcRuntime 的 Python 后端：每次运行起一个全新 python3 子进程，用 fd 3 上的 JSON-lines 帧承载绑定调用，把 stdout/stderr 留给程序自身输出，并以 RLIMIT_CPU/RLIMIT_AS、墙钟上限与输出预算约束单次运行 (src/index.ts:1-11, src/index.ts:744-771)。所有上限都是经 schemastery 校验的 Config，加载期即拒绝不可满足的组合（浮点 cpuSeconds、超 MAX_TIMER_DELAY_MS 的墙钟、超过 fd-3 帧解析上限的字节预算、非 CPython 3.10+ 的解释器等）(src/index.ts:746-754, src/index.ts:788-896, src/index.ts:447-480)。沙箱模式取 ctx.sandboxPolicy.defaultMode，实际限制经 ctx.sandbox.confine 施加；run() 要求已解析的 sandbox 策略 (src/index.ts:759, src/index.ts:982-1030)。包同时拥有无版本号的 fd-3 线协议本身，并把编解码与恶意帧校验再导出，供所有消费方共用一套词汇 (src/index.ts:32-42, src/protocol.ts)。

## Provides
- ctx.ptcRuntime 的 Python 后端 (PtcRuntime 实现：CPython 子进程、fd-3 绑定协议、rlimit 与超时预算、进程组回收)
- fd-3 线协议编解码与校验再导出 (checkDoneValue/encodeJsonPlain/validateChildFrame 等)
- hostFrameParseCeiling / resolvePythonBin / readProcessStart 等宿主侧可测工具函数

## Depends On (上游依赖)
- `dsh-sandbox-policy` [E1+E2] - 运行时默认沙箱模式与每次运行的策略解析都来自该 seam
  - 证据: `src/index.ts:27 import type {} from '@deepseek-ai/dsh-sandbox-policy' + src/index.ts:745 static inject = ['sandbox', 'sandboxPolicy'] + src/index.ts:759 this.ctx.sandboxPolicy.defaultMode + src/index.ts:982 this.ctx.sandboxPolicy.resolve() + package.json:32 peerDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
