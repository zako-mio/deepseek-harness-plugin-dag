# dsh-plan-mode

- 包名: `@deepseek-ai/dsh-plan-mode`
- 分组: G25 规划模式
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/plan/plan-mode`

## 实现逻辑
以 default 导出的 PlanModeController（extends Service，static inject=['tools','systemPrompt','sessionProjections']）实现 ctx.planMode，把 plan mode 当作「按 agent 记录的协作状态」：注册 key='plan' 的 session projection，从 command/run → command/done → plan/mode → request/header 事件折叠出 active/wanted/activeAtLastHeader，并对外只暴露 {active,pending} 的 wire 视图 (src/index.ts:136-168、src/index.ts:226)。在 agent/pre-step 上把待生效选择追加为 plan/mode 事件（仅当该 pre-step 被接受），并在必要时追加一条「用户已切换模式」的旁白消息，从而保证同一 turn 内请求装配一致 (src/index.ts:196-213、src/index.ts:448-474)。进入/退出有两条路径：ctx.inject(['commands']) 下注册的 /plan [off|message] 斜杠命令，以及常驻注册的 exit_plan_mode 工具——后者经 ctx.get('userQuestions') 发起 plan-review 提问，用户驳回时结束本 turn 而保持计划模式 (src/index.ts:229-275、src/index.ts:277-372)。plan:policy 提示词节按投影/待生效状态决定是否注入部署方指引，非计划模式注入空串 (src/index.ts:216-224)。

## Provides
- ctx.planMode (PlanModeController：按 agent 的计划模式状态、切换入口与状态读取的唯一所有者)
- session projection 'plan' (stateVersion 3 的折叠单元与 {active,pending} wire 视图)
- session 事件 'plan/mode' (log-only、整值替换的计划模式事实，驱动投影与恢复/分叉)
- tools.exit_plan_mode (模型可见的退出计划模式工具，非计划模式下仍常驻以稳定工具目录)
- commands.plan (/plan [off|message] 斜杠命令，含附件与 steering 消息)
- systemPrompt 章节 plan:policy (仅在计划模式生效时注入的部署方指引)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 在 agent 的 pre-step 边界提交计划模式选择并注入旁白消息
  - 证据: `package.json:39 peerDep + src/index.ts:28 type import Agent/PreStepDecision；src/index.ts:196 ctx.on('agent/pre-step')、src/index.ts:259 agent.steer`
- `dsh-commands` [E1+E2+E3] - 注册 /plan 斜杠命令；命令子插件仅在命令注册表被组合时激活
  - 证据: `package.json:40 peerDep(optional, package.json:49-53) + src/index.ts:34 type import、src/types.ts:11 type import CommandId；src/index.ts:229 ctx.inject(['commands'])；packages/bundle/base/cordis.patch.yml:312-313 与 :327-328 同 bundle 装配`
- `dsh-llm` [编译依赖] - 构造模式切换旁白消息并声明 plan-mode 消息来源映射
  - 证据: `package.json:41 peerDep + src/index.ts:29 import createUserMessage、src/index.ts:30 type import ContextFormed；src/index.ts:469 createUserMessage`
- `dsh-session` [E1+E2] - 把模式切换写入会话日志，使恢复与分叉重建同一状态
  - 证据: `package.json:42 peerDep + src/index.ts:31 type import Session/UserMessage；src/index.ts:440 与 src/index.ts:456 session.append('plan/mode')`
- `dsh-session-projection` [E1+E2] - 注册 plan 投影并读取 plan/turnBoundary 折叠状态以判定是否处于开放 turn
  - 证据: `package.json:43 peerDep + src/index.ts:35-36 type import ProjectionDefinition；src/index.ts:176 inject 'sessionProjections'、src/index.ts:226 register、src/index.ts:380 与 src/index.ts:391 stateOf`
- `dsh-system-prompt` [运行时依赖] - 注册 plan:policy 提示词节，按状态决定是否输出部署方指引
  - 证据: `package.json:44 peerDep + src/index.ts:176 inject 'systemPrompt'；src/index.ts:216 ctx.systemPrompt.section`
- `dsh-tools` [E1+E2] - 注册常驻的 exit_plan_mode 工具，保持跨模式工具目录不变
  - 证据: `package.json:45 peerDep + src/index.ts:32 import defineTool；src/index.ts:176 inject 'tools'、src/index.ts:277 ctx.tools.register`
- `dsh-user-questions` [E1+E2] - exit_plan_mode 经用户问答通道发起计划评审，并区分「被驳回」与失败
  - 证据: `package.json:46 peerDep + src/index.ts:33 import UserQuestionError/AskUserQuestionAnswer；src/index.ts:307 ctx.get('userQuestions')、src/index.ts:313 interaction.ask`

## Dependents (下游被依赖)
- `dsh-client-ui-conversation` - 计划模式投影类型
- `dsh-client-ui-plan` - 复用 plan 投影键类型
