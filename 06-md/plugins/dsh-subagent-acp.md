# dsh-subagent-acp

- 包名: `@deepseek-ai/dsh-subagent-acp`
- 分组: G39 子代理
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/subagent/subagent-acp`

## 实现逻辑
进程外 ACP 子代理后端：apply 校验两个 dispose 宽限期后把 `AcpProvider` 注册到 `ctx.subagents` 的 `acp` 名下 (src/index.ts:124-130)。该 provider 显式声明全部 start 能力为 false，因为进程外子代理无法履行 agentOptions/outputSchema/maxDepth/toolFilter/persona，并声明 `inheritsParentContext = false`（不跨进程继承会话）(src/index.ts:80-90)。start 先校验子进程 cwd 可用性并把失败包装为 ACP 配置错误，再组装 AcpRunSpec（命令、参数、权限自动应答策略、凭据清洗后的 env、宽限期）并调用 `startAcpRun`，其中 spawn 走 `ctx.subprocess.spawn` (src/index.ts:93-121)。run.ts 负责协议侧：内容块转换、stop reason 映射、EOF 驱动的宽限退出与升级终止 (src/run.ts:192-220、src/run.ts:336)。

## Provides
- ctx.subagents 上的 `acp` provider（进程外 ACP 子代理后端，每次运行独立进程/会话/模型/工具）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - ResolvedSubagentStartRequest.parent 为 Agent 类型
  - 证据: `package.json:31 peerDependencies '@deepseek-ai/dsh-agent'`
- `dsh-llm` [编译依赖] - 把模型内容块转换为 ACP 内容块
  - 证据: `src/run.ts:19 import type ContentBlock from '@deepseek-ai/dsh-llm'`
- `dsh-session` [编译依赖] - 子代理运行身份使用 SessionId
  - 证据: `src/run.ts:21 import type SessionId from '@deepseek-ai/dsh-session'`
- `dsh-subagent` [E1+E2] - provider 契约与注册入口由子代理 seam 提供
  - 证据: `src/index.ts:17 import { assertUsableCwd } + src/index.ts:22 inject ['subagents'] + src/index.ts:129 ctx.subagents.registerProvider`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
