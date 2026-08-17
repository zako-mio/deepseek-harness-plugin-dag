# dsh-subagent-dsh-sdk

- 包名: `@deepseek-ai/dsh-subagent-dsh-sdk`
- 分组: G33 子代理外部后端
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/subagent/subagent-dsh-sdk`

## 为什么需要它（设计初衷）
进程外完整 DSH runtime 子 Agent：经 stdio JSON-RPC 驱动一个完整 peer harness（自有 cordis.yml 组合/持久化/模型路由），子进程能力完全自治。

来源：
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/subagent/subagent-dsh-sdk
- https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/implemented/feature/2026-07-27-typescript-sdk-and-sdk-subagent-backend.md

## 实现逻辑
进程外 SDK 子代理后端：每个 child 是完整 DeepSeek Harness runtime（自有 cordis.yml 组合/session/model/tools），经 dsh-sdk-client 的 DeepSeekHarness 高层 API 通过 stdio JSON-RPC 驱动；不共享父 Cordis context、不声明父强制 start capabilities；唯一读取 request.parent 的是 session workspace cwd。inject=['subagents']，subprocess 仅经 scrubbedParentEnv 值导入使用。

## Provides
- ctx.subagents 命名 provider 'dsh-sdk'(one-shot)
- startSdkRun(DeepSeekHarness 驱动)
- 子 runtime provider/model/maxTokens 配置

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - ContentBlock 类型
  - 证据: `packages/subagent/subagent-dsh-sdk/src/run.ts:16`
- `dsh-sdk-client` [编译依赖] - DeepSeekHarness/HarnessNotification 驱动子 runtime
  - 证据: `packages/subagent/subagent-dsh-sdk/src/run.ts:15,118`
- `dsh-session` [编译依赖] - SessionId/SessionEvent/TurnEndReason 类型
  - 证据: `packages/subagent/subagent-dsh-sdk/src/run.ts:17`
- `dsh-subagent` [运行时依赖] - inject ['subagents'] 注册 provider；SubagentProvider/SubagentResult/settleRunResult 类型与工具(E1)
  - 证据: `packages/subagent/subagent-dsh-sdk/src/index.ts:15-16,26, packages/subagent/subagent-dsh-sdk/src/run.ts:18-19`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
