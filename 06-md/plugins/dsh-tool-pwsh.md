# dsh-tool-pwsh

- 包名: `@deepseek-ai/dsh-tool-pwsh`
- 分组: G36 Shell 执行
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/shell/tool-pwsh`

## 实现逻辑
向模型注册 pwsh 工具作为 ctx.shell 的 PowerShell 方言消费者：前台/后台执行、ctx.jobs 集成、DSH_* 环境注入、per-call sandbox policy 与升级审批、退出状态渲染均镜像 dsh-tool-bash (src/index.ts:212-544)。pwshDescription() 额外描述 Windows 沙箱下 ConstrainedLanguage 与命名管道 EPERM 边界 (src/index.ts:122-147)。background.ts 的进程→job 适配与 render.ts 的结果渲染故事与 bash 工具共用对称契约 (src/index.ts:276-379, 486-493)。

## Provides
- 模型工具 pwsh (PowerShell 方言的前台/后台执行、ctx.jobs 集成与沙箱升级审批)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 读取调用者 Agent 会话以解析 workdir 与作业归属
  - 证据: `src/index.ts:30 import type { Agent }; package.json:31 peerDep`
- `dsh-llm` [编译依赖] - 用 HarnessError/TOOL_ABORTED 表达工具中止
  - 证据: `src/index.ts:29 import HarnessError; package.json:33 peerDep`
- `dsh-sandbox-policy` [运行时依赖] - 解析调用会话的完整沙箱执行策略
  - 证据: `src/index.ts:36 import type { SandboxPolicyService }; src/index.ts:219 ctx.get('sandboxPolicy'); src/index.ts:226 sandboxPolicy.resolve`
- `dsh-shell-env` [E1+E2] - 为每次执行收集受信任 DSH_* 环境变量
  - 证据: `src/index.ts:32 import type {}; src/index.ts:50 inject ['shellEnv']; src/index.ts:511 ctx.shellEnv.collect(exec)`
- `dsh-system-prompt` [运行时依赖] - 注入 pwsh 交叉调用与 Windows 退出码指引段落
  - 证据: `src/index.ts:50 inject ['systemPrompt']; src/index.ts:264 ctx.systemPrompt.section`
- `dsh-tools` [E1+E2] - 注册 pwsh 工具定义并消费工具运行上下文
  - 证据: `src/index.ts:27-28 import defineTool/TOOL_ABORTED; src/index.ts:50 inject ['tools']; src/index.ts:593 ctx.tools.register`
- `dsh-user-approval` [运行时依赖] - 把沙箱升级请求路由到用户审批通道
  - 证据: `src/index.ts:33 import type {}; src/index.ts:254 ctx.get('approval')`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
