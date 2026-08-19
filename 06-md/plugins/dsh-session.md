# dsh-session

- 包名: `@deepseek-ai/dsh-session`
- 分组: G03 核心服务
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/core/session`

## 为什么需要它（设计初衷）
解决 agent 交互历史的单一事实来源问题：以『事件溯源』(event-sourced) 追加日志 + 内存存储作为会话的唯一真实来源，LLM 消息历史从日志推导，surface 投影层支持增量推导与压缩。持久化刻意不在此实现，由订阅 session/event 的插件负责，保证可重放、可 fork、可恢复。

发展史：dsh 的核心子系统之一（architecture.md 所列 core/session，ctx 键 sessions）。模型可见的输入必须被记录（model-visible means logged），运行时不可变检查保证该约束。支持 fork/resume/transcript/telemetry 全部从此日志流推导。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/core/session/README.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-session

## 实现逻辑
事件溯源(Event-sourced)会话存储。SessionStore(ctx.sessions) 维护内存 Map 存 Session，append-only 事件日志由 Session 类持有；append() 同步通知，通过 session/created / session/event / session/flush / session/disposed 事件向外广播，持久化由外部插件订阅事件自行落盘。Session 提供 deriveMessages()(折叠 surface 派生 LLM 消息历史)、requestHeader()(折叠 request/header 事件)、prepare/enter/announce 三段式发布边界(配合 agent-loop 的复合 effect 保证拆解顺序)。

## Provides
- ctx.sessions(SessionStore)
- session/created 事件
- session/event 事件
- session/flush 事件
- session/disposed 事件
- Session 类(append/events/deriveMessages/requestHeader/surface)
- SessionPreparation
- SessionForkError
- packChunkRuns/decodeStorageRecord(存储格式)
- deepFreeze 冻结的不可变事件契约

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - import deepFreeze 冻结事件/头, Message/UserMessage 类型定义事件载荷
  - 证据: `packages/core/session/package.json:46, packages/core/session/src/index.ts:11-14`
- `dsh-typert-registry` [运行时依赖] - ctx.inject(['typert']) 注册 session 查找器(typert.lookups.register)
  - 证据: `packages/core/session/src/index.ts:798-805`

## Dependents (下游被依赖)
- `dsh-agent` - Agent 以 SessionId 为 id
- `dsh-agent-instructions` - 订阅 session/event step 判定
- `dsh-agent-loop` - ctx.sessions.prepare/enter/announce 创建会话
- `dsh-agent-presets` - peerDependencies（session/event）
- `dsh-agent-spine-demo` - ctx.plugin(SessionStore) 事件溯源会话存储
- `dsh-api-remotes` - SessionHeader/SessionEvent/SessionId 类型与 ctx.sessions.get 服务（:139）
- `dsh-client-ui-agent-preset` - 会话行 preset 折入与选中回写
- `dsh-client-ui-commands` - 每会话 popup controller 与目录键
- `dsh-client-ui-goal` - SessionEvent<'command/run'> 类型
- `dsh-client-ui-input-trigger` - 按会话 scope 解析 controller
- `dsh-client-ui-model-selection` - 会话目录键与可用性判定
- `dsh-client-ui-permission-presets` - 会话绑定与命令执行
- `dsh-client-ui-skill` - 会话身份判定与键控缓存
- `dsh-client-ui-subagent` - 子会话候选源与导航动作
- `dsh-client-ui-workflow-run` - 会话 id 类型契约
- `dsh-code-runtime-worker-thread` - snapshotJsonValue 将绑定解析结果快照为无损耗 JSON
- `dsh-command-feedback` - feedback/record 持久化
- `dsh-commands` - 命令生命周期事件持久化
- `dsh-compaction-basic` - 订阅 session/event + append compaction 事件
- `dsh-compaction-tool-result-pruner` - 读 surface.nodes + append 替换
- `dsh-cordis-host-runner` - snapshotJsonValue/JsonValue
- `dsh-experimental-agent-team` - 以Lead会话为journal基底
- `dsh-fs-observation-policy` - owner 从 actor.agent.session 派生
- `dsh-goal` - goal/change 持久化
- `dsh-goal-round-driver` - checkpoint 冲刷与 turn 边界
- `dsh-hooks-claude-code` - session 消息类型
- `dsh-hooks-codex` - session 消息类型
- `dsh-host-apiproxy` - Session/SessionEvent/SessionId 类型
- `dsh-llm-retry` - agent.session.append('llm/retry')
- `dsh-message-feedback` - deriveEventMessage/isAppendSurfaceEvent 定位目标助手消息
- `dsh-plan-mode` - plan/mode 持久化
- `dsh-repeat-tool-reminder` - UserMessage 类型
- `dsh-sandbox-local` - SessionId 会话隔离键
- `dsh-sandbox-policy` - 会话事件日志作模式折叠存储
- `dsh-schedule` - session 事件日志（提醒持久化载体）
- `dsh-sdk-client` - SessionEvent 类型
- `dsh-sdk-jsonrpc-server` - SessionId 类型
- `dsh-session-checkpoint-policy` - ctx.sessions.flush 强制持久化屏障
- `dsh-session-persistence-jsonl` - 订阅 session/created|event|flush|disposed 事件源
- `dsh-session-persistence-sqlite` - 会话事件/头类型契约与 sessions 服务注入
- `dsh-session-projection` - 订阅 session/event 驱动投影
- `dsh-session-projection-cache` - Session/SessionEvent 类型与 snapshotJsonValue
- `dsh-session-query-sqlite` - static inject sessions; observeLive
- `dsh-session-reference` - SessionId branded 类型与 SessionHeader（cwd/createdAt）契约
- `dsh-session-stats` - peerDependencies（事件类型）
- `dsh-session-telemetry-otel` - static inject sessions; feedback 校验
- `dsh-session-title` - 事件源读取/追加
- `dsh-session-title-all-prompts-llm` - 会话事件流：标题生成时机（事件驱动）
- `dsh-session-title-first-prompt-llm` - 会话服务访问
- `dsh-shell-env` - 会话 id 注入 DSH_SESSION_ID
- `dsh-spill-policy` - SessionId 类型
- `dsh-subagent` - ctx.get('sessions') 枚举子代理
- `dsh-subagent-acp` - SessionId 类型
- `dsh-subagent-claude-code` - SessionId 类型
- `dsh-subagent-codex` - SessionId 类型
- `dsh-subagent-dsh-sdk` - SessionId/SessionEvent/TurnEndReason 类型
- `dsh-subagent-fork-in-process` - parent.session.events 截取种子
- `dsh-terminal-bash` - 会话事件驱动模式围栏
- `dsh-time-context` - 扫描会话事件定位前序消息/上次注入/requestMessages
- `dsh-tmux-context` - 扫描持久事件定位上次注入状态（latestInjectedState）
- `dsh-token-meter` - 订阅 session/event；折叠 header/surface
- `dsh-tool-cordis` - JSON 值/消息类型
- `dsh-tool-fs` - 解析会话 cwd
- `dsh-tool-fs-search` - 会话 cwd 作 rg workdir
- `dsh-tool-goal` - open turn 判定
- `dsh-tool-session-query` - SessionId branded 类型与会话头（cwd）
- `dsh-tool-subagent-control` - SessionId 品牌化入参
- `dsh-tool-todo` - todo 快照持久化
- `dsh-tool-workflow` - Session.append 记录运行事件
- `dsh-tools` - snapshotJsonValue 快照工具参数
- `dsh-user-approval` - 审批审计事件与 policy 持久化
- `dsh-web-search-deepseek` - session.append 记录搜索请求
- `dsh-workflow-worker-thread` - snapshotJsonValue 序列化跨 worker
- `dsh-workspace` - SessionHeader/SessionId 类型
