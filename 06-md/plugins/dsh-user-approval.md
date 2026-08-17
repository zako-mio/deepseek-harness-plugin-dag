# dsh-user-approval

- 包名: `@deepseek-ai/dsh-user-approval`
- 分组: G09 审批权限
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/interaction/user-approval`

## 为什么需要它（设计初衷）
Harness 的人机审批接缝 ctx.approval：一次性权限决策经 approval/request 瀑布分发给各 answerer，默认 fail-closed（无 answerer 即拒绝）。它为工具流水线的 ask 决策和沙箱 bash 提级重试提供安全阀，模型只看到被记录的最终工具结果，审计事件仅入日志。解决'Agent 工具执行前如何获得人的一次许可'的安全性问题。

发展史：自 approval-seam 设计（2026-07-06 Agent Note）演进为渠道无关的一次性审批服务，同时用于 ACP 自动化桥的机器决策。策略仅 ask/never 两态，无 allow-always/撤销/持久授权，均列为 deferred。版本 0.1.0-rc.5。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/interaction/user-approval/README.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/interaction/user-approval/package.json

## 实现逻辑
定义 ctx.approval 审批 seam(Service 默认导出)。request() 先校验 open turn，append approval/asked 审计事件，再经 ctx.waterfall 调度 scope-targeted 'approval/request' 瀑布(fail-closed 默认 'unavailable'，'never' 策略确定性 reject，abort 得 'cancelled')，最后 append approval/decided 配对事件。setPolicy() 用 setApprovalPolicy 写 session 日志并 agent.inject 用户可见切换通知；经 ctx.inject(['systemPrompt']) 注册 'approval:policy' context 段向模型陈述当前策略。

## Provides
- ctx.approval(ApprovalService)
- approval/request 瀑布事件(Scoped)
- session 事件 approval/asked|decided|policy
- systemPrompt context 段 approval:policy
- setApprovalPolicy/effectiveApprovalPolicy/APPROVAL_POLICIES

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 携带 live agent 路由 answerer
  - 证据: `packages/interaction/user-approval/src/index.ts:10,159,230`
- `dsh-llm` [编译依赖] - createUserMessage
  - 证据: `packages/interaction/user-approval/src/index.ts:11`
- `dsh-session` [运行时依赖] - 审批审计事件与 policy 持久化
  - 证据: `packages/interaction/user-approval/src/index.ts:146,267,274`
- `dsh-system-prompt` [组合依赖] - 向模型暴露 approval policy
  - 证据: `packages/interaction/user-approval/src/index.ts:204`

## Dependents (下游被依赖)
- `dsh-host-apiproxy` - ApprovalOutcome/ApprovalRequestId
- `dsh-permission-presets` - approval 旋钮写穿
- `dsh-tool-bash` - 升级批准通道
- `dsh-tool-fs` - approveEscalation 的 approver 通道
- `dsh-tools` - ctx.get('approval') 可选 seam：ask 决策转 approval.request
