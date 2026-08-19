# dsh-command-goal

- 包名: `@deepseek-ai/dsh-command-goal`
- 分组: G10 命令交互
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/goal/command-goal`

## 为什么需要它（设计初衷）
面向用户的 /goal 命令控制，基于 ctx.goals 持久 goal 栈：无需模型轮次即可展示/创建/编辑/暂停/恢复/清除目标，并将完成度、Round 计数与续行（autocontinue）状态暴露给 UI 与同会话驱动器，解决长任务『目标不可见、无续跑机制』的问题。

发展史：通过 ctx.commands 注册全局命令，由 2026-07-19 的 human-goal-command Agent Note 决策演进而来；仅纯文本交互，适配器专用徽标等 UI 化能力列为暂缓。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/goal/command-goal/README.zh.md

## 实现逻辑
apply() 在 ctx.commands 注册 /goal 命令。handler 解析 show/create/edit/pause/resume/clear 语法，通过 ctx.goals.get/create/edit/pause/resume/clear(compare-and-set ref) 执行，GoalView 渲染为多行 CommandResult。

## Provides
- /goal 命令
- GoalCommand 语法解析与渲染

## Depends On (上游依赖)
- `dsh-commands` [组合依赖] - /命令注册
  - 证据: `packages/goal/command-goal/src/index.ts:12,164`
- `dsh-goal` [运行时依赖] - goal 域状态读写
  - 证据: `packages/goal/command-goal/src/index.ts:8,113-146`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
