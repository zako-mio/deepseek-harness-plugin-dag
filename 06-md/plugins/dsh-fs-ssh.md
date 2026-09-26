# dsh-fs-ssh

- 包名: `@deepseek-ai/dsh-fs-ssh`
- 分组: G39 SSH 远程执行
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/ssh/fs-ssh`

## 实现逻辑
以 SshFileSystem 继承 dsh-fs 的 FileSystem seam，把 resolve/stat/lstat/readText/streamText/readBytes/listDir/writeText/editText 等全部文件系统原语转成 ctx.ssh.request('fs.*') 远程调用 (src/index.ts:20-95)。写入与编辑会先经 sandboxPolicy 解析执行策略再随请求下发，并把远端 RemoteOperationError 按错误码映射为本仓 FsError (src/index.ts:82-104)。sandboxMode 直接取 sandboxPolicy 的 defaultMode (src/index.ts:23)。

## Provides
- ctx.fs (SSH 远程 FileSystem seam 提供者 SshFileSystem，供文件系统消费方使用)

## Depends On (上游依赖)
- `dsh-sandbox-policy` [E1+E2] - 读取默认沙箱模式并在写/编辑时解析策略
  - 证据: `src/index.ts:7 (type import) + src/index.ts:21 (static inject ['ssh','sandboxPolicy']) + src/index.ts:23 (ctx.sandboxPolicy.defaultMode)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
