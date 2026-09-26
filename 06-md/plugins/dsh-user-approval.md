# dsh-user-approval

- 包名: `@deepseek-ai/dsh-user-approval`
- 分组: G21 交互命令
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/interaction/user-approval`

## 实现逻辑
实现 ctx.approval 审批能力 seam 的服务定义：request() 要求处于未闭合 turn 内，先写 approval/asked 审计再经作用域 waterfall 求决策并写 approval/decided（src/index.ts:215-234、267-307）。策略 'never' 在任何答案者之前由服务自身决断性拒绝，缺答案者则 fail-closed 返回 unavailable（src/index.ts:275、283）。setPolicy 写 approval/policy 事件并把切换通知注入模型，systemPrompt 上下文档声明当前策略（src/index.ts:162-195）。

## Provides
- ctx.approval (审批服务 + approval/request 作用域 waterfall；approval/asked↔decided 审计不变量，src/index.ts:150-308)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 以 agent/session 为审批作用域与日志目标
  - 证据: `package.json:40 peerDep + src/index.ts:10、src/types.ts:10 type import Agent`
- `dsh-invariants` [E1+E2] - 注册审批审计流不变量
  - 证据: `package.json:42 peerDep + src/invariant.ts:5 import; src/invariant.ts:112 ctx.invariants.register`
- `dsh-llm` [E1+E2] - 把策略切换通知注入模型消息
  - 证据: `package.json:43 peerDep + src/index.ts:11-12 import createUserMessage/ContextFormed; src/index.ts:188 agent.inject`
- `dsh-scope` [E1+E2] - 按 agent 过滤审批请求分派
  - 证据: `package.json:44 peerDep + src/index.ts:19、src/types.ts:9 import scopeTarget/Scoped; src/index.ts:282 作用域 waterfall`
- `dsh-session` [E1+E2] - 把审批审计对写入会话日志
  - 证据: `package.json:45 peerDep + src/index.ts:20-21 import Session/SessionSeq; src/index.ts:225/232 session.append`
- `dsh-system-prompt` [E1+E2] - 声明当前审批策略的模型可见上下文
  - 证据: `package.json:46 peerDep + src/index.ts:22 type import; src/index.ts:162 ctx.inject(['systemPrompt'])`

## Dependents (下游被依赖)
- `dsh-acp` - 声明合并权限 waterfall 并提供一次性决策
- `dsh-api-remotes` - 审批 waterfall 事件签名
- `dsh-experimental-auto-review` - 按 approval policy 决定 reviewer deny 是 ask 还是终态 deny
- `dsh-permission-presets` - 按预设写穿 approval 策略
- `dsh-plugin-manager` - 对提权的管理动作要求用户审批
- `dsh-subagent` - 将子代理审批策略固定为 never
- `dsh-tool-bash` - 把沙箱升级请求路由到用户审批通道
- `dsh-tool-fs` - 沙箱升级等敏感操作走用户审批
- `dsh-tool-pwsh` - 把沙箱升级请求路由到用户审批通道
- `dsh-tools` - 可选消费审批服务以处理升级请求
