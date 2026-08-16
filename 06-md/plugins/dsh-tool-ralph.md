# dsh-tool-ralph

- 包名: `@deepseek-ai/dsh-tool-ralph`
- 分组: G20 工作流
- 拓扑层: Layer 7
- 来源层: L1 核心集
- 源码路径: `packages/workflow/tool-ralph`

## 实现逻辑
模型可见 Ralph 循环工具：apply 注册 'ralph' 工具，execute 经 ctx.workflowEngine.start 执行固定 RALPH_SCRIPT。脚本每轮调 agent(prompt, {schema}) 启动 fresh structured-output 子代理，仅携带不可变 objective 与上轮受限结构化 handoff；requireFreshProvider 强制 provider 具备 outputSchema 且不继承父上下文。

## Provides
- 模型工具 'ralph'
- RALPH_SCRIPT/RALPH_META 固定编排
- systemPrompt section tool:ralph
- 子代理路由校验(fresh+outputSchema)

## Depends On (上游依赖)
- `dsh-subagent` [编译依赖] - getProvider 校验 fresh provider
  - 证据: `packages/workflow/tool-ralph/src/index.ts:12,20,221`
- `dsh-system-prompt` [编译依赖] - systemPrompt.section
  - 证据: `packages/workflow/tool-ralph/src/index.ts:17,20,407`
- `dsh-tools` [编译依赖] - defineTool + register
  - 证据: `packages/workflow/tool-ralph/src/index.ts:13,20,412`
- `dsh-workflow-worker-thread` [编译依赖] - ctx.workflowEngine 具体实现
  - 证据: `packages/workflow/tool-ralph/package.json:61`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
