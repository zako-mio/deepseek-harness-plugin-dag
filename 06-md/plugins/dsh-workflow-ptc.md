# dsh-workflow-ptc

- 包名: `@deepseek-ai/dsh-workflow-ptc`
- 分组: G49 工作流
- 拓扑层: Layer 7
- 来源层: L1 核心集
- 源码路径: `packages/workflow/workflow-ptc`

## 实现逻辑
PtcWorkflowEngine 继承 dsh-workflow 的 WorkflowEngine 并注册为 ctx.workflowEngine (src/index.ts:102-189)。start() 先校验 meta（src/meta.ts:76-82）与脚本体可解析，再解析子代理 provider 与总子代理上限，构造 WorkerInit 与 PtcWorkflowRun (src/index.ts:133-174)。PtcWorkflowRun 通过注入的 ctx.ptcRuntime 在沙箱 Node 进程中执行脚本，VM 提供 agent/parallel/pipeline/phase/log 钩子并按调用方 Session 的文件策略约束 (src/host.ts:112-306, src/runtime.ts:56-367)。运行管理子代理的启动、结果、取消与释放，并在 start() 后发出 workflow/* 事件。

## Provides
- ctx.workflowEngine (基于共享沙箱 PTC 执行器的工作流引擎实现)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 承载子代理的父 Agent 身份与归属
  - 证据: `package.json:31 peerDep + src/host.ts:3 import type { Agent }`
- `dsh-llm` [编译依赖] - 把子代理最终输出块展平为文本作为 agent() 结果
  - 证据: `package.json:32 peerDep + src/runtime.ts:10 import type { ContentBlock } + src/types.ts:7 import type { ContentBlock }`
- `dsh-sandbox-policy` [E1+E2] - 按调用方 Session 解析文件/沙箱策略并施加于运行
  - 证据: `package.json:39 peerDep + src/index.ts:12 import type {} from dsh-sandbox-policy + src/index.ts:103 inject 'sandboxPolicy' + src/index.ts:166 ctx.sandboxPolicy.resolve`
- `dsh-session` [编译依赖] - 以 SessionId 标识子代理会话身份
  - 证据: `package.json:33 peerDep + src/host.ts:6 import { SessionId } + src/runtime.ts:11 import type { SessionId }`
- `dsh-subagent` [E1+E2] - 为脚本的 agent() 钩子启动/等待/释放子代理
  - 证据: `package.json:34 peerDep + src/host.ts:7-8 import SubagentRuntime/SubagentRun + src/index.ts:103 inject 'subagents' + src/host.ts:200 subagents.start`
- `dsh-tools` [编译依赖] - 校验 agent() 的结构化输出 schema 是否在支持子集内
  - 证据: `package.json:35 peerDep + src/host.ts:9 import { assertObjectJsonSchema } + src/runtime.ts:12 import { assertObjectJsonSchema, JsonSchemaError }`

## Dependents (下游被依赖)
- `dsh-tool-ralph` - base bundle 中 workflow-ptc 先行装配以提供 ctx.workflowEngine，tool-ralph 随后装配使用该服务
- `dsh-tool-workflow` - base bundle 中 workflow-ptc 先行装配以提供 ctx.workflowEngine，tool-workflow 随后装配使用该服务
