# dsh-plan-mode

- 包名: `@deepseek-ai/dsh-plan-mode`
- 分组: G17 目标计划
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/plan/plan-mode`

## 为什么需要它（设计初衷）
per-agent 的日志化计划协作状态：/plan 命令、plan:policy 提示与 exit_plan_mode 退出。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/plan/plan-mode/README.md

## 实现逻辑
定义 ctx.planMode PlanModeController。状态由 session 日志 'plan/mode' 折叠；agent/pre-step 接受后 onBoundary append 待定选择；systemPrompt.section('plan:policy') 渲染部署指导；/plan 命令与 exit_plan_mode 工具(经 userQuestions.ask 做 plan-review，approve 则 pendingIntents 置 false)；'plan' session projection 由 command/run+plan/mode 双事件折叠。

## Provides
- ctx.planMode
- session 事件 plan/mode
- plan session projection
- /plan 命令
- ctx.tools: exit_plan_mode
- systemPrompt section plan:policy

## Depends On (上游依赖)
- `dsh-commands` [组合依赖] - /plan 命令
  - 证据: `packages/plan/plan-mode/src/index.ts:269`
- `dsh-session` [运行时依赖] - plan/mode 持久化
  - 证据: `packages/plan/plan-mode/src/index.ts:53,440,456`
- `dsh-session-projection` [组合依赖] - plan 投影单元
  - 证据: `packages/plan/plan-mode/src/index.ts:244`
- `dsh-system-prompt` [组合依赖] - plan:policy 段
  - 证据: `packages/plan/plan-mode/src/index.ts:33,225`
- `dsh-tools` [组合依赖] - exit_plan_mode 工具注册
  - 证据: `packages/plan/plan-mode/src/index.ts:32,185,305`
- `dsh-user-questions` [组合依赖] - exit 前计划评审
  - 证据: `packages/plan/plan-mode/src/index.ts:34,330`

## Dependents (下游被依赖)
- `dsh-client-ui-plan` - plan 投影会话值决定 chip 显隐（web 下 plan-mode 被 disabled 仍取投影）
