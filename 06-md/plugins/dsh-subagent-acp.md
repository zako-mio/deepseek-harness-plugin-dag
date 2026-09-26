# dsh-subagent-acp

- 包名: `@deepseek-ai/dsh-subagent-acp`
- 分组: G41 子代理
- 拓扑层: Layer 7
- 来源层: L3 其余
- 源码路径: `packages/subagent/subagent-acp`

## 实现逻辑
以 AcpProvider 注册进程外 ACP 子代理 provider（默认名 acp），声明零启动能力，且只从 parent 读取会话 workspace cwd (src/index.ts:132-188)。start() 经 ctx.subprocess.spawn 启动子进程，run.ts 用官方 ACP SDK 完成 initialize、session.new、session.prompt 握手，并对子进程权限请求按配置自动拒绝或选择首个 allow 选项 (src/run.ts:337-618)。运行结果经 seam 的 settleRunResult/subprocessRunHandle 结算，dispose 走 stdin EOF→terminate 的协作式关闭阶梯 (src/run.ts:184-219, 598-618)。

## Provides
- ctx.subagents 注册的 provider `acp` (进程外 ACP 子代理执行能力)

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 使用内容块类型
  - 证据: `src/run.ts:19 (import type ContentBlock)`
- `dsh-session` [编译依赖] - 品牌化父命名空间的 run/子会话 id
  - 证据: `src/run.ts:21 (import type SessionId)`
- `dsh-subagent` [E1+E2] - 复用 seam 契约并注册 acp provider
  - 证据: `src/index.ts:14-19 (import 类型) + src/index.ts:24 (inject ['subagents','subprocess']) + src/index.ts:205 (ctx.subagents.registerProvider) + src/run.ts:22 (import settleRunResult, subprocessRunHandle)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
