# dsh-user-approval

- 包名: `@deepseek-ai/dsh-user-approval`
- 分组: G09 审批权限
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/interaction/user-approval`

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
