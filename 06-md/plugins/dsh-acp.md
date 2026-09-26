# dsh-acp

- 包名: `@deepseek-ai/dsh-acp`
- 分组: G01 ACP 协议
- 拓扑层: Layer 7
- 来源层: L3 其余
- 源码路径: `packages/acp/acp`

## 实现逻辑
以 Cordis 函数插件把 ACP（Agent Client Protocol）服务端挂在 stdio JSON-RPC 上：apply() 先捕获注入的 sessionPersistence，构造 AcpSession 映射，并在 SDK 的 agent app 上注册 initialize/newSession/resumeSession/listSessions/closeSession/setSessionConfigOption/prompt/cancel 处理器 (src/index.ts:97-391)。每个会话由 AcpSession 组合一个未发布的 Agent（ctx.agents.create/resume，安装模型选择并挂载 ACP MCP 服务器）(src/session.ts:126-169)，再把已提交的 session 事件（assistant/message、tool/call、tool/result）投影为有序 ACP update 通知 (src/session.ts:345-389, src/updates.ts:16-85)。协议侧另有内容准入（文本/图片严格 base64 校验、拒绝 audio/resource 块）与模型/推理配置选项读写 (src/content.ts:123-204, src/model-control.ts:92-134)。权限请求走 approval/request waterfall，只提供一次性 allow/reject 选项，不推断持久授权 (src/index.ts:155-173)。

## Provides
- acp（自动化 ACP 服务端：JSON-RPC stdio 上的 initialize/newSession/resumeSession/listSessions/setSessionConfigOption/closeSession/prompt/cancel 方法族，供 dsh-subagent-acp 等程序化客户端驱动）
- 被代理 Agent 的会话生命周期，以及 model 与 reasoning_effort 标准配置选项（configOptions）
- approval/request 一次性权限决策通道（allow-once / reject-once，不产生持久授权）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 组合并驱动被代理 Agent，安装模型选择引用
  - 证据: `src/session.ts:13 import + src/session.ts:128 ctx.agents.create`
- `dsh-llm` [E1+E2] - 构造用户消息、错误链与模型目录查询
  - 证据: `src/session.ts:14 import + src/index.ts:20 errorChain`
- `dsh-mcp-client` [E1+E2] - 把 ACP 声明的 MCP 服务器挂成 Agent 作用域 MCP 客户端
  - 证据: `src/mcp.ts:8 import + src/mcp.ts:32 agentCtx.plugin(McpClient, config)`
- `dsh-session` [E1+E2] - 会话身份、头与已提交事件的投影来源
  - 证据: `src/session.ts:15 import + src/index.ts:229 ctx.sessions.flush`
- `dsh-token-meter` [运行时依赖] - 向客户端上报上下文占用（usage_update）
  - 证据: `src/updates.ts:6 import + src/updates.ts:95 ctx.get('tokenMeter')`
- `dsh-user-approval` [运行时依赖] - 声明合并权限 waterfall 并提供一次性决策
  - 证据: `src/index.ts:52 import + src/index.ts:155 ctx.on('approval/request')`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
