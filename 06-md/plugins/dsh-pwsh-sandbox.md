# dsh-pwsh-sandbox

- 包名: `@deepseek-ai/dsh-pwsh-sandbox`
- 分组: G15 沙箱执行
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/shell/pwsh-sandbox`

## 实现逻辑
bash-sandbox 的 pwsh 对偶(SandboxPwshExecutor extends PwshLocalExecutor,注册 ctx.shell):confine(spec, policy) 用 ctx.sandbox.confine 包裹完整 pwsh argv(Windows 上 ACL 受限令牌 runner 链);resolve() 印入 per-call policy,runner 失败分类与 denial 签名匹配。

## Provides
- ctx.shell 服务(SandboxPwshExecutor)
- ctx.shell.sandboxMode 能力事实
- result.sandbox 事实

## Depends On (上游依赖)
- `dsh-sandbox-local` [运行时依赖] - ctx.sandbox.confine
  - 证据: `packages/shell/pwsh-sandbox/src/index.ts:53,184`
- `dsh-sandbox-policy` [运行时依赖] - 默认模式事实
  - 证据: `packages/shell/pwsh-sandbox/src/index.ts:53,79`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
