# dsh-user-approval

- 包名: `@deepseek-ai/dsh-user-approval`
- 分组: G20 交互命令
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/interaction/user-approval`

## 实现逻辑
审批能力 seam 的 Service Definition：ApprovalService 注入 systemPrompt，把当前有效策略作为运行时上下文段落追加在保留历史之后，使切换策略不重写稳定缓存前缀 (src/index.ts:150-175)。request() 要求处于已打开 turn 内（否则审计事件会成为重载时被丢弃的崩溃尾部），先追加 approval/asked、再跑 approval/request waterfall、最后追加 approval/decided，构成成对审计 (src/index.ts:215-234, src/index.ts:84-92)。策略 never 在 dispatch 之前就返回 rejected（不依赖监听器顺序），缺失、抛错或返回非词汇值的 answerer 一律归一为 fail-closed 的 unavailable，取消经信号竞速立即结算 (src/index.ts:267-307)。

## Provides
- ctx.approval (ApprovalService：一次性审批决定、会话策略读写、审计)
- Cordis 事件 approval/request（Agent 作用域 waterfall，由 answerer 认领）
- Session 事件 approval/asked 与 approval/decided（成对审计）、approval/policy（策略覆盖）
- systemPrompt 上下文段 approval:policy（向模型陈述当前策略）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 审批请求以 Agent 为路由键与审计归属，切换通知注入该 agent
  - 证据: `src/index.ts:10 import type { Agent } + src/types.ts:10 + src/index.ts:188 agent.inject`
- `dsh-llm` [编译依赖] - 策略切换以用户消息注入会话，并复用 LLM 的 ToolCallId brand
  - 证据: `src/index.ts:11-12 import { createUserMessage, ContextFormed } + src/types.ts:11 dsh-llm/brand`
- `dsh-session` [编译依赖] - 审计事件必须落在可回放的会话日志中
  - 证据: `src/index.ts:20-21 import { SessionSeq } + src/index.ts:225,232 session.append 审计对`
- `dsh-system-prompt` [E1+E2] - 把有效策略作为运行时上下文告知模型
  - 证据: `src/index.ts:22 import type {} from '@deepseek-ai/dsh-system-prompt' + src/index.ts:162-165 ctx.inject(['systemPrompt']).context()`

## Dependents (下游被依赖)
- `dsh-acp` - 把权限请求转成 ACP requestPermission 并只回一次性决定
- `dsh-api-remotes` - 为 approval/request 转发事件提供 Events 声明
- `dsh-experimental-auto-review` - 按当前审批策略决定拒绝是终局还是转交用户询问
- `dsh-permission-presets` - 审批策略是预设 bundle 的另一半旋钮，并经 approval 服务切换
- `dsh-plugin-manager` - 把升级请求接到审批通道
- `dsh-subagent` - 继承的审批会话事件负载需要该服务类型
- `dsh-tool-bash` - 沙箱越权必须先拿到人工审批通道
- `dsh-tool-fs` - 升级到更宽沙箱模式的请求经审批服务裁决
- `dsh-tool-pwsh` - 沙箱越权必须先拿到人工审批通道
- `dsh-tools` - 把 pre-execute 的 ask 决策路由到人工审批通道；无通道时按契约降级为拒绝
