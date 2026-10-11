# dsh-hooks-claude-code

- 包名: `@deepseek-ai/dsh-hooks-claude-code`
- 分组: G13 实验特性
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/experimental/hooks-claude-code`

## 实现逻辑
以「配置解析 + 事件桥接」实现：load 时读 configPath 的 JSON，用 parseClaudeCodeConfig 把 Claude Code 的 event→matcher-group 格式解析成共享 MatcherGroup（只跑 command 钩子，非 command 记入 skipped 并 warn），并对 ${CLAUDE_PLUGIN_ROOT}/${CLAUDE_PROJECT_DIR} 做替换 (src/config.ts:78-122, src/index.ts:109-122)。随后在 agent/created、agent/pre-step、tools/pre-execute、tools/post-execute、agent/turn-stopping、subagent/start、subagent/end 七个扩展点注册监听，用 runPoint 以 CC 方言 payload 跑钩子并把结果折叠成各扩展点的决策 (src/index.ts:143-193, src/index.ts:209-303)。钩子进程经 ctx.shell 执行、工作目录经 ctx.workingDirectory 解析，钩子调用/结果对经 appendHookInvoked/appendHookResult 落进会话日志 (src/index.ts:152-158, src/index.ts:163-189)。

## Provides

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 订阅 Agent 生命周期与 pre-step/turn-stopping 拦截点，并用 Agent 身份注入上下文、读取会话与 steer 续跑
  - 证据: `package.json:33 peerDep + src/index.ts:15 import Agent/PreStepDecision/TurnBoundaryProjection + src/index.ts:209/225/276 监听 agent/created、agent/pre-step、agent/turn-stopping`
- `dsh-llm` [编译依赖] - 构造携带 hooks-claude-code 来源标记的用户消息，把钩子 additionalContext 注入模型上下文
  - 证据: `package.json:35 peerDep + src/index.ts:17 import createUserMessage + src/index.ts:25 import ContentBlock/MessageSource`
- `dsh-session` [编译依赖] - 为注入的上下文消息与 appendHook* 调用提供会话侧类型
  - 证据: `package.json:36 peerDep + src/index.ts:26 import UserMessage`
- `dsh-session-projection` [E1+E2] - 从 turnBoundary 投影读取 lastTurn，给 hook/invoked 与 hook/result 事件填 turn 号
  - 证据: `package.json:40 peerDep + src/index.ts:16 type import + src/index.ts:48 inject 'sessionProjections' + src/index.ts:320 ctx.sessionProjections.stateOf`
- `dsh-subagent` [E1+E2] - 在子 Agent 起止边沿触发 SubagentStart/SubagentStop 钩子，并按 runId 保留子 Agent 以取得其工作目录
  - 证据: `package.json:37 peerDep + src/index.ts:42 import SubagentRunId + src/index.ts:287/297 监听 subagent/start、subagent/end`
- `dsh-tools` [E1+E2] - 在工具执行前后拦截点把钩子结果映射成 deny/ask/block 决策与 additionalContexts
  - 证据: `package.json:38 peerDep + src/index.ts:27 import PreToolDecision/PostToolDecision/ToolExecution + src/index.ts:244/253 监听 tools/pre-execute、tools/post-execute`
- `dsh-working-directory` [E1+E2] - 解析会话工作目录，作为钩子进程的 cwd 与默认 CLAUDE_PROJECT_DIR
  - 证据: `package.json:41 peerDep + src/index.ts:11 type import + src/index.ts:48 inject 'workingDirectory' + src/index.ts:153-154 ctx.workingDirectory.get/ensure`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
