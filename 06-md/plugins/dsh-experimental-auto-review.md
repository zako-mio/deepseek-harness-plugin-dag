# dsh-experimental-auto-review

- 包名: `@deepseek-ai/dsh-experimental-auto-review`
- 分组: G13 实验特性
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/experimental/auto-review`

## 实现逻辑
为 current-session-only 的 Auto 权限预设提供 LLM 授权门：在 `tools/pre-execute` 上 prepend 监听器，仅当 session 处于 AUTO_PRESET 且非 `run_code` 外层传输时介入（src/index.ts:686-721）。它把 provider/model/cwd/项目指令/过滤历史/待执行动作冻结为五段快照（src/index.ts:361-523），经 `ctx.llm.stream` 用固定 REVIEW_POLICY 请求 reviewer，并对返回 JSON 做严格 risk/decision 协议解析（src/index.ts:562-638）。deny 时按 approval policy 决定 ask 还是终态 deny，并注册 Auto 预设、卸载时把受影响 session 降级为 danger-full-access（src/index.ts:709-738）。

## Provides
- Auto 权限预设的按调用 LLM 审查门 (tools/pre-execute prepend 决策)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 读取会话 surface、header 与 cwd 构造审查快照
  - 证据: `src/index.ts:12 import type { Agent } + src/index.ts:361 agent`
- `dsh-agent-instructions` [编译依赖] - 识别项目指令来源并归入 constraint 角色
  - 证据: `src/index.ts:13 import type {} from '@deepseek-ai/dsh-agent-instructions'`
- `dsh-llm` [E1+E2] - 用当前请求路由调用 reviewer 模型并解析流式块
  - 证据: `src/index.ts:22 import BlockAssembler/GenerateOptions 等 + src/index.ts:126 inject + src/index.ts:637 ctx.llm.stream`
- `dsh-permission-presets` [E1+E2] - 注册 Auto 预设并读取/设置当前 session 预设
  - 证据: `src/index.ts:24 import AUTO_PRESET + src/index.ts:126 inject + src/index.ts:680 permissionPresets + src/index.ts:723 registerAuto`
- `dsh-session` [E1+E2] - 读取会话事件日志并对受影响会话降级
  - 证据: `src/index.ts:25 import type { SessionEvent } + src/index.ts:126 inject 'sessions' + src/index.ts:730 ctx.sessions.list`
- `dsh-subagent` [编译依赖] - 解析子 Agent 的直接父指令初始提示边界
  - 证据: `src/index.ts:26 import type {} from '@deepseek-ai/dsh-subagent'`
- `dsh-tools` [E1+E2] - 在工具执行前介入并返回 allow/deny/ask/cancel 决策
  - 证据: `src/index.ts:32 import RUN_CODE_NAME/PreToolDecision + src/index.ts:126 inject 'tools' + src/index.ts:686 tools/pre-execute`
- `dsh-user-approval` [E1+E2] - 按 approval policy 决定 reviewer deny 是 ask 还是终态 deny
  - 证据: `src/index.ts:27 import type {} from '@deepseek-ai/dsh-user-approval' + src/index.ts:126 inject 'approval' + src/index.ts:710 overrideOf`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
