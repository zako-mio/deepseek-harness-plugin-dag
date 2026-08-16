# dsh-tool-goal

- 包名: `@deepseek-ai/dsh-tool-goal`
- 分组: G17 目标计划
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/goal/tool-goal`

## 实现逻辑
apply() 注册 get_goal/create_goal/update_goal 工具与 systemPrompt section 'tool:goal'。authority.ts 校验执行时 agent 为 live 且 open turn(GOAL_TOOL_DRIVER_REQUIRED)，create/edit/pause/resume 需 requireDirectHuman，complete/blocked 可由 direct-human 或精确 goal round 授权；autonomous 完成经 exec.deferContext 注入 wrapup 收尾上下文。

## Provides
- ctx.tools: get_goal/create_goal/update_goal
- systemPrompt section tool:goal
- execution-time authority 校验

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - 调用者认证
  - 证据: `packages/goal/tool-goal/src/authority.ts:55-62`
- `dsh-goal` [运行时依赖] - goal 域读写
  - 证据: `packages/goal/tool-goal/src/index.ts:9,202,225,269`
- `dsh-session` [运行时依赖] - open turn 判定
  - 证据: `packages/goal/tool-goal/src/authority.ts:30-42`
- `dsh-system-prompt` [组合依赖] - 模型策略指导
  - 证据: `packages/goal/tool-goal/src/index.ts:189`
- `dsh-tools` [组合依赖] - 工具注册
  - 证据: `packages/goal/tool-goal/src/index.ts:12,195`

## Dependents (下游被依赖)
- `dsh-agent-spine-demo` - 可选 ctx.plugin(toolGoal) 模型面目标工具
