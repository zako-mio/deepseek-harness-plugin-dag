# dsh-subprocess-ssh

- 包名: `@deepseek-ai/dsh-subprocess-ssh`
- 分组: G39 SSH 远程执行
- 拓扑层: Layer 1
- 来源层: L3 其余
- 源码路径: `packages/ssh/subprocess-ssh`

## 实现逻辑
SshSubprocessRuntime 继承 dsh-subprocess 的 SubprocessRuntime，经 ctx.ssh 在远端主机管理普通进程与 PTY（resolveExecutable/terminalEnvironment/spawn/spawnTerminal）(src/index.ts:229-343)。RemoteProcess 用独立 SSH 流复用本地 OutputCollector 处理 stdout/stderr 的收集、快照与背压，并通过 process.prepare/start/done/terminate 协议驱动远端进程生命周期 (src/index.ts:21-226)。构造函数内注册 ctx.effect 清理器，在插件销毁时终止所有存活进程与终端 (src/index.ts:236-253)。

## Provides
- ctx.subprocess (SSH 远程子进程与 PTY 提供者 SshSubprocessRuntime)

## Depends On (上游依赖)
- `dsh-subprocess-local` [编译依赖] - 复用本地输出收集器实现远程收集快照
  - 证据: `src/index.ts:7 (import OutputCollector from '@deepseek-ai/dsh-subprocess-local/output')`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
