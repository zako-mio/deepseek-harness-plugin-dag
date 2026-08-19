# dsh-subprocess-e2b

- 包名: `@deepseek-ai/dsh-subprocess-e2b`
- 分组: G30 外部执行后端
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/e2b/subprocess-e2b`

## 为什么需要它（设计初衷）
subprocess seam 的 E2B（远程云沙箱）实现：以 Linux 进程组 + base64 帧投影 stdio + PTY 终端会话，让 Bash/PTY/LSP 消费方无需改动即可在共享远程沙箱执行，解决本地执行的安全隔离与主机资源占用问题。

发展史：先加载 dsh-e2b 再替换 dsh-subprocess-local 即完成沙箱切换，是 dsh-subprocess seam 的远程替代后端；当前为 POC 级，仍受 E2B 无信号事实、无 Windows 支持等限制约束。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/e2b/subprocess-e2b/README.zh.md

## 实现逻辑
E2BSubprocessRuntime extends SubprocessRuntime (src/index.ts:52)，static inject ['e2b'] (:53) 注册 ctx.subprocess；spawn 在 ctx.e2b.runtimeRoot/processes 下建 stateDir 生成 E2BSubprocessHandle (:150-151)，spawnTerminal 走 spawnE2BTerminal (:180)，pollMs 控制面轮询 (:69-73)，dispose 统一终止 live handles/terminals (:74-99)，resolveExecutable 经 sandbox.commands.run 解析 PATH (:110-137)。

## Provides
- ctx.subprocess (SubprocessRuntime seam 的 E2B provider)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
