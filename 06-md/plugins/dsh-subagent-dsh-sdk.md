# dsh-subagent-dsh-sdk

- 包名: `@deepseek-ai/dsh-subagent-dsh-sdk`
- 分组: G39 子代理
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/subagent/subagent-dsh-sdk`

## 实现逻辑
进程外 DSH SDK 子代理后端：apply 校验超时/宽限期与 maxTokens，把 dshBin 与 patches 解析为真实文件路径后注册 `SdkSubagentProvider`（默认名 `dsh-sdk`）(src/index.ts:169-184)。能力集在 NO_START_CAPABILITIES 之上只放开 `agentOptions`，并把请求中的 provider/model/reasoningEffort/maxTokens 解析进子运行时的进程级握手，其余启动特性仍归子进程所有 (src/index.ts:99-117、src/index.ts:124-128)。start 校验 cwd 后组装 SdkRunSpec（profile、patches、隔离 dshHome、cwd 与父会话 originCwd、env、宽限期）交给 `startSdkRun`，由 run.ts 通过 `@deepseek-ai/dsh-sdk-client` 以 stdio JSON-RPC 驱动完整子 Harness，并负责 shutdown 交换与 EOF 宽限退出 (src/index.ts:134-166、src/run.ts:22、src/run.ts:231)。

## Provides
- ctx.subagents 上的 `dsh-sdk` provider（进程外完整 Harness 子代理后端，stdio JSON-RPC 驱动）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 解析子路由 agentOptions 并读取父会话 origin 目录
  - 证据: `src/index.ts:18 import type { AgentOptions } + src/index.ts:153 request.parent.session.header.cwd`
- `dsh-llm` [编译依赖] - 内容块与结果文本用于协议载荷
  - 证据: `src/run.ts:23 import from '@deepseek-ai/dsh-llm'`
- `dsh-session` [编译依赖] - 子代理运行身份使用 SessionId
  - 证据: `src/run.ts:24 import type SessionId from '@deepseek-ai/dsh-session'`
- `dsh-subagent` [E1+E2] - provider 契约、能力基线与注册入口
  - 证据: `src/index.ts:19-20 import NO_START_CAPABILITIES/assertUsableCwd/assertPositiveFinite + src/index.ts:31 inject ['subagents'] + src/index.ts:184 registerProvider`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
