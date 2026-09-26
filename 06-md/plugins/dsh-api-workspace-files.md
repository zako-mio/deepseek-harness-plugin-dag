# dsh-api-workspace-files

- 包名: `@deepseek-ai/dsh-api-workspace-files`
- 分组: G02 API 网关与控制器
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/api/workspace-files`

## 实现逻辑
WorkspaceFiles 继承 TypertRemoteService 并注册 workspaceFiles 服务，注入 fs/sandboxPolicy/sessions/typert，并在构造时注册 workspaceFileScope lookup：把 SessionId 解析为 workspaceRoot（活会话头或持久化头，缺 cwd 回退 sandboxPolicy.workspaceRoot）(src/index.ts:199-222)。read 以 fs.streamText 流式切页（不整文件读入、超 maxBytes 拒绝、页内含 NUL 判为二进制）(src/index.ts:113-160, 232-246)；readBytes/stat 走 fs.readByteRange/readBytes/stat 并施加 maxFileBytes 上限 (src/index.ts:256-293)；list 在 lstat 后经 confine 校验目录位于工作区内再 listDir (src/index.ts:302-328)。changes 流由 WorkspaceChangeFeed 订阅 fs/observed、按目标 watch，初始化后先产 ready 再产 change 帧 (src/changes.ts:39-109)；客户端另提供 file 协议的 ResourceProvider (src/client/provider.ts:46-112)。

## Provides
- ctx.remote.workspaceFiles（workspaceFiles 命名空间：read/readBytes/stat/list/changes，只读文件预览与工作区目录观测）
- workspaceFileScope Typert lookup 与客户端 file 协议 ResourceProvider

## Depends On (上游依赖)
- `dsh-api-gateway` [编译依赖] - 客户端 Remote 载体
  - 证据: `src/client/index.ts:9 import + src/client/remote.ts:6 import`
- `dsh-client-resources` [编译依赖] - 客户端 file 资源 provider 注册
  - 证据: `src/client/index.ts:10 import + src/client/provider.ts:24 import`
- `dsh-sandbox-policy` [运行时依赖] - 会话无 cwd 时的工作区根回退
  - 证据: `src/index.ts:27 import type {} + src/index.ts:188 static inject 'sandboxPolicy'`
- `dsh-session` [E1+E2] - 把会话身份解析为工作区根
  - 证据: `src/index.ts:28 import + src/index.ts:209 scope.sessions.get(sessionId)`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配 workspaceFiles 命名空间
- `dsh-client-ui-deliverables` - 读取工作区文件内容
- `dsh-client-ui-sidebar-documentpreview` - 工作区文件读取的类型与 remote 调用签名
- `dsh-client-ui-sidebar-files` - 工作区文件条目类型
- `dsh-office-to-pdf` - 按 Session 授权读取/校验源文件元数据
