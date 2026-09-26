# dsh-tool-bash

- 包名: `@deepseek-ai/dsh-tool-bash`
- 分组: G36 Shell 执行
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/shell/tool-bash`

## 实现逻辑
向模型注册 bash 工具作为 ctx.shell 的消费者：前台调用等待作业完成，有 ctx.jobs 时把进程注册为 job（run_in_background 立即返回 jobId，超时可按配置提升为后台）(src/index.ts:263-532)。execute 解析 per-call sandbox policy 与 workdir，经 ctx.shellEnv.collect 注入 DSH_* 环境，处理 sandbox_permissions/justification 的升级审批，再把 ShellRunResult 规范化渲染 (src/index.ts:478-528, src/render.ts:28-120)。background.ts 把 ShellProcess 适配为通用 job 的输出源与终态 (src/background.ts:44-129)。

## Provides
- 模型工具 bash (前台/后台执行、可选 ctx.jobs 集成与沙箱升级审批)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 读取调用者 Agent 会话以解析 workdir 与作业归属
  - 证据: `src/index.ts:21 import type { Agent }; package.json:30 peerDep`
- `dsh-llm` [编译依赖] - 用 HarnessError/TOOL_ABORTED 表达工具中止
  - 证据: `src/index.ts:20 import HarnessError; package.json:33 peerDep`
- `dsh-sandbox-policy` [运行时依赖] - 解析调用会话的完整沙箱执行策略
  - 证据: `src/index.ts:27 import type { SandboxPolicyService }; src/index.ts:215 ctx.get('sandboxPolicy'); src/index.ts:221 sandboxPolicy.resolve`
- `dsh-shell-env` [E1+E2] - 为每次执行收集受信任 DSH_* 环境变量
  - 证据: `src/index.ts:24 import type {}; src/index.ts:34 inject ['shellEnv']; src/index.ts:489 ctx.shellEnv.collect(exec)`
- `dsh-system-prompt` [运行时依赖] - 注入 bash 交叉调用指引段落
  - 证据: `src/index.ts:34 inject ['systemPrompt']; src/index.ts:257 ctx.systemPrompt.section`
- `dsh-tools` [E1+E2] - 注册 bash 工具定义并消费工具运行上下文
  - 证据: `src/index.ts:18-19 import defineTool/TOOL_ABORTED; src/index.ts:34 inject ['tools']; src/index.ts:540 ctx.tools.register`
- `dsh-user-approval` [运行时依赖] - 把沙箱升级请求路由到用户审批通道
  - 证据: `src/index.ts:23 import type {}; src/index.ts:247 ctx.get('approval')`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
