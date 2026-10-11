# dsh-acp

- 包名: `@deepseek-ai/dsh-acp`
- 分组: G01 ACP 协议
- 拓扑层: Layer 7
- 来源层: L3 其余
- 源码路径: `packages/acp/acp`

## 实现逻辑
以 Cordis 函数插件挂载一个 automation-only 的 Agent Client Protocol 服务端：apply 先捕获注入的 agents/llm/sessionPersistence/sessions(src/index.ts:62,100)，再用 @agentclientprotocol/sdk 的 ndJsonStream 把 process.stdin/stdout 接成 JSON-RPC 通道(src/index.ts:378-395)，并把 session/new|resume|list|close|setConfigOption|prompt|cancel 映射为 AcpSession 生命周期(src/index.ts:200-374)。AcpSession 通过 ctx.agents.create/resume 组合或恢复 Agent 并装载 ACP 声明的 MCP server(src/session.ts:129-172, src/mcp.ts:26-33)，把已提交的 session 事件翻译成标准 ACP update(src/updates.ts:16-102)，并把 approval/request 转成一次性的 requestPermission 请求(src/index.ts:159-177)。

## Provides
- ACP 协议服务端能力(JSON-RPC over stdio 的 automation-only Agent Client Protocol 桥，src/index.ts:97-441)
- 标准 ACP 方法集 session/new|list|resume|close|setConfigOption|prompt|cancel(src/index.ts:382-394)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 创建/恢复被 ACP 驱动的 Agent，并订阅 agent/* 事件维护会话记录
  - 证据: `package.json:36 peerDep + src/session.ts:13 import + src/index.ts:62 inject 'agents' + src/session.ts:131 ctx.agents.create`
- `dsh-llm` [E1+E2] - 构造模型选择控制并探测当前路由的图像输入能力
  - 证据: `package.json:38 peerDep + src/content.ts:8 import + src/index.ts:62 inject 'llm' + src/session.ts:130 ctx.llm`
- `dsh-mcp-client` [E1+E2] - 把 ACP newSession/resumeSession 声明的 MCP server 挂载到 Agent 作用域
  - 证据: `package.json:39 peerDep + src/mcp.ts:8 import * as McpClient + src/mcp.ts:32 agentCtx.plugin(McpClient, config)`
- `dsh-session` [E1+E2] - 以 Session 身份承载事件流并在 session/new 后落盘会话
  - 证据: `package.json:40 peerDep + src/session.ts:15 import + src/index.ts:233 ctx.sessions.flush`
- `dsh-token-meter` [E1+E2] - 在有用量与容量事实时发出标准 usage_update
  - 证据: `package.json:42 peerDep(optional) + src/updates.ts:6 import type {} + src/updates.ts:95 ctx.get('tokenMeter')`
- `dsh-user-approval` [E1+E2] - 把权限请求转成 ACP requestPermission 并只回一次性决定
  - 证据: `package.json:43 peerDep + src/index.ts:52 import type {} + src/index.ts:159 ctx.on('approval/request')`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
