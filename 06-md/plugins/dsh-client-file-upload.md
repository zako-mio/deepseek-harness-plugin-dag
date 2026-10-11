# dsh-client-file-upload

- 包名: `@deepseek-ai/dsh-client-file-upload`
- 分组: G05 客户端运行时
- 拓扑层: Layer 4
- 来源层: L2 web-app
- 源码路径: `packages/client/file-upload`

## 实现逻辑
Host 半 FileUploads 继承 TypertRemoteService，把上传字节落到 ctx.attachments，并按接收 Agent 的精确 Session 暂存 receipt（src/index.ts:56-110、src/index.ts:179-210）。它向 ctx.connection.fetch 注册 /api 下的流式原始字节路由，并订阅 session/event 与 session/disposed 在提示被投递或会话销毁时回收 receipt（src/index.ts:71-81、src/index.ts:232-245）。浏览器半 FileUploadRuntime 经生成的 Remote 回退（inject ['remote']）提供按 Session 寻址的后台上传服务 ctx.fileUpload（src/client/index.ts:17-26）。

## Provides
- ctx.fileUploads (Host 上传存储与按会话暂存的 receipt 服务，含 upload/uploadStream/bindPrompt/retirePrompt)
- ctx.fileUpload (浏览器端后台上传服务，经 Remote 调用 Host)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 以 Agent/Session 归属上传并校验其在落盘后仍存活
  - 证据: `src/index.ts:5 import + src/index.ts:57 static inject ['agents'] + src/index.ts:195 ctx.agents.get(agent.id)`
- `dsh-client-connection` [E1+E2] - 在共享 /api 通道注册流式上传路由
  - 证据: `src/index.ts:7 import type + src/index.ts:72 ctx.connection.fetch.register`
- `dsh-commands` [E1+E2] - 让命令提交解析 staged 文件 receipt
  - 证据: `src/index.ts:8 import + src/index.ts:68 ctx.commands.registerFileReceiptResolver`
- `dsh-session` [E1+E2] - 按会话事件与销毁回收暂存 receipt
  - 证据: `src/index.ts:9 import + src/index.ts:80 ctx.on('session/event') + src/index.ts:81 ctx.on('session/disposed')`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 把该业务包的 /remote 命名空间装配进 Client
- `dsh-api-session-controller` - 为上传文件注册 Session→Agent 解析器
- `dsh-client-ui-conversation` - 草稿文件上传走 fileUpload 服务
- `dsh-experimental-webworker-runtime` - 页面侧文件上传钩子被替换为走 worker 隧道
