# dsh-fs-e2b

- 包名: `@deepseek-ai/dsh-fs-e2b`
- 分组: G30 外部执行后端
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/e2b/fs-e2b`

## 实现逻辑
E2BFileSystem extends FileSystem seam (src/index.ts:171), static inject ['e2b'] (:172) pulls ctx.e2b sandbox; 所有 fs 操作(resolve/read/write/edit/list/stat) 经 sandbox.files/sandbox.commands 执行，canonicalPath 用 realpath+base64 传输 (:443-454)，写入走 staging 目录+原子 rename/guarded ln 发布 (:510-579)，per-targetKey 锁 (:431-441)，版本用 entry 事实 sha256 (:122-133)，含 CRLF/二进制检测。

## Provides
- ctx.fs (FileSystem seam 的 E2B 远程后端，E2BFileSystem extends FileSystem)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
