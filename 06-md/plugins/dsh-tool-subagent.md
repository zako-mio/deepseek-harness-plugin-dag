# dsh-tool-subagent

- 包名: `@deepseek-ai/dsh-tool-subagent`
- 分组: G41 子代理
- 拓扑层: Layer 7
- 来源层: L1 核心集
- 源码路径: `packages/subagent/tool-subagent`

## 实现逻辑
注册 model 可见委派工具 subagent：按配置绑定一个 ctx.subagents provider，工具随 provider 出现/移除动态注册与注销，并据 inheritsParentContext 选择措辞 (src/index.ts:360-606)。execute() 解析子代理模型路由（可选 list_subagent_models 策略与 preflight），前台调用 await start() 并 settleForegroundRun，一次性后台走 ctx.jobs，可续后台走 startContinuable (src/index.ts:471-568)。model-selection*.ts 实现逐会话路由策略、持久化投影与发现工具，invariant 保证可选路由定义可重构 (src/model-selection.ts:99-196, src/model-selection-state.ts:37-81, src/invariant.ts:19-41)。

## Provides
- model 可见工具 `subagent` (经 provider 启动前/后台子代理)
- model 可见工具 `list_subagent_models` (子代理 LLM 路由发现)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 读取调用 Agent 与 reconciling 组合作用域
  - 证据: `src/index.ts:15 (import type Agent, AgentOptions) + src/index.ts:658 (ctx.get('agents'))`
- `dsh-invariants` [E1+E2] - 注册可选路由定义完整性不变量
  - 证据: `src/invariant.ts:8 (import type InvariantFailure, InvariantInstaller) + src/invariant.ts:16 (inject ['invariants']) + src/invariant.ts:49 (ctx.invariants.register)`
- `dsh-llm` [E1+E2] - 子代理路由发现与 preflight
  - 证据: `src/index.ts:16 (import ReasoningEffortId) + src/list-models.ts:4-5 (import type LlmRuntime, LlmProviderInfo) + src/index.ts:498 (runtimeCtx.get('llm'))`
- `dsh-scope` [E1+E2] - 识别 preset 组合作用域
  - 证据: `src/index.ts:13 (import scopeChainOf, scopeOf) + src/index.ts:654 (scopeOf(ctx))`
- `dsh-session` [编译依赖] - 会话身份与投影读取
  - 证据: `src/index.ts:19-20 (import SessionSeq, type Session) + src/model-selection-state.ts:4 (import type Session)`
- `dsh-session-projection` [E1+E2] - 注册逐会话模型选择策略投影
  - 证据: `src/model-selection-state.ts:5-6 (import ProjectionDefinition, SessionProjectionRegistry) + src/index.ts:45 (inject ['sessionProjections']) + src/index.ts:326 (ctx.sessionProjections.register)`
- `dsh-subagent` [E1+E2] - 启动子代理并复用 seam 辅助
  - 证据: `src/index.ts:21-26 (import assertSubagentMaxDepth, parentAgentOptionsForDelegation, settleRun, 类型) + src/index.ts:45 (inject ['tools','subagents','systemPrompt','sessionProjections']) + src/index.ts:530 (ctx.subagents.startContinuable) + src/index.ts:563 (ctx.subagents.start)`
- `dsh-system-prompt` [运行时依赖] - 为可续后台委派注册提示段
  - 证据: `src/index.ts:45 (inject ['systemPrompt']) + src/index.ts:598 (runtimeCtx.systemPrompt.section)`
- `dsh-tools` [E1+E2] - 注册委派工具定义
  - 证据: `src/index.ts:14 (import defineTool) + src/index.ts:45 (inject ['tools']) + src/index.ts:379 (runtimeCtx.tools.register)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
