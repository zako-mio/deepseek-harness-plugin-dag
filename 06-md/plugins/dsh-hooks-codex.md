# dsh-hooks-codex

- 包名: `@deepseek-ai/dsh-hooks-codex`
- 分组: G19 Hooks 扩展
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/hooks/hooks-codex`

## 实现逻辑
把未改动的 Codex command hooks 桥接到 harness：SessionStart、UserPromptSubmit、PreToolUse/PostToolUse、Stop，仅同步 command 类型、正则匹配、snake_case payload 且 stdin 无尾换行（src/index.ts:119-176, 152）。config.ts 解析 Codex 五事件子集，跳过非 command 与 async hooks，并对非法 matcher 抛 SyntaxError（src/config.ts:43-85）。决策映射只保留阻断路径：工具与生命周期拦截点分别映射为 PreToolDecision/PostToolDecision 与 PreStepDecision（src/index.ts:191-276）。

## Provides
- Codex hooks 桥 (SessionStart/UserPromptSubmit/Pre+PostToolUse/Stop 到 harness 拦截点的决策映射)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 在 agent 生命周期与步进点注入上下文并映射 hook 决策
  - 证据: `src/index.ts:17 import (Agent, PreStepDecision) + src/index.ts:191 ctx.on('agent/created') + src/index.ts:205 ctx.on('agent/pre-step')`
- `dsh-hook-protocol` [E1+E2] - 复用共享的 hook 执行/解析/合并/持久事件与 matcher 校验
  - 证据: `src/index.ts:30-42 import (runHook, mergeHookOutputs, appendHookInvoked, ...) + src/index.ts:147 runHook(...) + src/config.ts:8 import matcherDiagnostic`
- `dsh-llm` [编译依赖] - 构造注入模型的上下文消息及其来源标签
  - 证据: `src/index.ts:19-20 import (createUserMessage, ContextFormed) + src/index.ts:27 import (ContentBlock, MessageSource)`
- `dsh-session` [编译依赖] - hook 上下文消息使用的会话消息类型
  - 证据: `src/index.ts:28 import UserMessage`
- `dsh-session-projection` [E1+E2] - 读取 turnBoundary 投影获取 turn_id 以记录 hook 事件
  - 证据: `src/index.ts:18 import type {} + src/index.ts:288 ctx.sessionProjections.stateOf(agent.session,'turnBoundary')`
- `dsh-tools` [E1+E2] - 在工具执行前后拦截点运行 hook 并映射为工具决策
  - 证据: `src/index.ts:29 import (PostToolDecision, PreToolDecision, ToolExecution, ToolExecutionResult) + src/index.ts:231 ctx.on('tools/pre-execute') + src/index.ts:240 ctx.on('tools/post-execute')`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
