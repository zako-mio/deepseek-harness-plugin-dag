# dsh-fs-local

- 包名: `@deepseek-ai/dsh-fs-local`
- 分组: G16 文件系统
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/fs/fs-local`

## 实现逻辑
LocalFileSystem 实现 ctx.fs 文件系统 seam：以 realpath 派生的 targetKey 作为目标身份，使别名共享版本守卫 (src/index.ts:133-138)；stat/读/流/列目录委托 fsio 辅助函数 (src/index.ts:157-200)，写与 edit 在 per-target FIFO 锁内完成版本守卫与原子替换，写前捕获有界 diff 基准，edit 走读-匹配-写临界区 (src/index.ts:202-291)。watch() 基于 chokidar 监视单文件或目录的变更 (src/index.ts:69-90)。

## Provides
- ctx.fs (本地宿主文件系统实现，供 fs-sandbox 等替换或包装)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-fs-sandbox` - 继承本地实现以复用原子写与编辑临界区
