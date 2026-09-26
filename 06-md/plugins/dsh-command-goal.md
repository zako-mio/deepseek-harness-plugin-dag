# dsh-command-goal

- 包名: `@deepseek-ai/dsh-command-goal`
- 分组: G17 目标与计划
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/goal/command-goal`

## 实现逻辑
以纯函数 parseGoalCommand 解析 /goal 的人类语法（show/create/edit/pause/resume/clear），再由 executeGoalCommand 把这些控制动词映射到 ctx.goals 的 compare-and-set 变更并渲染直接 UI 输出（src/index.ts:35-45, 126-177）。命令对象携带的附件经 submitObjectiveAttachments 以模型可见的 user 消息形式在目标下一轮前投递（src/index.ts:117-123）。apply 在 ctx.commands 上注册 Codex 形状的 'goal' 命令（src/index.ts:190-197）。

## Provides
- /goal 人类命令 (注册进 commands 注册表，管理目标的创建/编辑/暂停/恢复/清除)

## Depends On (上游依赖)
- `dsh-commands` [E1+E2] - 把 /goal 命令注册进命令注册表并复用其调用/结果类型
  - 证据: `src/index.ts:7-8 import (CommandDefinitionId, CommandInvocation) + src/index.ts:14 inject ['commands','goals'] + src/index.ts:191 ctx.commands.register`
- `dsh-goal` [E1+E2] - 通过目标域服务读写持久化目标并捕获 GoalError
  - 证据: `src/index.ts:9-10 import (GoalError, GoalPhase/GoalRef/GoalView) + src/index.ts:135 ctx.goals.get + src/index.ts:150 ctx.goals.create`
- `dsh-llm` [编译依赖] - 为目标附件构造模型可见的用户消息
  - 证据: `src/index.ts:11 import createUserMessage`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
