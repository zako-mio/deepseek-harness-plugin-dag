# dsh-workflow-worker-thread

- 包名: `@deepseek-ai/dsh-workflow-worker-thread`
- 分组: G20 工作流
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/workflow/workflow-worker-thread`

## 为什么需要它（设计初衷）
WorkflowEngine 实现：每次运行一个 Node worker thread 执行模型编写的工作流编排脚本，子 agent 留在 host，经类型化协议通过 ctx.subagents 桥接。核心目的：同步脚本循环不阻塞 host 事件循环，且忽略取消的脚本可随 worker.terminate() 真正终止；明确非安全沙箱，worker 只做事件循环隔离、空环境与结构化克隆边界。

发展史：2026-08-12 以 0.0.1-rc.3 发布，晚于首批基础包 2 天；作为 workflow seam 的 worker-thread 引擎，供 dsh-tool-workflow 面向模型消费。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/workflow/workflow-worker-thread/README.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-workflow-worker-thread

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
