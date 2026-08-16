# dsh-workspace

- 包名: `@deepseek-ai/dsh-workspace`
- 分组: G25 宿主服务
- 拓扑层: Layer 3
- 来源层: L2 web-app
- 源码路径: `packages/workspace/workspace`

## 实现逻辑
工作区实体注册表 ctx.workspaceRegistry：storageDomain 打开 workspace 域（workspaces 表+全局顺序/归档集+pending-mutation 恢复）；sessionPersistence 建 canonical-cwd 头索引与一次性历史 bootstrap；create/get/list/delete/insertBefore/archiveSession，实体经 WorkspaceEntity 校验会话成员。

## Provides
- ctx.workspaceRegistry（WorkspaceRegistry 服务）

## Depends On (上游依赖)
- `dsh-session` [编译依赖] - SessionHeader/SessionId 类型
  - 证据: `packages/workspace/workspace/package.json:43; src/index.ts:12`
- `dsh-storage-domain` [编译依赖] - DomainGlobal/KvTable 类型与域读写
  - 证据: `packages/workspace/workspace/package.json:41; src/index.ts:14`

## Dependents (下游被依赖)
- `dsh-client-ui-agent-preset` - 创作后落新会话
- `dsh-host-apiproxy` - workspace 域值类型与错误
