# dsh-bash-sandbox

- 包名: `@deepseek-ai/dsh-bash-sandbox`
- 分组: G15 沙箱执行
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/shell/bash-sandbox`

## 实现逻辑
沙箱消费型 bash 执行器(SandboxBashExecutor extends LocalBashExecutor,注册 ctx.shell 替代本地执行器):每条命令经 ctx.sandbox.confine(['bash','-c',command], policy) 包裹;resolve() 把 per-call sandboxPolicy 印入 spec;runner 失败抛 SANDBOX_UNAVAILABLE,settlement 按 denialSignatures 分类 denied 并附 enforcement 事实。

## Provides
- ctx.shell 服务(SandboxBashExecutor)
- ctx.shell.sandboxMode 能力事实
- result.sandbox 事实

## Depends On (上游依赖)
- `dsh-sandbox-local` [运行时依赖] - ctx.sandbox.confine
  - 证据: `packages/shell/bash-sandbox/src/index.ts:45,178`
- `dsh-sandbox-policy` [运行时依赖] - 默认模式事实
  - 证据: `packages/shell/bash-sandbox/src/index.ts:45,71`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
