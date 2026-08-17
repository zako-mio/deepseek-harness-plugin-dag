# dsh-hooks-claude-code

- 包名: `@deepseek-ai/dsh-hooks-claude-code`
- 分组: G36 Hooks工具扩展
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/hooks/hooks-claude-code`

## 为什么需要它（设计初衷）
Claude Code hook 桥：把用户既有 hooks.json（或 settings hooks 键）映射到 harness 拦截点，只实现 shell command 钩子子集。

来源：
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/hooks/hooks-claude-code

## 实现逻辑
Bridge 插件：在 harness 拦截 seam 上运行未修改的 Claude Code hooks.json/settings hook 配置。name='hooks-claude-code', inject=['shell']（src/index.ts:39-42）。apply 时一次性读入并解析 hooks.json（readFileSync + parseClaudeCodeConfig，:101-116），注册 7 个扩展点：agent/session-start(SessionStart, detached, :206)、agent/pre-step(UserPromptSubmit→PreStepDecision, :219)、tools/pre-execute(PreToolUse→PreToolDecision, :238)、tools/post-execute(PostToolUse→PostToolDecision, :247)、agent/turn-stopping(Stop, deny 时 agent.steer 强制续跑, :270)、subagent/start(:281)、subagent/end(:291)。共享执行/解析在 dsh-hook-protocol（runHook/matchesMatcher/mergeHookOutputs/createDetachedRuns/appendHookInvoked/appendHookResult）。写 hook/invoked+hook/result session 事件对；支持 CLAUDE_PLUGIN_ROOT/CLAUDE_PROJECT_DIR 替换；updatedInput/systemMessage 仅告警不生效；hook 在 session workspace 内运行。

## Provides
- 7 个拦截扩展点处理（SessionStart/UserPromptSubmit/PreToolUse/PostToolUse/Stop/SubagentStart/SubagentStop）
- Claude Code 方言 payload 编解码（stdin JSON + exit-code 决策映射）
- hook/invoked + hook/result session 事件对
- inject ['shell']

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - agent 类型与 pre-step 决策契约
  - 证据: `packages/hooks/hooks-claude-code/src/index.ts:15 (Agent/PreStepDecision 类型); package.json:38 (peerDep)`
- `dsh-llm` [编译依赖] - hook 输出构造 UserMessage 上下文
  - 证据: `packages/hooks/hooks-claude-code/src/index.ts:16-17 (createUserMessage/ContentBlock/MessageSource); package.json:41 (peerDep)`
- `dsh-session` [编译依赖] - session 消息类型
  - 证据: `packages/hooks/hooks-claude-code/src/index.ts:18 (UserMessage 类型); package.json:42 (peerDep)`
- `dsh-subagent` [编译依赖] - subagent start/end 配对 identity
  - 证据: `packages/hooks/hooks-claude-code/src/index.ts:36 (SubagentRunId); package.json:44 (peerDep)`
- `dsh-tools` [编译依赖] - tool 前后决策类型
  - 证据: `packages/hooks/hooks-claude-code/src/index.ts:20 (PostToolDecision/PreToolDecision/ToolExecution); package.json:45 (peerDep)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
