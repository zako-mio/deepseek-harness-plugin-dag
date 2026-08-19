# dsh-subagent

- 包名: `@deepseek-ai/dsh-subagent`
- 分组: G19 子代理
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/subagent/subagent`

## 为什么需要它（设计初衷）
子 Agent 能力族的核心契约：定义 provider 注册、委派与续跑接口（ctx.subagents），让主 Agent 能把任务委派给子 Agent 并隔离上下文/token 成本。背后挂接多种 provider——进程内 spawn/fork、进程外 ACP、Claude Code/Codex、完整 DSH runtime，解决『一个接口背后变化极大的子 Agent 执行世界』问题。RC7 移除 specialization preset 能力、描述符版本收敛为 v2。

发展史：RC8 子代理reportDelivery及时反馈并唤醒父任务 + 失败诊断回传

来源：
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/subagent
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/subagent.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/implemented/feature/2026-06-21-subagent-capability-seam.md

## 实现逻辑
index.ts:312-327 新增 drainContinuableChildren(parent, childIds): 释放指定父会话的常驻continuable直接子代理(验证父身份)。run-settlement.ts:21-28 新增 failureDetail 渲染provider自述诊断; types.ts:236-242 SubagentResult 新增 diagnostic 字段(限制4096字节)。

## Provides
- ctx.subagents(SubagentRuntime)
- subagent/provider-added|removed|start|end 事件
- SubagentContinuationManager
- subagent 标识/时序 sessionProjections
- SubagentRunId/descriptor 折叠/快照(v2)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - ctx.inject(['agents']) 建立 ContinuationManager
  - 证据: `packages/subagent/subagent/src/index.ts:186`
- `dsh-session` [编译依赖] - ctx.get('sessions') 枚举子代理
  - 证据: `packages/subagent/subagent/src/list-children.ts:201,231`
- `dsh-tools` [编译依赖] - assertObjectJsonSchema 校验
  - 证据: `packages/subagent/subagent/src/index.ts:37`

## Dependents (下游被依赖)
- `dsh-client-ui-subagent` - SubagentAddress 与子代理语义类型
- `dsh-experimental-agent-team` - teammate的continuable子代理提供者
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
