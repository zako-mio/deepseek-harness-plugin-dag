# dsh-storage-domain

- 包名: `@deepseek-ai/dsh-storage-domain`
- 分组: G25 宿主服务
- 拓扑层: Layer 2
- 来源层: L2 web-app
- 源码路径: `packages/storage/storage-domain`

## 实现逻辑
领域数据形式：apply 对声明的后端服务键 ctx.inject 等待，随后在 storage 中枢 ctx.storage.mount('domain') 挂 DomainFacility 并 provide ctx.storageDomain；open() 按 routes/backend 经 hub 路由到后端 kv、zod 校验加载记录、经 DomainImpl 发 domain/changed 变更事件。

## Provides
- ctx.storageDomain（DomainFacility）
- ctx.storage.domain 数据形式
- domain/changed 事件

## Depends On (上游依赖)
- `dsh-storage` [编译依赖] - storageBackendServiceKey 与 StorageForms 声明合并
  - 证据: `packages/storage/storage-domain/package.json:36-38; src/index.ts:12`
- `dsh-storage-json` [组合依赖] - config backend: json → 经 hub 解析 'json' 后端（E2 解析）
  - 证据: `packages/bundle/web-app/cordis.patch.yml:59-62; packages/storage/storage-domain/src/index.ts:106-107`

## Dependents (下游被依赖)
- `dsh-message-feedback` - KvTable 类型与域表读写
- `dsh-session-projection-cache` - KvTable 类型与域表
- `dsh-workspace` - DomainGlobal/KvTable 类型与域读写
