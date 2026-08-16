# dsh-subagent-acp

- 包名: `@deepseek-ai/dsh-subagent-acp`
- 分组: G33 子代理外部后端
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/subagent/subagent-acp`

## 实现逻辑
进程外 ACP 子代理后端：在独立子进程中按 Agent Client Protocol 驱动子 agent，子进程拥有自己的 process/session/model/tools，不共享父 Cordis context、不声明父强制的 start capabilities；唯一读取 request.parent 的是 session workspace cwd(resolveCwd)。permission 策略自动应答 session/request_permission(reject 默认/allow)。经外部 @agentclientprotocol/sdk(0.25.1) 通信——不依赖 dsh-acp seam。

## Provides
- ctx.subagents 命名 provider 'acp'
- startAcpRun 进程外驱动
- PermissionPolicy 权限应答

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - ContentBlock 类型
  - 证据: `packages/subagent/subagent-acp/src/run.ts:25`
- `dsh-session` [编译依赖] - SessionId 类型
  - 证据: `packages/subagent/subagent-acp/src/run.ts:26`
- `dsh-subagent` [运行时依赖] - inject ['subagents'] 注册 provider；SubagentProvider/ResolvedSubagentStartRequest/AssistantOutputFold 类型(E1)
  - 证据: `packages/subagent/subagent-acp/src/index.ts:14-19,24, packages/subagent/subagent-acp/src/run.ts:27-28`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
