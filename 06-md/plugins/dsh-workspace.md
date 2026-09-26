# dsh-workspace

- 包名: `@deepseek-ai/dsh-workspace`
- 分组: G50 工作区
- 拓扑层: Layer 3
- 来源层: L2 web-app
- 源码路径: `packages/workspace/workspace`

## 实现逻辑
以 Cordis Service 类 WorkspaceRegistry（static inject=['storageDomain','sessionPersistence']，src/index.ts:170-194）实现工作区实体注册表，启动时用 ctx.storageDomain.open 打开 name=workspace、version=2 的域规格，取得 workspaces 表与全局态（src/index.ts:198-202，src/spec.ts:76-84）。初始化先做 pendingMutation 恢复与 stored state 一致性校验，再按 initialized 标记决定是否用 sessionPersistence 的历史 header 一次性 bootstrap 出工作区记录与顺序（src/index.ts:204-218、src/index.ts:634-740、src/index.ts:748-783）。所有写操作串行挂在单条 operationTail 队列上（src/index.ts:886-895），每条记录由私有 WorkspaceEntity 承载，其 sessionIds 是把持久账户按「id 在账户中且 header 的 canonical cwd 等于工作区 path」同步过滤后的投影（src/entity.ts:101-103），写路径统一走 mutate→table.update 并盖章 updatedAt（src/entity.ts:202-220）。除 CRUD/排序/默认工作区外还维护注册表级归档集与置顶集，归档前以 waterfall 事件 workspace/session-activity 询问各 provider 会话是否活跃，拒绝则报 WorkspaceActiveSessionError（src/index.ts:363-385），带 stopActivity 时归档落盘后再 parallel 触发 workspace/session-stop 请求停止（src/index.ts:479-491）。路径唯一性由 realpathNormalize 统一规范化（src/paths.ts:52-57），另有 ./invariant 伴生插件订阅 domain/changed 断言实体缓存与持久表不漂移（src/invariant.ts:27-49）。

## Provides
- ctx.workspaceRegistry (持久化工作区实体注册表：工作区记录增删改查、稳定显示顺序、默认工作区初始化、会话归档/置顶集合、按 canonical cwd 校验的会话归属与顺序)
- 事件 workspace/session-activity (waterfall；归档前询问各 provider 该会话是否仍活跃，决定归档准入)
- 事件 workspace/session-stop (parallel；归档落盘后要求各 provider 停止该会话运行中的工作)
- storage 域规格 workspace v2 (workspaces 表 + bootstrap/顺序全局态，经 ctx.storageDomain 打开)

## Depends On (上游依赖)
- `dsh-invariants` [E1+E2] - ./invariant 伴生插件需向 runtime 不变量服务注册『实体缓存 ↔ 持久表』一致性断言
  - 证据: `src/invariant.ts:7 import；src/invariant.ts:16 export const inject=['invariants'] + src/invariant.ts:57 ctx.invariants.register(PACKAGE_NAME, install)`
- `dsh-session` [E1+E2] - 复用 SessionId/SessionHeader 类型与可选 sessions 服务，做会话存在性判定与 attach 时的 cwd 归属校验
  - 证据: `src/entity.ts:12 + src/index.ts:11 + src/spec.ts:10 + src/types.ts:9 import；src/index.ts:473 ctx.get('sessions')`
- `dsh-storage` [编译依赖] - 声明工作区域数据形态所在存储服务 seam 的 peer（源码无直接 import，随 dsh-storage-domain 一起装配）
  - 证据: `package.json:44 peerDependencies @deepseek-ai/dsh-storage`
- `dsh-storage-domain` [E1+E2] - 提供域数据形态（defineDomain/domainTable/KvTable/DomainGlobal），工作区记录与顺序全局态持久化在其之上
  - 证据: `src/entity.ts:13 + src/spec.ts:11 import；src/index.ts:171 static inject=['storageDomain','sessionPersistence'] + src/index.ts:198 ctx.storageDomain.open(workspaceDomainSpec)`

## Dependents (下游被依赖)
- `dsh-agent` - 回答 workspace/session-activity 的 turn 家族，并在 workspace/session-stop 时取消运行中的 agent
- `dsh-api-session-controller` - 工作区注册表与归档会话门控
- `dsh-api-workspace-controller` - 工作区注册表 seam（全部命令与状态源）
- `dsh-client-ui-conversation` - 工作区实体类型
- `dsh-schedule` - 以 SessionActivity 类型参与工作区归档准入与停止判定
- `dsh-subagent` - 响应工作区归档准入与活动上报
