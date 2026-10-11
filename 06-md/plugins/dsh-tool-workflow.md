# dsh-tool-workflow

- 包名: `@deepseek-ai/dsh-tool-workflow`
- 分组: G47 工作流
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/workflow/tool-workflow`

## 实现逻辑
apply() 先在 ctx.systemPrompt 注册 tool:<toolName> 用法段（把“仅显式要求时使用”的调用策略作为工具自带提示而非 persona 文本），再在 ctx.tools 注册 workflow 工具 (src/index.ts:315-328)。execute 前台分支调用 ctx.workflowEngine.start 并 await run.result，非 completed 的 stopReason 一律映射成工具错误，finally 里必定 dispose 并收尾记录 (src/index.ts:430-479)。后台分支经 ctx.get('jobs').start 把运行注册为 kind 'workflow' 的 job，脚本在 starter 内启动、结算即 job 结算，返回值随 job result 回传 (src/index.ts:262-313)。两个观察者：createWorkflowRecorder 把 workflow/agent-start|agent-end 落成 tool-workflow/* 持久事件，createWorkflowRecordMirror 把 workflow/phase|log 与成员事件镜像进 job 输出环 (src/index.ts:93-151, src/record.ts:37-63)。

## Provides
- ctx.tools (注册 `workflow` 模型工具：运行 JS 编排脚本 fan-out 子 agent 并返回脚本最终值)
- ctx.systemPrompt (注册 `tool:workflow` 用法段，声明仅显式要求编排时才使用)
- Session 事件 tool-workflow/run-start|agent-start|agent-end|run-end (顶层 workflow 运行的持久留痕)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 工具以调用方 Agent 为 parent 归置子 agent 与 job owner，非 Agent 调用直接拒绝
  - 证据: `package.json:36 peerDep + src/index.ts:19 import type { Agent }`
- `dsh-llm` [编译依赖] - 结果渲染卡片类型需要 llm 的内容块词汇
  - 证据: `package.json:38 peerDep + src/index.ts:20 import type { ContentBlock }`
- `dsh-session` [编译依赖] - 把顶层 workflow 运行与成员生命周期写成调用方 session 的持久事件
  - 证据: `package.json:39 peerDep + src/index.ts:22 import type { Session, SessionEventMap } + src/types.ts:8 import type { SessionId }`
- `dsh-system-prompt` [运行时依赖] - 把工具用法策略作为独立 prompt 段落注册，随工具存在而生效
  - 证据: `package.json:40 peerDep + src/index.ts:323 ctx.systemPrompt.section(...) (order 取自 src/index.ts:325 getSectionOrder)`
- `dsh-tools` [运行时依赖] - 用 defineTool 声明参数与 oneOf 输出 schema，并把工具登记进注册表
  - 证据: `package.json:41 peerDep + src/index.ts:17-18 import { defineTool } + src/index.ts:328 ctx.tools.register`

## Dependents (下游被依赖)
- `dsh-client-ui-workflow-run` - 读取工具侧 workflow 代理起止事件数据
