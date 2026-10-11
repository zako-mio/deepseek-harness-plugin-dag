# dsh-session-projection

- 包名: `@deepseek-ai/dsh-session-projection`
- 分组: G31 会话核心
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/session/session-projection`

## 实现逻辑
定义 session-projection 能力 seam 的 Service Definition 与驱动注册表：ctx.sessionProjections 提供 register / stateOf / snapshot / cachedSnapshot / checkpoint / restoreFloor / viewCheckpoint / restore / hydrate / onChanged (src/index.ts:199-713)。注册单元用 ProjectionDefinition 描述「key + stateSchema + init + 纯同步 apply + 可选 wire.view + stateVersion」，注册即 effect 并按 key 计数共享，最后一个注销者才移除该 key (src/index.ts:48-93, src/index.ts:233-294)。服务构造时只订阅一次 session/created 与 session/event，把每个已提交事件推过全部单元（急切驱动）；只有状态引用变化才重算 client view，且仅当 Object.is 变化时通知变更订阅者 (src/index.ts:207-223, src/index.ts:657-705)。读侧给出一致切面、零 I/O 的 checkpoint 视图、以及「缓存行 + 尾部重放」的冷读与就地水合路径 (src/index.ts:339-353, src/index.ts:449-470, src/index.ts:496-596)。类型出口 SessionProjectionMap/SessionProjectionStateMap 供各域 declare-merge (src/types.ts:17-24)。

## Provides
- ctx.sessionProjections (投影注册表服务：单元注册、一致快照、变更订阅、checkpoint/restore 折叠原语)
- SessionProjectionMap / SessionProjectionStateMap (可合并扩展的客户端投影与宿主折叠状态类型表)

## Depends On (上游依赖)
- `dsh-session` [E1+E2] - 订阅会话创建与已提交事件，并按 Session 日志做折叠与补齐
  - 证据: `package.json:38 peerDep + src/index.ts:22 import SessionLogOffset/SessionSeq；src/index.ts:209 ctx.on('session/created')、src/index.ts:220 ctx.on('session/event')`

## Dependents (下游被依赖)
- `dsh-agent` - 在投影状态表中声明 turnBoundary 键，供指令注入等消费者读取步边界事实
- `dsh-agent-instructions` - 读取 turnBoundary 投影判断当前是否处于开放 step，决定触碰项是即时投影还是延迟排队
- `dsh-agent-loop` - 注册 turnBoundary 与 inbox 投影，使步边界与待处理输入可从会话日志重放
- `dsh-agent-preset-registry` - 注册 agentPreset 投影并读取 turnBoundary 以判定会话是否已开始
- `dsh-api-session-controller` - 定义并读取会话投影(含模型选择投影)
- `dsh-experimental-claude-code-mods` - $.session 的用量等派生事实读取会话投影状态
- `dsh-goal` - 把目标折叠注册为可检查点、可下发给客户端的会话投影
- `dsh-hooks-claude-code` - 从 turnBoundary 投影读取 lastTurn，给 hook/invoked 与 hook/result 事件填 turn 号
- `dsh-hooks-codex` - 从 turnBoundary 投影取 lastTurn，为 turn_id 字段与 hook 事件填当前轮次
- `dsh-llm-retry` - 重试计数必须由会话日志投影恢复，重启后不重置
- `dsh-permission-presets` - 注册 permissions 投影，供客户端读取当前生效值
- `dsh-plan-mode` - 注册 plan 投影并读取 plan/turnBoundary 折叠状态以判定是否处于开放 turn
- `dsh-sandbox-policy` - 注册并读取 sandboxMode 投影单元，作为会话级覆盖的唯一读取口
- `dsh-schedule` - 切换 preset 前用 turnBoundary 投影判定会话是否已开始首轮
- `dsh-session-projection-cache` - 由注册表提供 checkpoint/restore/viewCheckpoint/hydrate 等折叠原语
- `dsh-session-reference` - 从 title/subagent 投影快照派生候选的提及标签与显示标题，避免折叠整个日志
- `dsh-session-stats` - 把 sessionStats 单元注册到投影注册表并交付客户端视图
- `dsh-session-title` - 注册 title/titleInput 投影单元并读取其状态
- `dsh-session-turn-outline` - 把 turnOutline 单元注册到投影注册表并交付客户端视图
- `dsh-subagent` - 子代理目录/时序/身份以 session projection 形式发布
- `dsh-terminal-bash` - 读取 sandboxMode 投影的折叠状态，作为围栏比较的当前模式依据
- `dsh-time-context` - 注册并读取可重放的时间读数投影，使节流与耗时基准在恢复会话后仍然成立
- `dsh-tmux-context` - 注册并读取 tmuxContext 投影以判断位置是否变化、是否超过刷新间隔
- `dsh-token-meter` - 注册三个投影单元并读取其在会话上的状态
- `dsh-tool-goal` - 读取 turnBoundary 投影确定开放轮的起始序列号
- `dsh-tool-present` - 读取 turnBoundary 投影以确认存在打开的 turn 并取得 turn 号
- `dsh-tool-session-query` - 读取调用者会话的 turnBoundary 投影以裁剪本会话检索范围
- `dsh-tool-subagent` - 模型选择策略以 session projection 持久化
- `dsh-tool-todo` - 注册 todos 投影单元，使 UI/客户端能从 session 事件流折叠出当前待办列表
- `dsh-user-questions` - 注册 userQuestions 投影并读取 active 问题
- `dsh-working-directory` - 注册 workingDirectory 投影并读取当前提交值
