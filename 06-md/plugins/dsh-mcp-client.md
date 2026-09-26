# dsh-mcp-client

- 包名: `@deepseek-ai/dsh-mcp-client`
- 分组: G25 MCP 协议
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/mcp/mcp-client`

## 实现逻辑
外部 MCP 服务器桥接：apply() 先解析重连策略、以 WeakMap 按注册作用域预留 serverName 命名空间，再由 startConnection 建立受监督连接并 registerServerContext 发布资源与指令，最后 await ready 以在激活前完成首连与工具同步（src/index.ts:154-203、src/connection.ts:127-409）。syncTools 拉取 tools/list，并以 mcp__<serverName>__<rawName> 公开名注册到 ctx.tools；注册冲突整代回滚（全有或全无）（src/tools.ts:113-162）。transport.ts 按 config 构造 stdio（经 dsh-subprocess 擦洗父环境）或 Streamable HTTP 传输（src/transport.ts:21-46）。连接断开时按有界指数退避重启，超预算则注销工具（src/connection.ts:211-245）。

## Provides
- ctx.tools 的 mcp__<serverName>__<rawName> 工具集（外部 MCP 工具桥接，src/tools.ts:149-151）
- ctx.mcpResources 注册（把连接代次的资源访问暴露给资源工具，src/server-context.ts:28-31）
- systemPrompt `mcp:<server>` 段（服务端指令原文，src/server-context.ts:32-38）

## Depends On (上游依赖)
- `dsh-llm` [E1+E2] - 校验当前模型路由声明了图像输入能力
  - 证据: `src/tools.ts:21 type ContentBlock + src/tools.ts:358 ctx.get('llm')、src/tools.ts:364 llm.resolveModelInfo`
- `dsh-mcp-resources` [E1+E2] - 向资源运行时发布本连接的资源请求能力
  - 证据: `src/server-context.ts:8 type McpResourceProvider + src/server-context.ts:29 ctx.inject(['mcpResources'])`
- `dsh-scope` [编译依赖] - 按注册作用域隔离 serverName 与 Agent 级命名空间复用
  - 证据: `src/index.ts:18 scopeOf`
- `dsh-system-prompt` [E1+E2] - 把服务端 attributed instructions 写入系统提示段
  - 证据: `src/server-context.ts:9 type import + src/server-context.ts:32 inner.systemPrompt.section`
- `dsh-tools` [E1+E2] - 把发现的 MCP 工具注册进 harness 工具运行时
  - 证据: `src/index.ts:24 type import + src/index.ts:34 inject 'tools' + src/tools.ts:150 ctx.tools.register`

## Dependents (下游被依赖)
- `dsh-acp` - 把 ACP 声明的 MCP 服务器挂成 Agent 作用域 MCP 客户端
- `dsh-experimental-browser-use-stagehand-native` - 把原生方法适配为 MCP 形状的工具定义
- `dsh-experimental-computer-use-cua-driver-mcp` - 承载 MCP 连接（发现/执行/重连）并作为子插件生命周期
- `dsh-experimental-computer-use-cua-driver-native` - 把原生工具目录适配为 MCP 形状工具定义
