# dsh-workflow-worker-thread

- 包名: `@deepseek-ai/dsh-workflow-worker-thread`
- 分组: G20 工作流
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/workflow/workflow-worker-thread`

## 实现逻辑
worker-thread workflow 引擎：WorkerThreadWorkflowEngine extends WorkflowEngine 注册为 ctx.workflowEngine。start() 同步校验 meta、宿主侧 body 预解析、解析 subagent provider 路由与并发上限，随后在独立 worker 线程执行模型编写的脚本，worker 内 agent() 经 ChildRpcBridge RPC 回宿主，宿主 startChild 调 this.subagents.start(provider) 启动子代理并把结果结构化克隆回 worker；发布 workflow/start|phase|log|agent-start|agent-end|end 事件。

## Provides
- ctx.workflowEngine(WorkerThreadWorkflowEngine)
- workflow/* 事件
- WorkerRun/materializeFromRealm/validateMeta

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - request.parent Agent
  - 证据: `packages/workflow/workflow-worker-thread/src/index.ts:14,177`
- `dsh-session` [编译依赖] - snapshotJsonValue 序列化跨 worker
  - 证据: `packages/workflow/workflow-worker-thread/src/host.ts:16,393`
- `dsh-subagent` [编译依赖] - startChild 经 subagents.start(provider)
  - 证据: `packages/workflow/workflow-worker-thread/src/host.ts:352`
- `dsh-tools` [编译依赖] - agent() 选项 schema
  - 证据: `packages/workflow/workflow-worker-thread/package.json:46`

## Dependents (下游被依赖)
- `dsh-tool-ralph` - ctx.workflowEngine 具体实现
- `dsh-tool-workflow` - ctx.workflowEngine 具体实现
