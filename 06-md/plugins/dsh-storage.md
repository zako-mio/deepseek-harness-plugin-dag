# dsh-storage

- 包名: `@deepseek-ai/dsh-storage`
- 分组: G40 存储
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/storage/storage`

## 实现逻辑
Storage 服务实现存储中枢 ctx.storage：自身不做 IO，只维护命名后端注册表 BackendRegistry 与可挂载的数据形态表 forms (src/index.ts:47-93)。mount()/form() 以 effect 语义挂载与解析数据形态，domain getter 暴露域形态 (src/index.ts:64-93)。BackendRegistry 支持多后端并存，注册返回 disposer 且带 stale-disposer 保护 (src/registry.ts:25-37)。

## Provides
- ctx.storage (存储中枢：命名后端注册表 + 数据形态挂载与解析)

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-storage-domain` - 作为存储中枢的 domain 数据形态，经后端路由打开域单元
- `dsh-storage-json` - 向存储中枢注册 json 后端并提供 kv facet
- `dsh-storage-sqlite` - 向存储中枢注册 sqlite 后端并提供 kv facet
- `dsh-workspace` - 声明工作区域数据形态所在存储服务 seam 的 peer（源码无直接 import，随 dsh-storage-domain 一起装配）
