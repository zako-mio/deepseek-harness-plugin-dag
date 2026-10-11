# dsh-storage-domain

- 包名: `@deepseek-ai/dsh-storage-domain`
- 分组: G38 存储
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/storage/storage-domain`

## 实现逻辑
在存储 hub 之上实现「域」数据形态：apply 收集配置中出现的后端服务键并 `ctx.inject` 等待，然后 `ctx.storage.mount('domain', facility)` 并 `provide('storageDomain', …)`，卸载时先 closeAll 再 unmount (src/index.ts:217-236)。DomainFacility.open 逐级失败：拒绝重名（already-open）、按 routes/backend 路由后端、要求 kv facet、以 `descriptorOf(spec)` 打开单元、用 zod schema 校验每条已存记录（可选 backup-and-skip），最后构造域 (src/index.ts:103-174、src/spec.ts:154-163)。DomainImpl 维护权威内存态与单条写链：每次写先等后端持久化成功、再改内存、再 emit `domain/changed`，因此写失败不会造成内存与介质分叉 (src/domain.ts:307-346、src/domain.ts:263-270)。

## Provides
- ctx.storageDomain（DomainFacility：按配置路由后端、打开/查询/批量关闭域）
- ctx.storage 的 `domain` 数据形态（schema 校验的 KV 域 + 全局单例）
- `domain/changed` 变更事件（每次持久化写入后携带新快照与操作判别符）

## Depends On (上游依赖)
- `dsh-storage` [E1+E2+E3] - 后端注册表、kv facet、单元描述符与形态挂载点全部来自存储 hub
  - 证据: `src/index.ts:12 import storageBackendServiceKey + src/index.ts:44 inject ['storage'] + src/index.ts:110 ctx.storage.backend.get + src/index.ts:226 ctx.storage.mount('domain', facility)`

## Dependents (下游被依赖)
- `dsh-api-workspace-controller` - 订阅持久域变更以产出工作区增量
- `dsh-experimental-claude-code-mods` - $.store 的 per-plugin JSON 存储落在一个 storage domain 上
- `dsh-schedule` - 以 schema 校验的 domain/table 持久化任务，损坏即拒绝打开
- `dsh-session-projection-cache` - 打开 session_projcache 域并持有 per-record 键值表
- `dsh-workspace` - 用 defineDomain 声明 workspace 域并借 storageDomain 打开表与 global 状态，取得原子写与 schema 校验边界
