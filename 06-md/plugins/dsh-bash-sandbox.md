# dsh-bash-sandbox

- 包名: `@deepseek-ai/dsh-bash-sandbox`
- 分组: G36 Shell 执行
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/shell/bash-sandbox`

## 实现逻辑
继承 LocalBashExecutor，作为 ctx.shell 的沙箱化 bash 执行器：resolve() 为每次调用盖上完整 sandboxPolicy（缺省取 ctx.sandboxPolicy.resolve()）(src/index.ts:45-87)。execute() 对非 danger-full-access 命令调用 ctx.sandbox.confine(['bash','-c',command]) 得到包装 argv 再交回本地执行路径，并按 per-process facts 分类 denial/runner 失败——runner 崩溃抛 SandboxUnavailableError，其余 provider 拒绝保留本地语义 (src/index.ts:89-133, 154-189)。helpers.ts 复用 dsh-sandbox 的签名与 runner 失败分类 (src/helpers.ts:12-14)。

## Provides
- ctx.shell (沙箱约束版 bash 执行器，经 ctx.sandbox.confine 包裹命令后执行并上报 enforcement/denial 事实)

## Depends On (上游依赖)
- `dsh-bash-local` [编译依赖] - 复用本地 bash 的执行生命周期、输出与 deadline 机制
  - 证据: `src/index.ts:25-26 import LocalBashExecutor 及 Config; src/index.ts:45 class extends LocalBashExecutor; package.json:31 peerDep`
- `dsh-sandbox-policy` [运行时依赖] - 读取部署默认沙箱模式并解析每次调用的完整策略
  - 证据: `src/index.ts:24 import type {}; src/index.ts:46 inject ['sandboxPolicy']; src/index.ts:72 ctx.sandboxPolicy.defaultMode`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
