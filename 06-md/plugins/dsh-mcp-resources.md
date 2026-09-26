# dsh-mcp-resources

- 包名: `@deepseek-ai/dsh-mcp-resources`
- 分组: G25 MCP 协议
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/mcp/mcp-resources`

## 实现逻辑
McpResourceRuntime 继承 Service 并声明 ctx.mcpResources，以 ScopedLayers/NamedEntries 按作用域存放各 MCP 连接的资源 provider；某作用域首个 provider 注册时挂载三条共享工具，末个移除时同步卸载（src/index.ts:36-119）。request() 先按 exec.agent 的可视作用域解析目标 server，找不到即报错，再把操作委托给 provider（src/index.ts:122-126）。tools.ts 定义 list_mcp_resources、list_mcp_resource_templates、read_mcp_resource 三工具并适配模型参数（src/tools.ts:31-63）；render.ts 以 JSON replacer 把 blob 二进制替换为描述文本，避免其进入模型历史（src/render.ts:16-23）。

## Provides
- ctx.mcpResources (作用域化 MCP 资源运行时，含三条 list/read 资源工具，src/index.ts:47-127)
- systemPrompt `mcp-resource-servers` 段（列出当前作用域可用资源服务器名，src/index.ts:59-71）

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 把资源结果投影为核心内容块
  - 证据: `src/render.ts:7 type ContentBlock`
- `dsh-scope` [编译依赖] - 按 Agent 作用域分层保存与合并资源 provider
  - 证据: `src/index.ts:8 createScope/NamedEntries/ScopedLayers/scopeOf`
- `dsh-system-prompt` [E1+E2] - 发布资源服务器清单提示段
  - 证据: `src/index.ts:11 type import + src/index.ts:59 ctx.inject(['systemPrompt'])`
- `dsh-tools` [E1+E2] - 注册并注销三条共享资源工具
  - 证据: `src/tools.ts:8 import defineTool + src/index.ts:49 static inject ['tools'] + src/tools.ts:33 ctx.tools.register`

## Dependents (下游被依赖)
- `dsh-mcp-client` - 向资源运行时发布本连接的资源请求能力
