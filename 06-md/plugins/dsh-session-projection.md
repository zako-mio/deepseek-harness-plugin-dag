# dsh-session-projection

- 包名: `@deepseek-ai/dsh-session-projection`
- 分组: G33 会话核心
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/session/session-projection`

## 实现逻辑
SessionProjectionRegistry（ctx.sessionProjections）是会话投影能力 seam 的 Service Definition 与其驱动：唯一订阅 session/created 与 session/event，把每个提交事件驱动过所有注册单元的纯同步 apply，并按 Object.is 判断状态/视图引用是否变化以触发 change feed（src/index.ts:199-223,656-704）。register() 是 effect，末位注册者退出即移除 key，并读面提供 stateOf/snapshot/cachedSnapshot/checkpoint/restoreFloor/viewCheckpoint/restore/hydrate（src/index.ts:233-595）。类型出口 types.ts 定义可合并的投影状态表与客户端视图表（src/types.ts:11-24）。

## Provides
- ctx.sessionProjections (会话投影单元注册表、驱动与快照/检查点读写面)

## Depends On (上游依赖)
- `dsh-session` [E1+E2] - 以会话日志为唯一输入驱动投影并读取 seq/header 元数据
  - 证据: `src/index.ts:22 import + src/index.ts:209,220 ctx.on session/created/session/event`

## Dependents (下游被依赖)
- `dsh-agent` - 向会话投影表声明 turnBoundary/inbox 投影条目
- `dsh-agent-instructions` - 依赖 turnBoundary 投影判断当前步是否开放，决定指令刷新是立即排队还是延迟到步结束
- `dsh-agent-loop` - 注册 turnBoundary 与 inbox 投影定义
- `dsh-agent-preset-registry` - 注册 agentPreset 投影并读取 turnBoundary 判定空会话
- `dsh-api-session-controller` - 会话投影状态与增量
- `dsh-goal` - 注册并读取 'goal' 会话投影以派生当前目标
- `dsh-hooks-claude-code` - 读取 turnBoundary 投影获取 open turn 号以记录 hook 事件
- `dsh-hooks-codex` - 读取 turnBoundary 投影获取 turn_id 以记录 hook 事件
- `dsh-llm-retry` - 注册 llmRetry projection 以在重试间保持每 provider/策略的尝试计数
- `dsh-permission-presets` - 注册 permissions 会话投影
- `dsh-plan-mode` - 注册 plan 投影并读取 plan/turnBoundary 状态
- `dsh-sandbox-policy` - 把 sandboxMode 作为投影单元注册并读取会话模式覆盖
- `dsh-session-projection-cache` - 对注册单元做 checkpoint/restore/hydrate 并查看缓存行
- `dsh-session-reference` - 从 title/subagent 投影快照派生候选的提及标签与显示标题，避免折叠整个日志
- `dsh-session-stats` - 把 sessionStats 单元注册到投影注册表并交付客户端视图
- `dsh-session-title` - 注册 title/titleInput 单元并读取 titleInput 与 turnBoundary 状态
- `dsh-session-turn-outline` - 把 turnOutline 单元注册到投影注册表并交付客户端视图
- `dsh-subagent` - 注册父目录、身份与时长投影
- `dsh-terminal-bash` - 读取 sandboxMode 投影以校验模式切换
- `dsh-time-context` - 注册并读取 timeContext 投影以驱动注入节流，且向 SessionProjectionStateMap 做类型合并
- `dsh-tmux-context` - 注册并读取 tmuxContext 投影以判断位置是否变化、是否超过刷新间隔
- `dsh-token-meter` - 注册三个投影单元并读取其在会话上的状态
- `dsh-tool-goal` - 读取 turnBoundary 投影确定开放轮的起始序列号
- `dsh-tool-present` - 读取当前 open turn 与 turn 号
- `dsh-tool-session-query` - 读取调用者会话的 turnBoundary 投影以裁剪本会话检索范围
- `dsh-tool-subagent` - 注册逐会话模型选择策略投影
- `dsh-tool-todo` - 注册 todos 投影单元
