# dsh-tool-workflow

- 包名: `@deepseek-ai/dsh-tool-workflow`
- 分组: G20 工作流
- 拓扑层: Layer 7
- 来源层: L1 核心集
- 源码路径: `packages/workflow/tool-workflow`

## 为什么需要它（设计初衷）
面向模型的工作流工具：经 ctx.workflowEngine 运行 JS 编排脚本。

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-tool-workflow
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/workflow/tool-workflow

## 实现逻辑
模型可见 workflow 工具：apply 注册 defineTool({name: config.toolName ?? 'workflow'})。execute 校验 exec.agent 后调 ctx.workflowEngine.start，桥接 exec.signal→run.cancel，await run.result 后按 stopReason 映射错误；createWorkflowRecorder 监听 workflow/agent-start|end 把 tool-workflow/run-start 等 4 类事件追加进父 Session。

## Provides
- 模型工具 'workflow'
- systemPrompt section tool:workflow
- Session 事件 tool-workflow/run-start|agent-start|agent-end|run-end

## Depends On (上游依赖)
- `dsh-session` [编译依赖] - Session.append 记录运行事件
  - 证据: `packages/workflow/tool-workflow/src/index.ts:18,87`
- `dsh-system-prompt` [编译依赖] - systemPrompt.section
  - 证据: `packages/workflow/tool-workflow/src/index.ts:27,30,212`
- `dsh-tools` [编译依赖] - defineTool + register
  - 证据: `packages/workflow/tool-workflow/src/index.ts:15,30,217`
- `dsh-workflow-worker-thread` [编译依赖] - ctx.workflowEngine 具体实现
  - 证据: `packages/workflow/tool-workflow/package.json:61`

## Dependents (下游被依赖)
- `dsh-client-ui-workflow-run` - tool-workflow 事件负载类型
