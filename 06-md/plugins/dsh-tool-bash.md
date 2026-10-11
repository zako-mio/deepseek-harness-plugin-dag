# dsh-tool-bash

- 包名: `@deepseek-ai/dsh-tool-bash`
- 分组: G34 Shell 执行
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/shell/tool-bash`

## 实现逻辑
作为 `ctx.shell` 能力 seam 的模型侧消费者注册 `bash` 工具：execute 先按调用会话解析沙箱策略，在模型同时给出 `sandbox_permissions` 与 `justification` 时经 `ctx.approval` 走共享的 fail-closed 越权审批，再构造 `ShellExecRequest` 交给 `ctx.shell.resolve/execute` (src/index.ts:477-529)。装配了 `ctx.jobs` 时每次调用都在启动时把进程登记为作业：`run_in_background` 立刻返回 jobId，前台调用则在该作业上等待，等待超时则把结果降级为 promoted 并把已产出输出交给后续 `job_output` 续读 (src/index.ts:262-366、src/background.ts:99-128)。结果渲染统一处理截断落盘路径、stderr 分段以及超时/外部停止/信号/退出码标记，非零退出只报告不报错 (src/render.ts:28-66)。注册形态随 registry 有无切换：无 `ctx.jobs` 时前台单版本，`ctx.inject(['jobs'])` 生效时替换为作业版本并在卸载时回退 (src/index.ts:541-554)。

## Provides
- ctx.tools 上的 `bash` 工具定义（前台/后台执行、超时转后台、沙箱越权审批入口）
- system prompt 片段 `tool:bash`（exit code 标记的跨调用使用指引）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 调用归属（exec.agent）与会话身份来自 agent 包类型
  - 证据: `package.json:30 peerDependencies '@deepseek-ai/dsh-agent'`
- `dsh-llm` [编译依赖] - 中止时抛出带 TOOL_ABORTED 码的 HarnessError
  - 证据: `src/index.ts:21 import { HarnessError } from '@deepseek-ai/dsh-llm'`
- `dsh-sandbox-policy` [运行时依赖] - 每次调用需解析本会话的完整常驻沙箱策略
  - 证据: `src/index.ts:209 ctx.get('sandboxPolicy') + src/index.ts:215 sandboxPolicy.resolve`
- `dsh-shell-env` [运行时依赖] - 把托管 DSH_* 环境变量注入每次执行
  - 证据: `src/index.ts:24 type import + src/index.ts:489 ctx.shellEnv.collect(exec)`
- `dsh-system-prompt` [运行时依赖] - 注册工具专属的提示片段
  - 证据: `src/index.ts:251 ctx.systemPrompt.section({ name: 'tool:bash' })`
- `dsh-tool-jobs` [组合依赖] - 模型侧收集/停止后台作业的工具由 tool-jobs 提供，缺它则后台能力不可用
  - 证据: `src/index.ts:503 报错文案要求同时装配 dsh-jobs 与 dsh-tool-jobs；packages/bundle/base/cordis.patch.yml:276-285 中 tool-bash 与 tool-jobs 同处 base`
- `dsh-tools` [E1+E2] - 工具必须注册进工具注册表才能被模型调用
  - 证据: `src/index.ts:19-20 import defineTool/TOOL_ABORTED + src/index.ts:34 inject 'tools' + src/index.ts:542 ctx.tools.register`
- `dsh-user-approval` [运行时依赖] - 沙箱越权必须先拿到人工审批通道
  - 证据: `src/index.ts:23 type import + src/index.ts:241 approver: ctx.get('approval')`
- `dsh-working-directory` [运行时依赖] - 缺省工作目录取自会话工作区，相对 workdir 据此解析
  - 证据: `src/index.ts:14 type import + src/index.ts:487 ctx.workingDirectory.ensure(exec.agent, exec.signal)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
