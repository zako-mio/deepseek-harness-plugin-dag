# dsh-command-feedback

- 包名: `@deepseek-ai/dsh-command-feedback`
- 分组: G10 命令交互
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/feedback/command-feedback`

## 实现逻辑
apply() 在 ctx.commands 注册 /feedback 命令(recordInput:false)。handler 校验非空文本后 recordFeedback() 向 session append 'feedback/record' 事件(log-only)，acknowledge 附带 session id、匿名用户 id 与 session-telemetry 共享披露句。

## Provides
- /feedback 命令
- session 事件 feedback/record
- recordFeedback()

## Depends On (上游依赖)
- `dsh-commands` [组合依赖] - /命令注册
  - 证据: `packages/feedback/command-feedback/src/index.ts:16,101`
- `dsh-session` [运行时依赖] - feedback/record 持久化
  - 证据: `packages/feedback/command-feedback/src/index.ts:12,75`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
