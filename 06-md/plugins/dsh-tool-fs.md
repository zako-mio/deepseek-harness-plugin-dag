# dsh-tool-fs

- 包名: `@deepseek-ai/dsh-tool-fs`
- 分组: G13 文件系统
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/fs/tool-fs`

## 实现逻辑
模型面向的文件系统工具套件:apply() 经 ctx.tools.register 注册 read/write/edit 工具(read 附带流式大文件/窗口渲染/观察事件,write/edit 通过 FsSandboxController 解析 per-call 沙箱策略、经 ctx.waterfall 取 fs/write-intent|fs/edit-intent 守卫并 emit fs/observed);read_image 仅在 ctx.inject(['attachments']) 挂载时注册;每工具同时注册 ctx.systemPrompt.section 引导文本。

## Provides
- ctx.tools 注册 read/write/edit/read_image(条件)
- fs/observed 事件发射
- fs/write-intent、fs/edit-intent waterfall 触发点
- ctx.systemPrompt section: tool:read/write/edit

## Depends On (上游依赖)
- `dsh-fs-observation-policy` [运行时依赖] - fs/* 事件槽的监听方
  - 证据: `packages/fs/tool-fs/src/write.ts:111,122`
- `dsh-llm` [运行时依赖] - read_image 能力门控
  - 证据: `packages/fs/tool-fs/src/read-image.ts:68,72`
- `dsh-sandbox-policy` [运行时依赖] - per-call 策略解析
  - 证据: `packages/fs/tool-fs/src/sandbox.ts:46-49,89`
- `dsh-session` [运行时依赖] - 解析会话 cwd
  - 证据: `packages/fs/tool-fs/src/session-cwd.ts:24`
- `dsh-tools` [运行时依赖] - 工具注册管线
  - 证据: `packages/fs/tool-fs/src/index.ts:22; write.ts:69`
- `dsh-user-approval` [运行时依赖] - approveEscalation 的 approver 通道
  - 证据: `packages/fs/tool-fs/src/sandbox.ts:100`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
