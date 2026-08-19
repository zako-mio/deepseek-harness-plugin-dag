# dsh-storage-domain

- 包名: `@deepseek-ai/dsh-storage-domain`
- 分组: G25 宿主服务
- 拓扑层: Layer 2
- 来源层: L2 web-app
- 源码路径: `packages/storage/storage-domain`

## 为什么需要它（设计初衷）
存储中心的领域数据形态：在配置的后端上提供 schema 校验、事件发射的 KV 领域（ctx.storageDomain / ctx.storage.domain 投影）。领域以 defineDomain + zod 记录 schema 声明，内存为权威、读同步、写按领域串行化，先落盘后更新内存并发射 domain/changed。用于存放非会话数据（workspace 记录、未来会话 sidecar）。

发展史：由 2026-07-24 domain-kv-storage Agent Note 定案（storage/domain 分层）；2026-08-10 发布 0.0.1-rc.1，补足会话日志之外的结构化存储形态。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/storage/storage-domain/README.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/proposed/architecture/2026-07-24-domain-kv-storage-and-workspace.zh.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-storage-domain

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
