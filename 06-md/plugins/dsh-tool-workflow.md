# dsh-tool-workflow

- 包名: `@deepseek-ai/dsh-tool-workflow`
- 分组: G49 工作流
- 拓扑层: Layer 8
- 来源层: L1 核心集
- 源码路径: `packages/workflow/tool-workflow`

## 实现逻辑
注册模型可见的 workflow 工具（默认名 workflow）与使用指引章节 (src/index.ts:315-483)。前台执行把脚本交给 ctx.workflowEngine.start 并 await result，非 completed 停止原因转为工具错误 (src/index.ts:433-479)；run_in_background 则把运行注册为 ctx.jobs 作业并立即返回 jobId (src/index.ts:262-313)。createWorkflowRecorder 把 workflow/* 事件折叠成 tool-workflow/* 会话记录 (src/index.ts:93-151)，record.ts 把进度镜像进作业输出环 (src/record.ts:37-63)，invariant.ts 作为伴生插件校验这些记录的持久化不变量 (src/invariant.ts:132-168)。

## Provides
- tools.workflow (模型可见的工作流编排工具，前台/后台两态)
- systemPrompt 章节 tool:workflow
- tool-workflow/* 会话事件 (持久化的工作流运行记录)
- invariants 伴生校验 (tool-workflow 记录折叠)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 取得调用方 Agent 以归属后台作业与工作流运行记录
  - 证据: `package.json:41 peerDep + src/index.ts:19 import type { Agent } + src/index.ts:407 exec.agent + src/index.ts:442 parent.session`
- `dsh-invariants` [E1+E2] - 注册 tool-workflow 记录的伴生不变量校验器
  - 证据: `package.json:42 peerDep + src/invariant.ts:5 import type { InvariantFailure, InvariantInstaller } + src/invariant.ts:13 static inject ['invariants'] + src/invariant.ts:168 ctx.invariants.register`
- `dsh-llm` [编译依赖] - 工具呈现使用 dsh-llm 的内容块类型
  - 证据: `package.json:44 peerDep + src/index.ts:20 import type { ContentBlock }`
- `dsh-session` [E1+E2] - 把运行记录写入会话并订阅会话事件做不变量折叠
  - 证据: `package.json:45 peerDep + src/index.ts:22 import type { Session, SessionEventMap } + src/index.ts:102 session.append + src/invariant.ts:4 import type { Session, SessionEvent } + src/invariant.ts:154 ctx.on('session/event')`
- `dsh-system-prompt` [E1+E2] - 注册 workflow 工具的使用策略提示章节
  - 证据: `package.json:46 peerDep + src/index.ts:41 inject 'systemPrompt' + src/index.ts:323 ctx.systemPrompt.section`
- `dsh-tools` [E1+E2] - 注册 workflow 工具定义与呈现
  - 证据: `package.json:47 peerDep + src/index.ts:17 import { defineTool } + src/index.ts:41 static inject ['tools','workflowEngine','systemPrompt'] + src/index.ts:328 ctx.tools.register`
- `dsh-workflow-ptc` [组合依赖] - base bundle 中 workflow-ptc 先行装配以提供 ctx.workflowEngine，tool-workflow 随后装配使用该服务
  - 证据: `packages/bundle/base/cordis.patch.yml:392-398`

## Dependents (下游被依赖)
- `dsh-client-ui-workflow-run` - 解析工具侧工作流成员事件数据
