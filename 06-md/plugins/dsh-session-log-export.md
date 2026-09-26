# dsh-session-log-export

- 包名: `@deepseek-ai/dsh-session-log-export`
- 分组: G34 会话检索
- 拓扑层: Layer 17
- 来源层: L2 web-app
- 源码路径: `packages/session-query/session-log-export`

## 实现逻辑
以 fflate 流式 Zip 把单个会话的逻辑日志（header 行 + 逐事件 JSONL）连同子会话与引用附件打包导出：serializeSessionLog/readSessionLogText 生成规范 JSONL，sessionLogZipEntries 按 zip 顺序产出根日志、子代理日志与 media/files 条目，streamSessionLogZip 用 ReadableStream + 背压闸门（ResponseCapacityGate）增量压缩并支持取消 (src/archive.ts:110-169, 347-404, 545-616)。Host 侧注册 /export 命令与 /api/session.export 的 GET/HEAD 路由，校验 sessionId/includeDescendants 并返回 400/404/500 (src/index.ts:78-168)。浏览器侧提供 ctx.sessionLogDownload 控制器并挂载会话头部菜单项，订阅 command/executed 在 /export 成功后触发下载 (src/client/index.ts:36-63)。

## Provides
- ctx.sessionLogDownload (浏览器端会话日志导出下载控制器，供会话头部动作与 /export 命令共享)
- Web /export 命令与 /api/session.export ZIP 下载路由 (Host 侧流式导出能力)

## Depends On (上游依赖)
- `dsh-client-locale` [运行时依赖] - 注册 session-log-download 命名空间的中英文字典
  - 证据: `src/client/index.ts:30 inject ['locale']; src/client/index.ts:40 ctx.locale.register`
- `dsh-client-ui-commands` [运行时依赖] - 订阅 /export 命令执行成功事件以启动浏览器下载
  - 证据: `src/client/index.ts:6 import; src/client/index.ts:48 ctx.on('command/executed')`
- `dsh-client-ui-conversation` [编译依赖] - 声明会话头部工具插槽的运行时 props 类型
  - 证据: `src/client/index.ts:7 import; src/client/Dialog.tsx:16 PropsRuntime<'conversation.session.header.utilities'>`
- `dsh-client-ui-message-feedback` [E1+E2] - 探测 feedbackUi 可用性并在下拉菜单中提供反馈入口
  - 证据: `src/client/index.ts:10 import; src/client/index.ts:60 ctx.get('feedbackUi')`
- `dsh-client-ui-primitives` [编译依赖] - 复用 Button/Menu/Modal 等基础组件渲染菜单与下载弹窗
  - 证据: `src/client/HeaderAction.tsx:6 import; src/client/Dialog.tsx:3 import`
- `dsh-client-ui-renderer` [编译依赖] - 沿用客户端渲染层的类型环境
  - 证据: `src/client/index.ts:8 import`
- `dsh-client-ui-session` [编译依赖] - 沿用会话视图的类型环境
  - 证据: `src/client/index.ts:9 import`
- `dsh-commands` [E1+E2] - 注册 Web /export 命令作为导出入口
  - 证据: `src/index.ts:4,8 import; src/index.ts:41 inject ['commands']; src/index.ts:79 ctx.commands.register`
- `dsh-session` [编译依赖] - 使用 SessionId/SessionHeader/SessionEvent/SessionStore 类型与 SESSION_FORMAT_VERSION 序列化日志
  - 证据: `src/archive.ts:30,32 import; package.json:46 peerDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
