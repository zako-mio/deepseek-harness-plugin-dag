# dsh-tool-pwsh

- 包名: `@deepseek-ai/dsh-tool-pwsh`
- 分组: G34 Shell 执行
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/shell/tool-pwsh`

## 实现逻辑
`ctx.shell` 的 PowerShell 侧消费者，逐调用镜像 `dsh-tool-bash` 的契约：前台/`run_in_background` 执行、把进程登记为 `pwsh` 类作业、超时转后台、DSH_* 环境变量、按会话解析沙箱策略并经 `ctx.approval` 处理越权 (src/index.ts:503-554、src/index.ts:43-47)。差异集中在 PowerShell 方言：工具描述声明原生 `C:\...` 路径与 `$env:NAME` 变量，并在挂载了限制型执行器时补充 ConstrainedLanguage 与命名管道 EPERM 的边界说明 (src/index.ts:123-151)。结果渲染是与 bash 渲染器对称的孪生实现，输出 stdout/分段 stderr/沙箱拒绝与截断提示后追加退出码标记 (src/render.ts:48-60、src/index.ts:492-499)。

## Provides
- ctx.tools 上的 `pwsh` 工具定义（PowerShell 前台/后台执行、超时转后台、沙箱越权审批入口）
- system prompt 片段 `tool:pwsh`（退出码标记与 Windows 强杀语义指引）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 调用归属与会话身份来自 agent 包类型
  - 证据: `package.json:31 peerDependencies '@deepseek-ai/dsh-agent'`
- `dsh-llm` [编译依赖] - 中止时抛 TOOL_ABORTED 结构化错误
  - 证据: `src/index.ts:30 import { HarnessError } from '@deepseek-ai/dsh-llm'`
- `dsh-sandbox-policy` [运行时依赖] - 解析本会话的常驻沙箱策略
  - 证据: `src/index.ts:221 ctx.get('sandboxPolicy') + src/index.ts:228 sandboxPolicy.resolve`
- `dsh-shell-env` [运行时依赖] - 注入托管 $env:DSH_* 变量
  - 证据: `src/index.ts:32 type import + src/index.ts:519 dshEnv: ctx.shellEnv.collect(exec)`
- `dsh-system-prompt` [运行时依赖] - 注册 pwsh 专属提示片段
  - 证据: `src/index.ts:266 ctx.systemPrompt.section({ name: 'tool:pwsh' })`
- `dsh-tool-jobs` [组合依赖] - 模型侧作业收集与停止工具由 tool-jobs 提供
  - 证据: `src/index.ts:528 报错文案要求装配 dsh-jobs 与 dsh-tool-jobs；packages/bundle/base/cordis.patch.yml:280-285 tool-pwsh 与 tool-jobs 同处 base`
- `dsh-tools` [E1+E2] - 工具必须注册进工具注册表
  - 证据: `src/index.ts:28-29 import defineTool/TOOL_ABORTED + src/index.ts:50 inject 'tools' + src/index.ts:603 ctx.tools.register`
- `dsh-user-approval` [运行时依赖] - 沙箱越权必须先拿到人工审批通道
  - 证据: `src/index.ts:33 type import + src/index.ts:256 approver: ctx.get('approval')`
- `dsh-working-directory` [运行时依赖] - 缺省工作目录与相对 workdir 解析
  - 证据: `src/index.ts:24 type import + src/index.ts:513 ctx.workingDirectory.ensure(exec.agent, exec.signal)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
