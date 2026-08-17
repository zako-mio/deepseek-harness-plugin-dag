# dsh-agent-spine-demo

- 包名: `@deepseek-ai/dsh-agent-spine-demo`
- 分组: G37 示例与框架
- 拓扑层: Layer 7
- 来源层: L3 其余
- 源码路径: `packages/examples/agent-spine-demo`

## 为什么需要它（设计初衷）
默认无执行器/无 UI 的 agent spine 作为单一 bundle 插件：装载每个 harness agent 所需的固定服务集，应用只加点与可换后端。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/examples/agent-spine-demo/README.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-agent-spine-demo

## 实现逻辑
默认 executor-less/UI-less agent spine 组合插件。apply() 按依赖分层 ctx.plugin 装配：Timer/LlmRuntime/SessionStore/SessionTitleService/SystemPrompt/ToolRuntime 核心 → SkillRegistry+SkillFileSystem(skills 可选) → AgentRegistry+llmRetry → 可选 GoalService/toolGoal/goalSession → LocalJobRegistry+InvariantRegistry+4 个 invariant 伴随插件 → 可选 bashEnv+toolBash → workspaceContext → toolSkill/toolJobs → AgentLoop(agents 列表驱动)。Config 用 z.intersect 合并 AgentLoop.Config+SystemPrompt.Config+自有 schema；pickSpineConfig() 提取 bundle 属主字段供 app 包转发。只暴露命名导出(Loader 默认解包会丢 Config schema, 见 docs/postmortem/0001)。

## Provides
- agent-spine-demo 组合插件
- pickSpineConfig 字段提取
- SkillConfigSchema/SessionTitleConfigSchema/ToolBashConfigSchema/GoalConfigSchema 等转发 schema
- agent-spine-demo-invariant 伴随插件

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - ctx.plugin(AgentRegistry) agent 注册表
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:237`
- `dsh-agent-instructions` [运行时依赖] - 可选 ctx.plugin(workspaceContext) 工作区上下文
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:255`
- `dsh-agent-loop` [运行时依赖] - ctx.plugin(AgentLoop) 装配循环，agents 声明式启动
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:261-264`
- `dsh-goal` [运行时依赖] - 可选 ctx.plugin(GoalService) 持久化目标域
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:240`
- `dsh-goal-round-driver` [运行时依赖] - 可选 ctx.plugin(goalSession) 同会话目标驱动
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:242`
- `dsh-jobs-local` [运行时依赖] - ctx.plugin(LocalJobRegistry) 进程内后台任务
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:244`
- `dsh-llm` [运行时依赖] - ctx.plugin(LlmRuntime) LLM 服务
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:221`
- `dsh-llm-retry` [运行时依赖] - ctx.plugin(llmRetry) provider 路由重试
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:238`
- `dsh-session` [运行时依赖] - ctx.plugin(SessionStore) 事件溯源会话存储
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:222`
- `dsh-session-title` [运行时依赖] - ctx.plugin(SessionTitleService) 会话标题服务
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:223`
- `dsh-shell-env` [运行时依赖] - ctx.plugin(bashEnv) shell 环境
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:251`
- `dsh-skill` [运行时依赖] - ctx.plugin(SkillRegistry) 技能注册表(可选)
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:234`
- `dsh-skill-filesystem` [运行时依赖] - ctx.plugin(SkillFileSystem) 本地技能提供者
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:235`
- `dsh-system-prompt` [运行时依赖] - ctx.plugin(SystemPrompt) 提示词装配
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:225-230`
- `dsh-tool-bash` [运行时依赖] - 可选 ctx.plugin(toolBash) 模型面 bash 工具
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:252`
- `dsh-tool-goal` [运行时依赖] - 可选 ctx.plugin(toolGoal) 模型面目标工具
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:241`
- `dsh-tool-jobs` [运行时依赖] - 可选 ctx.plugin(toolJobs) 模型面任务工具
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:260`
- `dsh-tool-skill` [运行时依赖] - 可选 ctx.plugin(toolSkill) 模型面技能目录
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:259`
- `dsh-tools` [运行时依赖] - ctx.plugin(ToolRuntime) 工具注册表
  - 证据: `packages/examples/agent-spine-demo/src/index.ts:231`

## Dependents (下游被依赖)
- `dsh-acp-demo` - ctx.plugin(agentCore) 装配默认 spine 作为 ACP 会话后端
