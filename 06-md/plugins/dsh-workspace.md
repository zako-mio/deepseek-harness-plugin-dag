# dsh-workspace

- 包名: `@deepseek-ai/dsh-workspace`
- 分组: G48 工作区
- 拓扑层: Layer 2
- 来源层: L2 web-app
- 源码路径: `packages/workspace/workspace`

## 实现逻辑
WorkspaceRegistry extends Service 以 'workspaceRegistry' 名注册，static inject ['storageDomain','sessionPersistence']；Service.init 里打开 workspace 域（v2：workspaces 表 + global 单例）、恢复未完成的两次写标记、校验已存状态，未初始化时先建 header 索引再跑一次性 history bootstrap，最后索引在线 session 并重建实体缓存 (src/index.ts:170-218, src/spec.ts:76-84)。对外提供 create/initializeDefault/list/insertBefore/delete 与 archiveSession/unarchiveSession/pinSession/unpinSession 等耐久操作，全部经 enqueueOperation 串到同一条写链上，check-then-write 不可交错 (src/index.ts:236-242, src/index.ts:363-385, src/index.ts:397-464)。归档前用 waterfall 'workspace/session-activity' 询问各 provider 是否仍有活动（非空即拒），带 stopActivity 时先落盘再 parallel 'workspace/session-stop' 广播停止请求，失败只记日志不回滚归档 (src/index.ts:371-383, src/index.ts:480-491)。实体写入统一走 table.update 单写路径，在同一链槽内 stamp updatedAt 并剪除已失效的候选 session，无变化则用哨兵中止以免重写介质 (src/entity.ts:202-220)。

## Provides
- ctx.workspaceRegistry (持久 workspace 注册表：目录归属与稳定顺序、归档/置顶全局集合、会话成员校验)
- workspace/session-activity 与 workspace/session-stop 事件 (归档前的活动查询 waterfall 与停止广播 parallel 的扩展点)

## Depends On (上游依赖)
- `dsh-session` [E1+E2] - 以 SessionHeader 的 canonical cwd 判定 workspace 成员资格，并在 create/initializeDefault 时用在线 session store 判断是否为空历史
  - 证据: `package.json:32 peerDep + src/index.ts:11 import type { SessionHeader, SessionId } + src/index.ts:260 ctx.get('sessions')`
- `dsh-storage-domain` [E1+E2] - 用 defineDomain 声明 workspace 域并借 storageDomain 打开表与 global 状态，取得原子写与 schema 校验边界
  - 证据: `package.json:34 peerDep + src/index.ts:13 import type { DomainGlobal, KvTable } + src/spec.ts:11 import { defineDomain, domainTable } + src/index.ts:198 ctx.storageDomain.open(workspaceDomainSpec)`

## Dependents (下游被依赖)
- `dsh-agent` - 回答 Workspace 归档准入的 turn 家族活动，并在归档时按用户停下的方式取消该 turn
- `dsh-api-session-controller` - 按工作区登记会话并实现归档准入
- `dsh-api-workspace-controller` - 读写权威工作区实体与登记顺序
- `dsh-client-ui-conversation` - 工作区实体类型
- `dsh-schedule` - 参与工作区归档准入：有活跃提醒的会话拒绝归档，归档停止则删除其任务行
- `dsh-subagent` - 归档准入订阅 workspace 会话活动/停止事件
