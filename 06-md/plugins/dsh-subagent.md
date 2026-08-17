# dsh-subagent

- 包名: `@deepseek-ai/dsh-subagent`
- 分组: G19 子代理
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/subagent/subagent`

## 为什么需要它（设计初衷）
子 Agent 能力族的核心契约：定义 provider 注册、委派与续跑接口（ctx.subagents），让主 Agent 能把任务委派给子 Agent 并隔离上下文/token 成本。背后挂接多种 provider——进程内 spawn/fork、进程外 ACP、Claude Code/Codex、完整 DSH runtime，解决『一个接口背后变化极大的子 Agent 执行世界』问题。

发展史：2026-06-21 子 Agent capability seam 决策确立契约；2026-07-21 引入 continuable background subagents（可续跑后台子代理）；2026-07-26 合并 subagent control service 简化控制面。

来源：
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/subagent
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/subagent.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/implemented/feature/2026-06-21-subagent-capability-seam.md

## 实现逻辑
子代理能力缝(capability seam)的服务定义：SubagentRuntime extends Service 注册为 ctx.subagents，维护命名 provider 注册表。start() 先做能力校验与描述符快照再委派给 provider，并用 observeRun 发布 subagent/start、subagent/end 生命周期事件。构造时 ctx.inject(['agents']) 创建 SubagentContinuationManager 支撑可续聊子代理，ctx.inject(['sessionProjections']) 注册 subagentTiming/Identity 投影。

## Provides
- ctx.subagents(SubagentRuntime)
- subagent/provider-added|removed|start|end 事件
- SubagentContinuationManager
- subagent 标识/时序 sessionProjections
- SubagentRunId/descriptor 折叠/快照

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - ctx.inject(['agents']) 建立 ContinuationManager
  - 证据: `packages/subagent/subagent/src/index.ts:186`
- `dsh-session` [编译依赖] - ctx.get('sessions') 枚举子代理
  - 证据: `packages/subagent/subagent/src/list-children.ts:201,231`
- `dsh-tools` [编译依赖] - assertObjectJsonSchema 校验
  - 证据: `packages/subagent/subagent/src/index.ts:37`

## Dependents (下游被依赖)
- `dsh-client-ui-subagent` - SubagentAddress 与子代理语义类型
- `dsh-hooks-claude-code` - subagent start/end 配对 identity
- `dsh-host-apiproxy` - SubagentError/SubagentListEntry 类型
- `dsh-sdk-jsonrpc-server` - SubagentRuntime 类型 + ctx.on('subagent/end') 订阅生命周期
- `dsh-subagent-acp` - inject ['subagents'] 注册 provider；SubagentProvider/ResolvedSubagentStartRequest/AssistantOutputFold 类型(E1)
- `dsh-subagent-claude-code` - inject ['subagents'] 注册 provider；SubagentProvider/ResolvedSubagentStartRequest 类型(E1)
- `dsh-subagent-codex` - inject ['subagents'] 注册 provider；SubagentProvider/SubagentResult 类型(E1)
- `dsh-subagent-dsh-sdk` - inject ['subagents'] 注册 provider；SubagentProvider/SubagentResult/settleRunResult 类型与工具(E1)
- `dsh-subagent-fork-in-process` - inject subagents 注册 provider
- `dsh-subagent-spawn-in-process` - inject subagents 注册 provider
- `dsh-tool-ralph` - getProvider 校验 fresh provider
- `dsh-tool-subagent` - start/startContinuable/getProvider
- `dsh-tool-subagent-control` - followup/interrupt
- `dsh-tool-subagent-report` - registerContinuableSetup + reportFrom
- `dsh-workflow-worker-thread` - startChild 经 subagents.start(provider)
