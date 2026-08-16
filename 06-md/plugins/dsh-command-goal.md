# dsh-command-goal

- 包名: `@deepseek-ai/dsh-command-goal`
- 分组: G10 命令交互
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/goal/command-goal`

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
