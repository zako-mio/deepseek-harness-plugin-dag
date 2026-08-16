# dsh-hooks-codex

- 包名: `@deepseek-ai/dsh-hooks-codex`
- 分组: G36 Hooks工具扩展
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/hooks/hooks-codex`

## 实现逻辑
Bridge 插件：在 harness 拦截 seam 上运行未修改的 Codex hooks.json。name='hooks-codex', inject=['shell']（src/index.ts:40-41）。apply 读入解析 Codex hooks.json（parseCodexConfig, :81-97），注册 5 个扩展点：agent/session-start(SessionStart, detached, :188)、agent/pre-step(UserPromptSubmit, 仅 reject 支持, :199)、tools/pre-execute(PreToolUse, 仅 deny, :225)、tools/post-execute(PostToolUse, :234)、agent/turn-stopping(Stop, :260)。Codex 方言：snake_case payload、每事件带 model、正则匹配器、无 hook 环境/命令替换、无 pre-tool approval/rewrite 路径，仅 honor 阻断决策；stop_hook_active 恒 false。共享执行/解析在 dsh-hook-protocol。

## Provides
- 5 个拦截扩展点处理（SessionStart/UserPromptSubmit/PreToolUse/PostToolUse/Stop）
- Codex 方言 payload 编解码（snake_case + model + turn_id）
- hook/invoked + hook/result session 事件对
- inject ['shell']

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - agent 类型与决策契约
  - 证据: `packages/hooks/hooks-codex/src/index.ts:18 (Agent/PreStepDecision); package.json:38 (peerDep)`
- `dsh-llm` [编译依赖] - hook 输出构造上下文
  - 证据: `packages/hooks/hooks-codex/src/index.ts:19-20 (createUserMessage/ContentBlock/MessageSource); package.json:41 (peerDep)`
- `dsh-session` [编译依赖] - session 消息类型
  - 证据: `packages/hooks/hooks-codex/src/index.ts:21 (UserMessage); package.json:42 (peerDep)`
- `dsh-tools` [编译依赖] - tool 前后决策类型
  - 证据: `packages/hooks/hooks-codex/src/index.ts:23 (PostToolDecision/PreToolDecision/ToolExecution); package.json:44 (peerDep)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
