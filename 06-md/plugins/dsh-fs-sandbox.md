# dsh-fs-sandbox

- 包名: `@deepseek-ai/dsh-fs-sandbox`
- 分组: G16 文件系统
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/fs/fs-sandbox`

## 实现逻辑
SandboxedFileSystem 继承 LocalFileSystem，复用其全部文本存储机制，只在两个变更入口加每调用策略围栏：writeText/editText 先经 checkedTarget (src/index.ts:80-109)。checkedTarget 按策略 mode 判定：read-only 抛 FS_SANDBOX_DENIED，workspace-write 立即用 resolve 重规范化路径并要求落在 writableRoots 内（返回该新目标以避免 check-here-write-there），danger-full-access 原样放行 (src/index.ts:122-144)；读操作完全透传。

## Provides
- ctx.fs (沙箱约束版文件系统实现，加载时替换 fs-local)

## Depends On (上游依赖)
- `dsh-fs-local` [E1+E2] - 继承本地实现以复用原子写与编辑临界区
  - 证据: `src/index.ts:30 LocalFileSystem import + src/index.ts:55 extends LocalFileSystem`
- `dsh-sandbox-policy` [E1+E2] - 解析每调用会话的沙箱模式与工作区根
  - 证据: `src/index.ts:56 inject ['sandboxPolicy'] + src/index.ts:36 import`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
