# dsh-tool-ralph

- 包名: `@deepseek-ai/dsh-tool-ralph`
- 分组: G49 工作流
- 拓扑层: Layer 8
- 来源层: L1 核心集
- 源码路径: `packages/workflow/tool-ralph`

## 实现逻辑
注册模型可见的 ralph 工具与专用 systemPrompt 章节 (src/index.ts:402-477)。execute 先校验调用方 agent，并要求子代理 provider 是「新鲜且支持结构化输出」的 (src/index.ts:218-230)，随后用固定的 RALPH_SCRIPT 通过 ctx.workflowEngine.start 启动工作流 (src/index.ts:445-453)。脚本每轮开一个无父上下文的新子代理，只传不可变目标与受 maxHandoffChars 限制的结构化 handoff，宿主侧再防御性解码每轮报告与终态 (src/index.ts:88-175, 244-331)。

## Provides
- tools.ralph (模型可见的 fresh-agent Ralph 循环工具)
- systemPrompt 章节 tool:ralph (仅显式请求时使用的使用策略)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 声明式 peer 依赖（通过 exec.agent 取得调用方 Agent）
  - 证据: `package.json:30 peerDep`
- `dsh-llm` [编译依赖] - 工具结果呈现使用 dsh-llm 的内容块类型
  - 证据: `package.json:31 peerDep + src/index.ts:10 import type { ContentBlock }`
- `dsh-subagent` [E1+E2] - 校验并指定每轮新子代理所用的 provider（新鲜、支持结构化输出）
  - 证据: `package.json:32 peerDep + src/index.ts:12 import type { SubagentProvider } + src/index.ts:18 inject 'subagents' + src/index.ts:219 ctx.subagents.getProvider`
- `dsh-system-prompt` [E1+E2] - 注册 ralph 的显式请求使用策略提示章节
  - 证据: `package.json:33 peerDep + src/index.ts:18 inject 'systemPrompt' + src/index.ts:405 ctx.systemPrompt.section`
- `dsh-tools` [E1+E2] - 注册 ralph 工具定义与结果呈现
  - 证据: `package.json:34 peerDep + src/index.ts:13 import { defineTool } + src/index.ts:18 static inject ['tools','workflowEngine','subagents','systemPrompt'] + src/index.ts:410 ctx.tools.register`
- `dsh-workflow-ptc` [组合依赖] - base bundle 中 workflow-ptc 先行装配以提供 ctx.workflowEngine，tool-ralph 随后装配使用该服务
  - 证据: `packages/bundle/base/cordis.patch.yml:392-397, 446-448`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
