# dsh-subagent-claude-code

- 包名: `@deepseek-ai/dsh-subagent-claude-code`
- 分组: G39 子代理
- 拓扑层: Layer 7
- 来源层: L3 其余
- 源码路径: `packages/subagent/subagent-claude-code`

## 实现逻辑
按 profile 命名的 Claude Code 一次性子代理 provider：apply 解析配置、校验 disposeGraceMs 不超过定时器上限，并把 `ClaudeCodeProvider` 注册到 `ctx.subagents`（默认名 `claude-code`）(src/index.ts:123-146)。provider 声明 `NO_START_CAPABILITIES` 且 `inheritsParentContext = false`，start 先校验委托会话工作区 cwd，失败时若请求已中止则原样报中止、否则包装成 Claude Code 启动失败 (src/index.ts:73-99)。随后组装 ClaudeCodeRunSpec（可选 model、权限模式、env 覆盖、宽限期，spawn 走 `ctx.subprocess.spawn`）并交给 `startClaudeCodeRun`，由 run.ts 驱动官方 Agent SDK、消费查询流并把 SDK 派生的真实 CLI 置于共享 subprocess owner 之下 (src/index.ts:100-115、src/run.ts:385、src/process.ts:67)。

## Provides
- ctx.subagents 上的 `claude-code` provider（一次性 Claude Code 子代理后端，托管 SDK 派生的 CLI 进程）

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 把模型内容块/结果文本转换为 SDK 输入输出
  - 证据: `src/run.ts:18 import from '@deepseek-ai/dsh-llm'`
- `dsh-session` [编译依赖] - 子代理运行身份使用 SessionId
  - 证据: `src/run.ts:20 import type SessionId from '@deepseek-ai/dsh-session'`
- `dsh-subagent` [E1+E2] - provider 契约、能力常量与注册入口
  - 证据: `src/index.ts:12-19 import NO_START_CAPABILITIES/assertUsableCwd/assertPositiveFinite + src/index.ts:31 inject ['subagents'] + src/index.ts:141 registerProvider`
- `dsh-tool-subagent` [组合依赖] - 该后端必须与委托工具一起装配，模型侧才有入口启动它
  - 证据: `cordis.patch.yml:4-5 把 tool-subagent-claude-code 与 subagent-claude-code 装配在同一补丁；package.json:54 dependencies`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
