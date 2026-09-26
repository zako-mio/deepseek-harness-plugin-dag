# dsh-client-file-upload

- 包名: `@deepseek-ai/dsh-client-file-upload`
- 分组: G05 客户端运行时
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/client/file-upload`

## 实现逻辑
Host 侧 `FileUploads extends TypertRemoteService` 承接待上传文件：`upload` 走 base64 编码路径、`uploadStream` 走原始字节流，均委托 `ctx.attachments` 落盘 (src/index.ts:105-131)，并在 Agent 会话作用域下以 receiptId 暂存，`bindPrompt`/`retirePrompt` 随 prompt 生命周期提交或回滚绑定 (src/index.ts:139-181)。它向 Connection 注册 `POST` 流式路由 `handleFileUploadHttp`，校验 content-type 与 sessionId 后把请求体转成 AsyncIterable (src/index.ts:72-80, src/http-route.ts:22-81)，并通过 `session/event` 观察 user/message 来退役已消费 receipt (src/index.ts:241-254)。

## Provides
- ctx.fileUploads (Host 侧文件上传存储与 Agent 级暂存 receipt 服务)
- 上传 HTTP 流式路由 (FILE_UPLOAD_PATH，application/octet-stream)
- CommandFileReceiptResolver 注册 (让命令层解析上传 receipt)
- ctx.fileUpload (浏览器侧后台上传服务 FileUploadRuntime)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 以接收 Agent 及其 session 作为上传暂存的作用域与生命周期主体
  - 证据: `src/index.ts:5 + src/index.ts:58 static inject 'agents' + src/index.ts:199 ctx.agents.get`
- `dsh-client-connection` [E1+E2] - 在 Connection 的 fetch 注册表上挂原始字节上传路由
  - 证据: `src/index.ts:7 + src/index.ts:58 inject 'connection' + src/index.ts:73 ctx.connection.fetch.register`
- `dsh-commands` [运行时依赖] - 让命令 prompt 能解析上传 receipt 为文件引用
  - 证据: `src/index.ts:8 + src/index.ts:58 inject 'commands' + src/index.ts:69 ctx.commands.registerFileReceiptResolver`
- `dsh-scope` [编译依赖] - 用 scopeOf 校验操作发生在目标 Agent 自身作用域内
  - 证据: `src/index.ts:9`
- `dsh-session` [编译依赖] - 以 SessionId 寻址会话并观察 session/event 退役 receipt
  - 证据: `src/index.ts:10 + src/client/contract.ts:1 + src/http-route.ts:4`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配文件上传命名空间
- `dsh-api-session-controller` - 上传收据解析与 Agent 解析登记
- `dsh-client-ui-conversation` - 浏览器 Worker 文件上传服务
- `dsh-experimental-webworker-runtime` - 复用文件上传类型于 Worker 传输层
