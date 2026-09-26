# dsh-plan-mode

- 包名: `@deepseek-ai/dsh-plan-mode`
- 分组: G26 规划模式
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/plan/plan-mode`

## 实现逻辑
PlanModeController 注册 `plan` 会话投影，折叠 command/run、command/done、plan/mode、request/header 事件以还原模式状态与待选意图（src/index.ts:137-169）。用户切换经 pendingIntents 暂存，仅在下一个被接受的 in-turn agent/pre-step 里 append plan/mode 并附模式切换叙述（src/index.ts:197-214、:419-454）。服务同时注册仅激活时渲染的 plan:policy 提示段（src/index.ts:217-225）、条件注入的 /plan on|off 命令（src/index.ts:230-276）与常驻 exit_plan_mode 工具——后者经 userQuestions 呈现计划评审，批准则排队退出（src/index.ts:278-366）。invariant.ts 校验 plan/mode 的 active 必须是布尔（src/invariant.ts:20-49）。

## Provides
- ctx.planMode (日志化计划协作状态控制器，src/index.ts:59-61、:176-469)
- sessionProjections `plan` 投影（cropped {active,pending}，src/index.ts:227、:137-169）
- ctx.tools 的 `exit_plan_mode` 工具（提交计划供用户评审，src/index.ts:278-366）
- ctx.commands 的 `/plan` 命令（on/off 与消息附带，条件注册，src/index.ts:230-276）
- systemPrompt `plan:policy` 段（部署自有计划指导，仅激活时渲染，src/index.ts:217-225）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 阅读并驱动 Agent 的会话与预备步决策
  - 证据: `src/index.ts:29 type import Agent/PreStepDecision + src/index.ts:202 agent.session`
- `dsh-commands` [E1+E2] - 注册 /plan 命令并关联命令生命周期事件
  - 证据: `src/index.ts:35 type import CommandDefinitionId + src/types.ts:11 CommandId + src/index.ts:230 ctx.inject(['commands'])`
- `dsh-invariants` [E1+E2] - 注册 plan/mode 载荷校验不变式
  - 证据: `src/invariant.ts:5 type InvariantInstaller + src/invariant.ts:49 ctx.invariants.register`
- `dsh-llm` [编译依赖] - 构造模式切换的用户叙述消息
  - 证据: `src/index.ts:30 import createUserMessage + src/index.ts:31 type ContextFormed`
- `dsh-session` [编译依赖] - 追加 plan/mode 事件供投影折叠与恢复
  - 证据: `src/index.ts:32 type Session/UserMessage + src/invariant.ts:4 + src/index.ts:434 session.append('plan/mode')`
- `dsh-session-projection` [E1+E2] - 注册 plan 投影并读取 plan/turnBoundary 状态
  - 证据: `src/index.ts:36-37 type import ProjectionDefinition + src/index.ts:227 ctx.sessionProjections.register + src/index.ts:374 stateOf`
- `dsh-tools` [E1+E2] - 注册常驻的 exit_plan_mode 工具
  - 证据: `src/index.ts:33 import defineTool + src/index.ts:177 inject 'tools' + src/index.ts:278 ctx.tools.register`
- `dsh-user-questions` [E1+E2] - 呈现计划评审问答通道
  - 证据: `src/index.ts:34 import UserQuestionError + src/index.ts:303 ctx.get('userQuestions')`

## Dependents (下游被依赖)
- `dsh-client-ui-conversation` - 计划模式输入提示
- `dsh-client-ui-plan` - 引入 plan SessionProjectionMap 声明以使用投影
