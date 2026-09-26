# dsh-hooks-claude-code

- 包名: `@deepseek-ai/dsh-hooks-claude-code`
- 分组: G19 Hooks 扩展
- 拓扑层: Layer 7
- 来源层: L3 其余
- 源码路径: `packages/hooks/hooks-claude-code`

## 实现逻辑
把未改动的 Claude Code command hooks 桥接到 harness 拦截点：SessionStart、UserPromptSubmit、PreToolUse/PostToolUse、Stop、SubagentStart/Stop（src/index.ts:209-301）。config.ts 解析 CC 的 event→matcher-group 格式，仅保留 command 类型并对命令做 ${CLAUDE_PLUGIN_ROOT}/${CLAUDE_PROJECT_DIR} 替换（src/config.ts:78-122）。runPoint 对每个匹配 hook 记录 invoked/result 事件并调用 runHook，最后把合并结果映射为 PreStepDecision/PreToolDecision/PostToolDecision（src/index.ts:143-192, 225-271）。

## Provides
- Claude Code hooks 桥 (SessionStart/UserPromptSubmit/Pre+PostToolUse/Stop/SubagentStart+Stop 到 harness 拦截点的决策映射)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 在 agent 生命周期与步进点注入上下文并映射 hook 决策
  - 证据: `src/index.ts:14 import (Agent, PreStepDecision, TurnBoundaryProjection) + src/index.ts:209 ctx.on('agent/created') + src/index.ts:214 agent.inject`
- `dsh-hook-protocol` [E1+E2] - 复用共享的 hook 执行/解析/合并/持久事件与 matcher 校验
  - 证据: `src/index.ts:27-39 import (runHook, mergeHookOutputs, appendHookInvoked, ...) + src/index.ts:169 runHook(...) + src/config.ts:9 import matcherDiagnostic`
- `dsh-llm` [编译依赖] - 构造注入模型的上下文消息及其来源标签
  - 证据: `src/index.ts:16-17 import (createUserMessage, ContextFormed) + src/index.ts:24 import (ContentBlock, MessageSource)`
- `dsh-session` [编译依赖] - hook 上下文消息使用的会话消息类型
  - 证据: `src/index.ts:25 import UserMessage`
- `dsh-session-projection` [E1+E2] - 读取 turnBoundary 投影获取 open turn 号以记录 hook 事件
  - 证据: `src/index.ts:15 import type {} + src/index.ts:318 ctx.sessionProjections.stateOf(agent.session,'turnBoundary')`
- `dsh-subagent` [E1+E2] - 把子代理 start/end 映射到 SubagentStart/SubagentStop hook
  - 证据: `src/index.ts:42 import SubagentRunId + src/index.ts:287 ctx.on('subagent/start') + src/index.ts:297 ctx.on('subagent/end')`
- `dsh-tools` [E1+E2] - 在工具执行前后拦截点运行 hook 并映射为工具决策
  - 证据: `src/index.ts:26 import (PostToolDecision, PreToolDecision, ToolExecution, ToolExecutionResult) + src/index.ts:244 ctx.on('tools/pre-execute') + src/index.ts:253 ctx.on('tools/post-execute')`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
