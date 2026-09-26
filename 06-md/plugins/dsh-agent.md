# dsh-agent

- 包名: `@deepseek-ai/dsh-agent`
- 分组: G09 核心运行时
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/core/agent`

## 实现逻辑
Agent 接口与注册表实现：`AgentRegistry`（服务名 `agents`）用 `Map<SessionId, AgentEntry>` 维护存活 agent，并以 `AsyncLocalStorage` 承载进程内 initiator scope，提供 `create/resume`（委派给已注册的 `AgentFactory`）、`register/enter/announce/get/list/roots` 等生命周期方法 (src/index.ts:245-283,391-416,437-559)。构造时经 `ctx.inject(['typert'])` 注册 agent 的 typert lookup/host context，并安装 workspace 归档准入监听 (src/index.ts:257-270,282)。dispatch.ts 提供 `agentCarrier/agentEvents/emitAgentEvent/assembleContextFor`，把 agent 主体与其 scope carrier 融合，保证派发作用域键与 payload.agent 不漂移 (src/dispatch.ts:94-176)。model-selection.ts 把可变模型选择耦合到 `system-prompt/assemble` 与 `agent/request` 瀑布并在路由变化时追加持久化通知 (src/model-selection.ts:81-131)；consumed-work.ts 单遍折叠会话日志判定已消费工作 (src/consumed-work.ts:69-108)；invariant.ts 校验 `agent/status` 无空转 (src/invariant.ts:15-24)。

## Provides
- ctx.agents (Agent 注册表服务：create/resume/register/enter/announce/get/list/roots 与 initiator scope)
- Agent 事件词表 (agent/created、agent/disposed、agent/status、agent/inbox/*、agent/pre-step、agent/request、agent/request-error、agent/assistant-stream、agent/turn-stopping、agent/error)
- agentEvents/agentCarrier/emitAgentEvent/assembleContextFor 融合作用域派发助手
- installModelSelection (agent 级模型选择与请求路由耦合)
- foldConsumedWork (会话日志的已消费工作折叠)
- Agent/Inbox/AgentOptions/TurnBoundaryProjection 等公共类型与声明合并

## Depends On (上游依赖)
- `dsh-invariants` [E1+E2] - 作为 invariant companion 注册 agent 生命周期不变量
  - 证据: `src/invariant.ts:4 import + src/invariant.ts:12 inject(['invariants']) + src/invariant.ts:32 register`
- `dsh-llm` [编译依赖] - 复用 LlmCallConfig/ReasoningEffortId 及 createUserMessage/boundContextSummary 生成模型切换通知
  - 证据: `src/model-selection.ts:14 import + package.json:42 peerDep`
- `dsh-scope` [E1+E2] - 用 scopeTarget/Scoped 构建 agent 作用域载体
  - 证据: `src/index.ts:12 import scopeTarget + src/dispatch.ts:10`
- `dsh-session` [编译依赖] - 复用 SessionId/SessionEvent/SessionLogOffset 会话身份与日志词汇，并依赖 agent.session 语义
  - 证据: `src/index.ts:14 import type + src/types.ts:10`
- `dsh-session-projection` [编译依赖] - 向会话投影表声明 turnBoundary/inbox 投影条目
  - 证据: `src/projection.ts:2 + src/types.ts:58 声明合并`
- `dsh-system-prompt` [编译依赖] - assembleContextFor 返回 AssembleContext，并向该类型声明合并 agent 字段
  - 证据: `src/dispatch.ts:12 import type AssembleContext + src/runtime-types.ts:17`
- `dsh-workspace` [E1+E2] - 回答 workspace/session-activity 的 turn 家族，并在 workspace/session-stop 时取消运行中的 agent
  - 证据: `src/archive-admission.ts:12 import type + src/archive-admission.ts:27,34 事件订阅`

## Dependents (下游被依赖)
- `dsh-acp` - 组合并驱动被代理 Agent，安装模型选择引用
- `dsh-agent-default-model` - 复用 Agent 侧的 ModelSelection 选择类型
- `dsh-agent-instructions` - 在 agent 步前把工作区指令上下文拼入请求消息序列，并读取 agent.session 的可见表面状态
- `dsh-agent-loop` - 实现 AgentFactory 并经 ctx.agents 工厂/注册表发布与登记 agent
- `dsh-agent-preset-registry` - 绑定并读取活动 Agent 的预设版次
- `dsh-api-account-controller` - 枚举运行中的 Agent 以判断账号任务
- `dsh-api-remotes` - waterfall 请求携带的 Agent 类型
- `dsh-api-session-controller` - Agent 创建/续跑与模型选择安装
- `dsh-api-terminal-controller` - Remote 方法以 Agent 作为 Session 所有者参数
- `dsh-client-file-upload` - 以接收 Agent 及其 session 作为上传暂存的作用域与生命周期主体
- `dsh-client-ui-chat` - agent 相关类型
- `dsh-client-ui-conversation` - agent/initiator 类型
- `dsh-client-ui-trajectory` - 引入 agent 类型用于消息定义
- `dsh-client-ui-workspace` - 引入 agent 活动类型用于归档确认
- `dsh-commands` - 命令以 agent 及其 session 为作用域与日志目标
- `dsh-compaction-basic` - 在 agent 的步边界与请求错误扩展点上挂自动压缩与溢出恢复，并借 agent.runMaintenance 预约空闲会话的手动压缩
- `dsh-compaction-image-offload` - 在 agent 请求错误扩展点上拦截图像卸载失败并返回 retry 动作，发起一次表面修复后的重试
- `dsh-cordis-host-runner` - Inspect 查询与运行请求以 Agent 为其作用域主体
- `dsh-experimental-auto-review` - 读取会话 surface、header 与 cwd 构造审查快照
- `dsh-experimental-browser-use-chrome-devtools-mcp` - 按 live Agent 建立 Session 作用域
- `dsh-experimental-browser-use-playwright-mcp` - 按 live Agent 建立 Session 作用域
- `dsh-experimental-browser-use-stagehand-native` - 按 owner Agent 隔离浏览器运行时并注入 initiator
- `dsh-experimental-tool-agent-team` - 枚举/跟踪 Agent 并在其 scope 内注册工具
- `dsh-file-reference-local` - 按 agent 维护搜索索引与提示词 fiber 生命周期，并用 agent 的会话 cwd 作为搜索根
- `dsh-goal` - 以 agent 为键持有运行时激活状态、校验 live 身份并订阅 agent/created
- `dsh-goal-round-driver` - 经 agent 生命周期/收件箱投递续轮消息并参与 pre-step 决策
- `dsh-hooks-claude-code` - 在 agent 生命周期与步进点注入上下文并映射 hook 决策
- `dsh-hooks-codex` - 在 agent 生命周期与步进点注入上下文并映射 hook 决策
- `dsh-jobs-local` - 把作业 owner 会话解析为活 Agent 实例并挂接其 scope 清理，实现按 owner 归属与生命周期取消
- `dsh-llm-retry` - 在 agent 请求错误恢复点上裁决是否重试，并把重试写入 agent.session
- `dsh-plan-mode` - 阅读并驱动 Agent 的会话与预备步决策
- `dsh-plugin-package-inventory-deepseek` - 按请求会话定位 agent，以追加其 standing preset 的活跃条目
- `dsh-repeat-tool-reminder` - 以 agent 为键维护重复链并在用户插话时重置
- `dsh-sandbox-policy` - 合并 agent 请求上下文事件类型以取到会话
- `dsh-schedule` - 把工具注册绑定到根 agent 的作用域与会话
- `dsh-sdk-jsonrpc-server` - 经 agent 工厂创建/管理 SDK 会话 agent
- `dsh-session-checkpoint-policy` - 在每步请求前持久化前一步结果
- `dsh-session-reference` - 在 agent 步前把会话引用上下文拼入直接用户消息之后
- `dsh-session-title` - 合并 agent 相关事件/上下文类型
- `dsh-subagent` - 创建与检索子 Agent、读取其会话与状态
- `dsh-subagent-dsh-sdk` - 解析并合并子代理 route 选项
- `dsh-subagent-fork-in-process` - 从父 Agent 会话日志切取 seed
- `dsh-terminal` - 以精确 Agent 作为会话 owner，并绑定其生命周期做 cleanup
- `dsh-terminal-bash` - 以会话 owner Agent 及其 session 做沙箱模式护栏
- `dsh-time-context` - 在 agent 步前注入时间上下文读数，并读取 turn/step 位置
- `dsh-tmux-context` - 在 agent 步前注入 tmux 位置上下文，并读取 turn/step 位置
- `dsh-tool-ask-user` - 工具执行携带的 agent 身份
- `dsh-tool-bash` - 读取调用者 Agent 会话以解析 workdir 与作业归属
- `dsh-tool-bash-persistent` - 以 Agent 为 owner 隔离持久 shell 并读取其会话 cwd
- `dsh-tool-cordis` - 查询需以 Agent 为其作用域主体
- `dsh-tool-goal` - 校验调用 agent 的 live 身份与 root 归属以判定人类权威
- `dsh-tool-jobs` - 把完成通知投递到 owner Agent（inject/followup）并据其 input 重置唤醒预算
- `dsh-tool-present` - 取得调用 Agent 及其 Session
- `dsh-tool-pwsh` - 读取调用者 Agent 会话以解析 workdir 与作业归属
- `dsh-tool-pwsh-persistent` - 以 Agent 为 owner 隔离持久 shell 并读取其会话 cwd
- `dsh-tool-ralph` - 声明式 peer 依赖（通过 exec.agent 取得调用方 Agent）
- `dsh-tool-session-query` - 读取调用者 Agent 会话的 header 与边界投影类型
- `dsh-tool-skill` - 订阅 agent/pre-step 注入技能正文与技能目录，并读取 agent.session 的 cwd 与事件序列
- `dsh-tool-subagent` - 读取调用 Agent 与 reconciling 组合作用域
- `dsh-tool-subagent-control` - 读取活跃 Agent 状态用于发现结果
- `dsh-tool-terminal` - 以执行 Agent 作为终端 owner
- `dsh-tool-todo` - todo 列表挂在调用 Agent 的 session 上
- `dsh-tool-workflow` - 取得调用方 Agent 以归属后台作业与工作流运行记录
- `dsh-tools` - 复用 Agent 类型以在调度中引用所属 agent
- `dsh-user-approval` - 以 agent/session 为审批作用域与日志目标
- `dsh-user-questions` - 限定只有运行时根的存活 agent 可发起人类交互
- `dsh-web-search-deepseek` - 通过 ctx.get('agents') 找到当前发起方 Agent，以记录辅助搜索请求
- `dsh-workflow-ptc` - 承载子代理的父 Agent 身份与归属
- `dsh-workspace-changes` - 在 turn 停止时收口快照
