# dsh-agent-loop

- 包名: `@deepseek-ai/dsh-agent-loop`
- 分组: G03 核心服务
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/core/agent-loop`

## 实现逻辑
具体 agent 循环插件。AgentLoop 服务(static inject: agents/sessions/llm/tools/systemPrompt) 实现 dsh-agent 的 AgentFactory(createAgent/resume)，创建 ReactLoopAgent；config.agents 声明式启动。ReactLoopAgent 驱动 turn/step 边界：systemPrompt.assemble 装配提示词→runtimeContext 投影动态上下文→llm.prepareCall/stream 发起模型流→executeToolCalls 用 tools 注册表调度工具→错误经 agent/request-error 瀑布恢复。

## Provides
- ctx.agentLoop(AgentLoop)
- AgentFactory 实现(setFactory)
- ReactLoopAgent(Agent 驱动实现)
- agent-loop/config-start-failed 事件
- AGENT_LOOP_SETTINGS_NAMESPACE
- agent-loop-invariant 伴随插件

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - static inject agents + setFactory
  - 证据: `packages/core/agent-loop/src/index.ts:297, 350, 559-562`
- `dsh-llm` [运行时依赖] - llm.prepareCall/stream 发起模型调用
  - 证据: `packages/core/agent-loop/src/agent.ts:345, 449`
- `dsh-session` [运行时依赖] - ctx.sessions.prepare/enter/announce 创建会话
  - 证据: `packages/core/agent-loop/src/index.ts:24-25, 558-560, 590`
- `dsh-system-prompt` [运行时依赖] - ctx.systemPrompt.assemble 装配提示词
  - 证据: `packages/core/agent-loop/src/agent.ts:230, 337`
- `dsh-tools` [运行时依赖] - ctx.tools.executionMode 调度工具
  - 证据: `packages/core/agent-loop/src/tool-calls.ts:17, 88, 204`

## Dependents (下游被依赖)
- `dsh-agent-spine-demo` - ctx.plugin(AgentLoop) 装配循环，agents 声明式启动
