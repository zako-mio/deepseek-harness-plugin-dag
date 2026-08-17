# dsh-sandbox-policy

- 包名: `@deepseek-ai/dsh-sandbox-policy`
- 分组: G15 沙箱执行
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/sandbox/sandbox-policy`

## 为什么需要它（设计初衷）
沙箱策略解析的唯一所有者（ctx.sandboxPolicy）：统一为每次调用解析部署默认与每会话持久覆盖的 SandboxMode（read-only / workspace-write / danger-full-access）及不可变工作区根。若 FS 工具、单次 bash、终端会话各自解析 mode+workspaceRoot，会漂移成分裂的世界——此插件正是为防止策略分裂而生，默认 read-only 故障安全。

发展史：2026-07-06 sandbox 决策划定能力边界（进程约束缝，bwrap/Landlock/Seatbelt 后端）；2026-07-14 cross-family fs sandbox 决策让文件系统/子进程共享同一策略；策略由单个事件写入、重放可恢复。

来源：
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/sandbox/sandbox-policy
- https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/implemented/feature/2026-07-06-sandbox.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/sandbox.md

## 实现逻辑
沙箱策略中枢(SandboxPolicyService extends Service,注册 ctx.sandboxPolicy):部署默认模式(read-only fail-safe)+ per-session 解析——resolve({session}) 合并 approved override > 会话 sandbox/mode 事件折叠 > 部署默认;会话级 mode 切换以 setSandboxMode 写 sandbox/mode 日志事件;另经 ctx.inject(['systemPrompt']) 提供 sandbox:policy 动态上下文段落。

## Provides
- ctx.sandboxPolicy 服务
- sandbox/mode 会话事件 + setSandboxMode/effectiveSandboxMode
- ctx.systemPrompt context: sandbox:policy

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 类型依赖
  - 证据: `packages/sandbox/sandbox-policy/src/index.ts:24`
- `dsh-session` [运行时依赖] - 会话事件日志作模式折叠存储
  - 证据: `packages/sandbox/sandbox-policy/src/index.ts:26,139-150; session-mode.ts:70`
- `dsh-system-prompt` [运行时依赖] - 策略投影进运行时上下文
  - 证据: `packages/sandbox/sandbox-policy/src/index.ts:112-123`

## Dependents (下游被依赖)
- `dsh-bash-sandbox` - 默认模式事实
- `dsh-fs-sandbox` - static inject sandboxPolicy;默认模式取自 defaultMode
- `dsh-permission-presets` - sandbox 旋钮写穿
- `dsh-pwsh-sandbox` - 默认模式事实
- `dsh-terminal-bash` - 沙箱模式决策与默认模式
- `dsh-tool-bash` - standing policy 解析
- `dsh-tool-fs` - per-call 策略解析
- `dsh-tool-pwsh` - standing policy
- `dsh-tool-str-replace-editor` - MutationPolicy per-call 模式
