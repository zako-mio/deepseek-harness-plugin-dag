# dsh-tool-fs

- 包名: `@deepseek-ai/dsh-tool-fs`
- 分组: G16 文件系统
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/fs/tool-fs`

## 实现逻辑
以 ctx.fs 文件系统接缝为唯一后端，实现模型面向的 read / read_image / write / edit 四个工具：apply 先用 schemastery 补齐并校验读窗口上限，再依次注册 read、read_image（仅当 attachments 挂载时经 ctx.inject 注册）、write、edit (src/index.ts:55-79)。read 先做一次 stat 判定缺失/类型/尺寸路由，大文件或尺寸未知走 streamText，再由 buildWindow 生成带行号的有界窗口并 emit fs/observed (src/read.ts:137-164)。write/edit 先由 FsSandboxController 解析沙箱升级策略、经 waterfall 取可选守卫意图，再调 ctx.fs.writeText / editText，失败经 remediateFsError 映射为稳定诊断 (src/write.ts:112-131, src/edit.ts:119-147)。

## Provides
- ctx.tools 的 read 工具（读取 UTF-8 文本文件，返回带行号的有界窗口）
- ctx.tools 的 write 工具（创建或整体覆盖 UTF-8 文本文件）
- ctx.tools 的 edit 工具（按字面文本替换，默认要求唯一匹配）
- ctx.tools 的 read_image 工具（仅在 attachments 服务挂载时注册，返回图像内容块）
- fs/observed 观察事件（记录已读版本/缺失，供 fs-observation-policy 支撑守卫式变更）
- tool:read / tool:write / tool:edit 三条 systemPrompt 片段（按 scope 是否注册工具条件性输出）

## Depends On (上游依赖)
- `dsh-llm` [E1+E2] - 解析当前路由模型是否声明 image 输入（严格能力闸门），并构造图像内容块
  - 证据: `src/read-image.ts:18 import type ContentBlock + src/read-image.ts:124 ctx.get('llm')`
- `dsh-sandbox-policy` [E1+E2] - 解析每会话沙箱模式；受限文件系统已挂载但策略服务缺失时 fail-loud
  - 证据: `src/sandbox.ts:17 import type SandboxPolicyService + src/sandbox.ts:46 ctx.get('sandboxPolicy')`
- `dsh-session` [编译依赖] - peer 声明，用于工具观察事件与会话作用域类型的对齐
  - 证据: `package.json:40 peerDependencies @deepseek-ai/dsh-session`
- `dsh-system-prompt` [运行时依赖] - 注册工具使用指引片段，并按 scope 内工具是否注册决定文本
  - 证据: `src/read.ts:69-75 ctx.systemPrompt.section + package.json:41 peerDependencies`
- `dsh-tools` [E1+E2] - 注册工具定义与参数/输出 schema，并在 execute 期取得 ToolExecution 与渲染钩子
  - 证据: `src/edit.ts:9 import defineTool + src/index.ts:23 static inject ['tools','fs','systemPrompt','workingDirectory'] + src/edit.ts:85 ctx.tools.register`
- `dsh-user-approval` [E1+E2] - 升级到更宽沙箱模式的请求经审批服务裁决
  - 证据: `src/index.ts:11 import type {} from '@deepseek-ai/dsh-user-approval' + src/sandbox.ts:100 ctx.get('approval')`
- `dsh-working-directory` [E1+E2] - 解析会话当前工作目录作为 fs 调用的 cwd
  - 证据: `src/index.ts:8 import type {} from '@deepseek-ai/dsh-working-directory' + src/session-cwd.ts:23 ctx.workingDirectory.ensure`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
