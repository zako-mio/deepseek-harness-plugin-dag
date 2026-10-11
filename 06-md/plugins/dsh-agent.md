# dsh-agent

- 包名: `@deepseek-ai/dsh-agent`
- 分组: G09 核心运行时
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/core/agent`

## 实现逻辑
提供 Agent 能力 seam 与事件词汇。AgentRegistry（ctx.agents）以 Map 维护活跃 agent 条目，用 AsyncLocalStorage 承载进程内 initiator 作用域，并通过 setFactory 把「创建/恢复」委派给由 loop 插件实现的 AgentFactory（src/index.ts:245-283、src/index.ts:358-374、src/index.ts:391-416）。register/enter/announce 组成可回滚的发布事务：enter 校验 agent.id 与 session.id 一致、以 scopeTarget(agent, agent) 作为事件载体，announce 串行派发 agent/created 并在 detach 请求时配对 agent/disposed（src/index.ts:459-494、src/index.ts:537-559）。dispatch.ts 的 agentEvents 把 agent 主体与作用域载体融合，使事件 subject 与 scope key 不可能漂移（src/dispatch.ts:107-149）；archive-admission 用 workspace/session-activity 与 workspace/session-stop 回答「该 Session 是否仍在 turn 中」并支持归档时取消（src/archive-admission.ts:26-38）。

## Provides
- ctx.agents（活跃 agent 注册表与 initiator 作用域，src/index.ts:245-283）
- agent 事件词汇：agent/created、agent/disposed、agent/status、agent/inbox/inserted|claimed|discarded、agent/pre-step、agent/request、agent/request-error、agent/assistant-stream、agent/turn-stopping、agent/error（src/runtime-types.ts:246-393）
- AgentFactory 接口（agent 创建/恢复的工厂 seam，src/index.ts:171-203）
- sessionProjections 'turnBoundary' 投影键声明（src/projection.ts:4-9）
- agent 作用域事件分发助手 agentCarrier/agentEvents/emitAgentEvent/assembleContextFor（src/dispatch.ts:94、src/dispatch.ts:107、src/dispatch.ts:158、src/dispatch.ts:174）
- 会话活动类型扩展点 SessionActivityKindMap 与 Inbox 契约（src/types.ts:21-27、src/runtime-types.ts:48-107）

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 复用 LLM 的消息、工具调用与模型选择类型，使 agent 选项与请求配置对齐
  - 证据: `src/types.ts:7 import type ... from '@deepseek-ai/dsh-llm/types' + src/model-selection.ts:14 import ... from '@deepseek-ai/dsh-llm'`
- `dsh-session` [E1+E2] - 共享 agent/session 同一身份，并在注册边界校验会话事件与序号类型
  - 证据: `src/index.ts:14 import type { SessionEvent, SessionId, SessionLogOffset } + src/index.ts:461 if (id !== agent.session.id) throw new Error(...)`
- `dsh-session-projection` [编译依赖] - 在投影状态表中声明 turnBoundary 键，供指令注入等消费者读取步边界事实
  - 证据: `src/projection.ts:2 import type {} from '@deepseek-ai/dsh-session-projection' + src/projection.ts:4 declare module '@deepseek-ai/dsh-session-projection/types'`
- `dsh-system-prompt` [编译依赖] - 组装提示时同时带上 agent 与 scope，避免 agent 作用域贡献被静默遗漏
  - 证据: `src/dispatch.ts:12 import type { AssembleContext } + src/dispatch.ts:174 export function assembleContextFor(agent, signal)`
- `dsh-workspace` [E1+E2] - 回答 Workspace 归档准入的 turn 家族活动，并在归档时按用户停下的方式取消该 turn
  - 证据: `src/archive-admission.ts:12 import type { SessionActivity } from '@deepseek-ai/dsh-workspace' + src/archive-admission.ts:27 ctx.on('workspace/session-activity', ...)`

## Dependents (下游被依赖)
- `dsh-acp` - 创建/恢复被 ACP 驱动的 Agent，并订阅 agent/* 事件维护会话记录
- `dsh-agent-default-model` - 复用 Agent 侧的 ModelSelection 选择类型
- `dsh-agent-instructions` - 在工作区指令投影里读写 agent 的 inbox 与 pre-step 决策，指令才能折进本步消息批次
- `dsh-agent-loop` - 实现 AgentFactory 并向 agents 注册表登记，同时复用其 agent 事件与 inbox 契约驱动生命周期
- `dsh-agent-preset-registry` - 把 preset 选择与绑定作用到具体 Agent 的上下文与会话
- `dsh-api-account-controller` - 枚举运行中的 Agent 以判断账号任务
- `dsh-api-remotes` - 声明 waterfall 事件必须直携的 Agent 载体类型
- `dsh-api-session-controller` - 激活/恢复 Session 的 Agent 并读取其状态
- `dsh-api-terminal-controller` - 以 Agent 作为 Session 所有者参数与执行环境选择器
- `dsh-client-file-upload` - 以 Agent/Session 归属上传并校验其在落盘后仍存活
- `dsh-client-ui-chat` - Agent 类型
- `dsh-client-ui-conversation` - Agent 类型
- `dsh-client-ui-tool` - 问题行的待答状态类型来自 agent
- `dsh-client-ui-trajectory` - 消息节点读取 agent 侧事件类型
- `dsh-client-ui-user-questions` - 读取 agent 侧待答信箱状态
- `dsh-client-ui-workspace` - 归档前判定会话活动状态
- `dsh-commands` - Agent 既是命令作用域键也是命令的接收者
- `dsh-compaction-basic` - 在 agent 的步边界与请求错误扩展点上挂自动压缩与溢出恢复，并借 agent.runMaintenance 预约空闲会话的手动压缩
- `dsh-compaction-image-offload` - 在 agent 请求错误扩展点上拦截图像卸载失败并返回 retry 动作，发起一次表面修复后的重试
- `dsh-cordis-host-runner` - 以发起 Agent 的 Session 作为插件归属与权限边界，并向运行失败上报目标 Agent
- `dsh-experimental-auto-review` - 审查绑定与 agent 作用域类型来自 agent 包
- `dsh-experimental-browser-use-chrome-devtools-mcp` - 每个存活 Session 一个 MCP 进程，需要 agents 注册表
- `dsh-experimental-browser-use-playwright-mcp` - 每个存活 Session 一个 MCP 进程，需要 agents 注册表
- `dsh-experimental-browser-use-stagehand-native` - 按 owner Agent 隔离浏览器运行时并注入 initiator
- `dsh-experimental-claude-code-mods` - mod 事件以 Agent 生命周期与 pre-step 为触发点，绑定对象是 Agent
- `dsh-experimental-tool-agent-team` - 工具按 Agent 作用域安装，并随 Agent 生命周期增删
- `dsh-file-reference-local` - 按 agent 维度维护搜索缓存与提示 fiber，并在 agent/created、agent/disposed 上挂载与回收
- `dsh-goal` - 按 Agent 作用域发出目标变更事件，并用 agents 注册表校验 Agent 是否为存活实例
- `dsh-goal-round-driver` - 在 Agent 生命周期与 inbox 事件上调度轮次，并在 pre-step 处做准入裁决
- `dsh-hooks-claude-code` - 订阅 Agent 生命周期与 pre-step/turn-stopping 拦截点，并用 Agent 身份注入上下文、读取会话与 steer 续跑
- `dsh-hooks-codex` - 订阅 Agent 生命周期与 pre-step/turn-stopping 拦截点，注入上下文并在 Stop 钩子阻塞时 steer 续跑
- `dsh-jobs-local` - 把作业 owner 会话解析为活 Agent 实例并挂接其 scope 清理，实现按 owner 归属与生命周期取消
- `dsh-llm-retry` - 重试策略挂在 agent 循环的请求错误恢复扩展点上
- `dsh-plan-mode` - 在 agent 的 pre-step 边界提交计划模式选择并注入旁白消息
- `dsh-plugin-package-inventory-deepseek` - 按请求 session 定位所属 agent，进而读取其 preset 组合
- `dsh-repeat-tool-reminder` - 以 agent 为键维护重复链并在用户插话时重置
- `dsh-sandbox-policy` - 提示词上下文按 agent 取会话，从而解析该 agent 的策略
- `dsh-schedule` - 按会话查活跃 Agent 以判定委派深度，决定是否拒绝绑定
- `dsh-sdk-jsonrpc-server` - 创建 SDK 拥有的 agent 会话并在每次投递前校验句柄仍存活
- `dsh-session-checkpoint-policy` - 在每步请求前持久化前一步结果
- `dsh-session-reference` - 在 agent 步前把会话引用上下文拼入直接用户消息之后
- `dsh-session-title` - 合并 agent 侧投影类型声明
- `dsh-subagent` - 子代理就是 Agent 实体，管理器绑定在 Agent 注册表上
- `dsh-subagent-acp` - ResolvedSubagentStartRequest.parent 为 Agent 类型
- `dsh-subagent-dsh-sdk` - 解析子路由 agentOptions 并读取父会话 origin 目录
- `dsh-subagent-fork-in-process` - 以 Agent 为父级读取其会话历史
- `dsh-terminal` - 以精确 Agent 作为会话 owner，并绑定其生命周期做 cleanup
- `dsh-terminal-bash` - 后端以 Agent 为 owner 单位持有会话与围栏状态（sandboxModeFences 以 Agent 为键）
- `dsh-time-context` - 通过 agents 服务在 pre-step 瀑布上注入时间上下文，并复用其 PreStepDecision 契约
- `dsh-tmux-context` - 在 agent 步前注入 tmux 位置上下文，并读取 turn/step 位置
- `dsh-tool-ask-user` - 把调用 agent 作为问答请求的归属与作用域
- `dsh-tool-bash` - 调用归属（exec.agent）与会话身份来自 agent 包类型
- `dsh-tool-bash-persistent` - 以 Agent 作为会话所有者（owner 隔离与清理）
- `dsh-tool-cordis` - 从工具执行上下文取得 Agent，巡检结果按该 Agent 的作用域收敛
- `dsh-tool-goal` - 校验调用 agent 的 live 身份与 root 归属以判定人类权威
- `dsh-tool-jobs` - 把完成通知投递到 owner Agent（inject/followup）并据其 input 重置唤醒预算
- `dsh-tool-present` - 工具执行信封的 agent 载体类型来自 agent 包
- `dsh-tool-pwsh` - 调用归属与会话身份来自 agent 包类型
- `dsh-tool-pwsh-persistent` - 以 Agent 作为会话所有者
- `dsh-tool-ralph` - 声明式 peer 依赖（通过 exec.agent 取得调用方 Agent）
- `dsh-tool-schedule` - 以 Agent 类型标注调用者参数；仅编译期类型依赖，运行期经 exec.agent 取得
- `dsh-tool-session-query` - 读取调用者 Agent 会话的 header 与边界投影类型
- `dsh-tool-skill` - 以 Agent 为 scope 键做分层查找并挂载 pre-step 注入
- `dsh-tool-subagent` - 委托需要精确的活跃父 Agent 与父子路由继承
- `dsh-tool-subagent-control` - 读取活跃 Agent 状态以区分 running/inactive
- `dsh-tool-terminal` - 从工具执行上下文取得发起 Agent 作为终端会话的 owner 身份
- `dsh-tool-todo` - 待办清单是 per-agent-session 状态，需要 Agent 身份来定位归属会话
- `dsh-tool-workflow` - 工具以调用方 Agent 为 parent 归置子 agent 与 job owner，非 Agent 调用直接拒绝
- `dsh-tools` - 把调用方 agent 作为工具执行的主体，用于作用域解析、审批路由与 PTC 工作目录归属
- `dsh-user-approval` - 审批请求以 Agent 为路由键与审计归属，切换通知注入该 agent
- `dsh-user-questions` - 以 Agent 注册表判定调用方是否为可交互的存活 runtime root
- `dsh-web-search-deepseek` - 从当前发起者会话读取 request context 的 provider，决定是否走账号令牌路径；并作为事件记录归属
- `dsh-workflow-ptc` - 运行以父 Agent 为归属，子 agent 与工作目录均挂在该 Agent 上
- `dsh-working-directory` - 对传入的 Agent 及其会话、fiber 生效
- `dsh-workspace-changes` - turn 收尾钩子用于在 turn 结束前把捕获结果落定
