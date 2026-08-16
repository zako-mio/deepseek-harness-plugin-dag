# dsh-tmux-context

- 包名: `@deepseek-ai/dsh-tmux-context`
- 分组: G34 Web上下文扩展
- 拓扑层: Layer 3
- 来源层: L3 其余
- 源码路径: `packages/context/tmux-context`

## 实现逻辑
opt-in tmux 位置上下文插件：apply() 注册 prepend 的 'agent/pre-step' 监听器（inject ['agents']），仅 step===1（每 turn 首次请求）通过 ctx.shell（ShellExecutor）运行只读命令拉取 tmux 状态。queryTmuxLocation() 组合 bash 脚本：TMUX_PANE 存在校验 → ps -o tty= 取本进程控制终端 → tmux display-message 取 #{pane_tty} → 两者相等才继续（防止从 tmux 祖先继承 $TMUX/$TMUX_PANE 的 VS Code 集成终端误判）→ exec tmux display-message 输出 tab 分隔的 8 字段（session/window/pane/layout/active）。仅当渲染状态（renderState，不含 volatile turn 前缀）相比上次注入变化时重注入，refreshIntervalMs 为注入下限（latestInjectedState 从 raw durable 事件扫描，跨 compaction/恢复存活）；executor 拒绝/查询失败是 no-op 仅 warn，绝不使 turn 失败。注入为 source.kind='plugin' form='snapshot' 的 UserMessage。

## Provides
- agent/pre-step prepend 监听器（step=1 注入 tmux 位置快照）
- tmux 位置上下文（session/window/pane/layout + active 标志 + tty 真伪校验）
- 状态变化驱动的重注入 + refreshIntervalMs 下限
- source.kind='plugin' form='snapshot' 会话事件写入

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - agent/pre-step 事件词表与 PreStepDecision 注入契约
  - 证据: `packages/context/tmux-context/src/index.ts:23 Agent/PreStepDecision 类型；218 ctx.on('agent/pre-step')；package.json:38`
- `dsh-llm` [编译依赖] - 构造注入的 UserMessage 载荷
  - 证据: `packages/context/tmux-context/src/index.ts:25 createUserMessage`
- `dsh-session` [编译依赖] - 扫描持久事件定位上次注入状态（latestInjectedState）
  - 证据: `packages/context/tmux-context/src/index.ts:182 agent.session.events 扫描 + package.json:41`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
