# dsh-storage-json

- 包名: `@deepseek-ai/dsh-storage-json`
- 分组: G40 存储
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/storage/storage-json`

## 实现逻辑
注册存储后端 json：JsonStorageBackend 在配置 root 下按 descriptor.layout 打开 single（整单元单文件）或 per-record（记录级目录）单元 (src/index.ts:64-80)。single 单元以内存为权威，每次写整文件原子重写并在失败时回滚 (src/single-unit.ts:74-112)；per-record 单元不持有内存态、目录即状态，记录键映射为路径段并带版本戳读取 (src/per-record-unit.ts:195-254)。原子发布用同目录临时文件 fsync 后 rename，并对父目录 fsync (src/atomic.ts:24-40)。

## Provides
- storage 后端 `json` (storage.backend.json 生命周期服务与 kv facet)

## Depends On (上游依赖)
- `dsh-storage` [E1+E2] - 向存储中枢注册 json 后端并提供 kv facet
  - 证据: `src/index.ts:12-13 (import StorageError/UNIT_NAME_RE/storageBackendServiceKey 与类型) + src/index.ts:20 (inject ['storage']) + src/index.ts:112 (ctx.storage.backend.register('json'))`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
