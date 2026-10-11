# dsh-api-workspace-controller

- 包名: `@deepseek-ai/dsh-api-workspace-controller`
- 分组: G02 API 网关与控制器
- 拓扑层: Layer 3
- 来源层: L2 web-app
- 源码路径: `packages/api/workspace-controller`

## 实现逻辑
实现 Host 侧 Workspace 业务 API：WorkspaceController 继承 TypertRemoteService 并以 namespace 'workspace' 注册 ctx.workspaceController(src/index.ts:51,67-78)，静态注入 typert/workspaceRegistry(src/index.ts:52)。Remote 方法 create/initializeDefault/rename/delete/insertBefore/insertSessionBefore/archiveSession/unarchiveSession/pinSession/unpinSession 委托 WorkspaceCommands(src/index.ts:85-187)，follow 由 WorkspaceFeed 产出可重连基线与增量(src/index.ts:194-197, src/feed.ts:1-20)。构造时还挂载 DirectoryPickerController 子插件，使无拾取后端的主机不注册该命名空间(src/index.ts:73-77, src/directory-picker.ts:1-8)。

## Provides
- ctx.workspaceController(Host Workspace 业务 API 与 ctx.remote.workspace 命名空间所有者，src/index.ts:43-51)
- ctx.remote.workspace 远程方法集 create/initializeDefault/rename/delete/insertBefore/insertSessionBefore/archiveSession/unarchiveSession/pinSession/unpinSession/follow(src/index.ts:85-197)

## Depends On (上游依赖)
- `dsh-api-gateway` [E1+E2] - Client 面经 Gateway 的 ctx.remote 暴露工作区命名空间
  - 证据: `package.json:47,50 dsh.client.external/inject + src/client/model.ts:5 import '@deepseek-ai/dsh-api-gateway/client' + src/client/index.ts:41 inject ['remote','remote.workspace']`
- `dsh-client-connection` [E1+E2] - Client 面工作区服务依赖承载层的连接生命周期
  - 证据: `package.json:80 peerDep + package.json:51 dsh.client.inject`
- `dsh-session` [编译依赖] - 在工作区视图中标注会话归属
  - 证据: `package.json:82 peerDep + src/types.ts:8 import '@deepseek-ai/dsh-session/types' + src/client/service.ts:4 import`
- `dsh-storage-domain` [E1+E2] - 订阅持久域变更以产出工作区增量
  - 证据: `package.json:83 peerDep + src/feed.ts:5 import DomainChanged + src/feed.ts:61 ctx.on('domain/changed')`
- `dsh-workspace` [E1+E2] - 读写权威工作区实体与登记顺序
  - 证据: `package.json:85 peerDep + src/feed.ts:6 import Workspace/workspaceView + src/index.ts:52 inject 'workspaceRegistry' + src/index.ts:100 ctx.workspaceRegistry.initializeDefault`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 把该业务包的 /remote 命名空间装配进 Client
- `dsh-client-ui-conversation` - 工作区控制器类型与状态
- `dsh-client-ui-schedule` - 同上，会话可用性还需工作区快照参与判定
- `dsh-client-ui-sidebar` - New Session 动作以 WorkspaceId 为可选参数，其不透明 id 类型由 workspace-controller 持有
- `dsh-client-ui-sidebar-browser` - Desktop 侧按工作区解析存储分区与 canonical CWD
- `dsh-client-ui-workspace` - 工作区列表、创建、归档与固定状态由工作区控制器拥有
