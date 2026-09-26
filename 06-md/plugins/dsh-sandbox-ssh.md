# dsh-sandbox-ssh

- 包名: `@deepseek-ai/dsh-sandbox-ssh`
- 分组: G39 SSH 远程执行
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/ssh/sandbox-ssh`

## 实现逻辑
SshSandboxProvider 继承 dsh-sandbox 的 SandboxProvider，把 confine() 约束请求经 ctx.ssh.request('sandbox', …) 发往远端主机解析并返回 ConfinedArgv (src/index.ts:10-25)。返回结果会规范化 runnerFailureRules 中的可选字段 (src/index.ts:20-24)，任何失败都包装为 SandboxUnavailableError (src/index.ts:26-29)。

## Provides
- ctx.sandbox (SSH 远程沙箱约束提供者 SshSandboxProvider)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
