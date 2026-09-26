# dsh-pwsh-sandbox

- 包名: `@deepseek-ai/dsh-pwsh-sandbox`
- 分组: G36 Shell 执行
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/shell/pwsh-sandbox`

## 实现逻辑
继承 PwshLocalExecutor，作为 ctx.shell 的沙箱化 PowerShell 执行器：resolve() 为每次调用盖上完整 sandboxPolicy (src/index.ts:92-94)。execute() 对受限模式调用 ctx.sandbox.confine(this.argv(spec)) 包装 pwsh argv，并按 confinement facts 分类 denial 与 runner 失败（runner 崩溃抛 SandboxUnavailableError），danger-full-access 直接执行 (src/index.ts:96-140, 161-196)。helpers.ts 镜像 bash-sandbox 的判定方言，含 ENOENT/EACCES 的 runner 归属规则与 fatal/informational 行分类 (src/helpers.ts:42-119)。

## Provides
- ctx.shell (沙箱约束版 PowerShell 执行器，经 ctx.sandbox.confine 包裹 pwsh 调用并上报 enforcement/denial 事实)

## Depends On (上游依赖)
- `dsh-pwsh-local` [编译依赖] - 复用本地 pwsh 的 argv、执行生命周期与输出机制
  - 证据: `src/index.ts:28-29 import PwshLocalExecutor 及 Config; src/index.ts:52 class extends PwshLocalExecutor; package.json:31 peerDep`
- `dsh-sandbox-policy` [运行时依赖] - 读取部署默认沙箱模式并解析每次调用的完整策略
  - 证据: `src/index.ts:27 import type {}; src/index.ts:53 inject ['sandboxPolicy']; src/index.ts:79 ctx.sandboxPolicy.defaultMode`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
