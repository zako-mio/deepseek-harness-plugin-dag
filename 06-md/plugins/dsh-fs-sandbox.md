# dsh-fs-sandbox

- 包名: `@deepseek-ai/dsh-fs-sandbox`
- 分组: G13 文件系统
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/fs/fs-sandbox`

## 实现逻辑
以 SandboxedFileSystem 类(继承 LocalFileSystem)提供沙箱强制的 ctx.fs 后端:对 writeText/editText 两个变更操作做 per-call 策略围栏(checkedTarget)——read-only 拒绝所有变更,workspace-write 重新 canonicalize 后以 isPathUnder 判定目标位于 writableRoots 内并返回新鲜 target 防 TOCTOU,danger-full-access 放行;拒绝抛 FS_SANDBOX_DENIED。读取不设防。

## Provides
- ctx.fs 服务(SandboxedFileSystem,替代 dsh-fs-local)
- ctx.fs.sandboxMode 能力事实
- fs-sandbox-invariant 伴生插件

## Depends On (上游依赖)
- `dsh-sandbox-policy` [运行时依赖] - static inject sandboxPolicy;默认模式取自 defaultMode
  - 证据: `packages/fs/fs-sandbox/src/index.ts:60,127,65`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
