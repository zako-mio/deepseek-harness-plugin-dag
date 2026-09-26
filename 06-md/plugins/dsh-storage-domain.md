# dsh-storage-domain

- 包名: `@deepseek-ai/dsh-storage-domain`
- 分组: G40 存储
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/storage/storage-domain`

## 实现逻辑
向存储中枢挂载 domain 数据形态：DomainFacility 按 Config.backend/routes 路由到后端 kv facet，打开单元、用 zod schema 校验载入记录后构造 DomainImpl (src/index.ts:103-175)。DomainImpl 维护权威内存状态与每域唯一写链，写操作先落盘、再改内存、再 emit domain/changed，从而读与介质不产生分叉 (src/domain.ts:236-270)。spec.ts 用 defineDomain 校验域声明并投影为后端 descriptor (src/spec.ts:107-163)，invariant 保证事件快照等于内存状态 (src/invariant.ts:24-59)。

## Provides
- ctx.storage.domain (域数据形态 DomainFacility)
- ctx.storageDomain (域设施服务别名，供 Provider 注入)

## Depends On (上游依赖)
- `dsh-invariants` [E1+E2] - 注册 domain/changed 与内存状态一致性不变量
  - 证据: `src/invariant.ts:13 (import type InvariantFailure, InvariantInstaller) + src/invariant.ts:21 (inject ['invariants']) + src/invariant.ts:67 (ctx.invariants.register)`
- `dsh-storage` [E1+E2] - 作为存储中枢的 domain 数据形态，经后端路由打开域单元
  - 证据: `src/index.ts:12 (import storageBackendServiceKey) + src/index.ts:44 (inject ['storage']) + src/index.ts:108-117 (ctx.storage.backend.get / kv.open) + src/index.ts:228 (domainCtx.storage.mount)`

## Dependents (下游被依赖)
- `dsh-api-workspace-controller` - domain/changed 事件类型
- `dsh-schedule` - 把任务与投递历史持久化到 schedule 存储域
- `dsh-session-projection-cache` - 以域表承载每会话一条检查点记录
- `dsh-workspace` - 提供域数据形态（defineDomain/domainTable/KvTable/DomainGlobal），工作区记录与顺序全局态持久化在其之上
