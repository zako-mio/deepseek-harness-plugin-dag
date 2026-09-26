# dsh-tmux-context

- 包名: `@deepseek-ai/dsh-tmux-context`
- 分组: G08 上下文注入
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/context/tmux-context`

## 实现逻辑
可选的 tmux 位置上下文：在 turn 的首个请求(step===1)时经 ctx.shell 执行一次 tmux display-message，并通过比对 pane 的 pane_tty 与本进程控制终端来确认真正运行于该 pane（避免继承 $TMUX_PANE 的假阳），失败/不在 tmux/无 shell 时静默 no-op（src/index.ts:120-168、src/index.ts:246-274）。渲染出的读数含稳定的 location 状态块；注册 tmuxContext 投影记录上次注入状态，仅在状态变化且超过可选 refreshIntervalMs 时才重新注入（src/index.ts:175-186、src/index.ts:230-263）。

## Provides
- session projection 'tmuxContext' (持久化最近一次 tmux 位置读数，供变更抑制复用)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 在 agent 步前注入 tmux 位置上下文，并读取 turn/step 位置
  - 证据: `src/index.ts:24 import type PreStepDecision + src/index.ts:246 ctx.on('agent/pre-step', {prepend:true})`
- `dsh-llm` [编译依赖] - 构造带来源标记的 tmux 位置快照 user 消息，并复用消息来源合并类型
  - 证据: `src/index.ts:27 import createUserMessage + src/index.ts:28 import type ContextFormed`
- `dsh-session-projection` [E1+E2] - 注册并读取 tmuxContext 投影以判断位置是否变化、是否超过刷新间隔
  - 证据: `src/index.ts:25 type-only import + src/index.ts:44 inject ['agents','sessionProjections'] + src/index.ts:230 ctx.sessionProjections.register + src/index.ts:254 ctx.sessionProjections.stateOf`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
