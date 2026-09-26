# dsh-sandbox-policy

- 包名: `@deepseek-ai/dsh-sandbox-policy`
- 分组: G30 沙箱
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/sandbox/sandbox-policy`

## 实现逻辑
SandboxPolicyService（ctx.sandboxPolicy）是文件沙箱策略的单一归属：持有部署默认 mode 与 fallback workspaceRoot，并按 (显式 override > 会话最近 sandbox/mode 事件 > 部署默认) 结合 session.cwd 解析出每次调用的 SandboxExecutionPolicy（src/index.ts:110-181）。它把 sandboxMode 折叠注册为 session-projection 单元（src/index.ts:133-139），并在每次请求前经 systemPrompt.context 注入策略文本（src/index.ts:141-152）。session-mode.ts 定义 log-only 的 sandbox/mode 事件与其唯一写路径 setSandboxMode（src/session-mode.ts:33-54）。

## Provides
- ctx.sandboxPolicy (文件沙箱模式与 workspace 根的统一策略解析与 per-session override 折叠)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 合并 agent 请求上下文事件类型以取到会话
  - 证据: `src/index.ts:27 type import`
- `dsh-invariants` [E1+E2] - 注册本包事件字段的运行时不变式检查
  - 证据: `src/invariant.ts:5 import + src/invariant.ts:13 inject + src/invariant.ts:43 ctx.invariants.register`
- `dsh-session` [E1+E2] - 读取会话 cwd/日志并在事件上声明 sandbox/mode 事件类型
  - 证据: `src/index.ts:29 import + src/session-mode.ts:21 import + src/invariant.ts:25 ctx.sessions`
- `dsh-session-projection` [E1+E2] - 把 sandboxMode 作为投影单元注册并读取会话模式覆盖
  - 证据: `src/index.ts:30 type import + src/index.ts:119 static inject + src/index.ts:133 register`
- `dsh-system-prompt` [运行时依赖] - 向模型请求注入解析后的文件策略文本
  - 证据: `src/index.ts:31 type import + src/index.ts:141-144 systemPrompt.context`

## Dependents (下游被依赖)
- `dsh-api-terminal-controller` - 取工作目录与沙箱工作区根
- `dsh-api-workspace-files` - 会话无 cwd 时的工作区根回退
- `dsh-bash-sandbox` - 读取部署默认沙箱模式并解析每次调用的完整策略
- `dsh-client-ui-deliverables` - native open 前校验沙箱策略
- `dsh-fs-sandbox` - 解析每调用会话的沙箱模式与工作区根
- `dsh-fs-ssh` - 读取默认沙箱模式并在写/编辑时解析策略
- `dsh-permission-presets` - 按预设写穿 sandbox/mode 规范 setter
- `dsh-plugin-manager` - 解析会话沙箱模式，决定管理操作是否需要 danger-full-access 提权
- `dsh-ptc-runtime-node` - 读取部署/会话沙箱策略作为执行的文件效应边界
- `dsh-pwsh-sandbox` - 读取部署默认沙箱模式并解析每次调用的完整策略
- `dsh-subagent` - 捕获父会话沙箱覆盖并播种给子代理
- `dsh-terminal-bash` - 解析当前会话的沙箱执行策略
- `dsh-tool-bash` - 解析调用会话的完整沙箱执行策略
- `dsh-tool-fs` - 解析每调用沙箱策略并映射拒绝错误
- `dsh-tool-pwsh` - 解析调用会话的完整沙箱执行策略
- `dsh-tool-str-replace-editor` - 解析每调用沙箱策略并映射拒绝错误
- `dsh-tools` - 引入沙箱策略服务的上下文类型合并
- `dsh-workflow-ptc` - 按调用方 Session 解析文件/沙箱策略并施加于运行
