# dsh-agent-instructions

- 包名: `@deepseek-ai/dsh-agent-instructions`
- 分组: G08 上下文注入
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/context/agent-instructions`

## 实现逻辑
AGENTS.md 兼容的工作区指令加载器：启动/恢复基线在首个请求前进入持久上下文，成功触及文件的 fs 工具会把嵌套/变更/移除的指令合入 inbox（src/index.ts:84-225）。通过 ctx.fs 逐目录探测候选指令文件、按字节预算渲染、按 trimmed-content 摘要去重，并把变更状态协商进 sessionProjections 的 turnBoundary 判定（src/index.ts:286-294、src/state.ts:247-433）。监听 session/event(step/end)、agent/pre-step、tools/result 以在正确提交边界刷新指令上下文（src/index.ts:307、src/index.ts:315、src/index.ts:343）。仅在 ctx.fs 存在时生效，无 provider 时退化为 no-op（src/index.ts:119-120）。

## Provides

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 在 agent 步前把工作区指令上下文拼入请求消息序列，并读取 agent.session 的可见表面状态
  - 证据: `src/index.ts:14 import type Agent/PreStepDecision + src/index.ts:315 ctx.on('agent/pre-step') + src/state.ts:7 import type Agent`
- `dsh-llm` [编译依赖] - 把渲染后的指令文本构造成带 source 标记的 user 消息注入上下文
  - 证据: `src/index.ts:15 import createUserMessage + src/state.ts:8 createUserMessage + src/state.ts:9 import type Message`
- `dsh-session` [E1+E2] - 读写会话表面历史以判定指令是否已注入，并在 step/end 边界触发刷新
  - 证据: `src/index.ts:16 import type Session/UserMessage + src/index.ts:184 type import + src/index.ts:307 ctx.on('session/event') + src/state.ts:10 import type Session/UserMessage`
- `dsh-session-projection` [E1+E2] - 依赖 turnBoundary 投影判断当前步是否开放，决定指令刷新是立即排队还是延迟到步结束
  - 证据: `src/index.ts:17 type-only import + src/index.ts:34 inject ['sessionProjections'] + src/index.ts:287 ctx.sessionProjections.stateOf(session, 'turnBoundary')`
- `dsh-tools` [E1+E2] - 从成功的 read/write/edit 工具结果中提取 file_path，把被触及路径转成指令刷新线索
  - 证据: `src/index.ts:18 import type ToolExecution/ToolExecutionResult/ToolExecutionToken + src/index.ts:343 ctx.on('tools/result')`

## Dependents (下游被依赖)
- `dsh-experimental-auto-review` - 识别项目指令来源并归入 constraint 角色
