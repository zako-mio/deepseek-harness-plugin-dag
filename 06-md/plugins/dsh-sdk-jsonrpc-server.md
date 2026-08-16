# dsh-sdk-jsonrpc-server

- 包名: `@deepseek-ai/dsh-sdk-jsonrpc-server`
- 分组: G31 协议与SDK
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/sdk/server`

## 实现逻辑
SDK 面向的 stdio JSON-RPC 服务插件（由外部 cordis.yml 决定加载）：HarnessSdkJsonRpcServer 持 JsonRpcLineTransport 处理 initialize/agent 生命周期/turn/subagent 等请求，订阅 session/agent/subagent 生命周期事件并向客户端 notify；shutdown 应答后 dispose 整个 root runtime 并 exit 0。stdout 保留给协议帧，不得挂 stdout logger。inject=['agents']，LLM seam 经 ctx.get() 可选读取。

## Provides
- sdk-jsonrpc-server 插件(name/inject['agents'])
- HarnessSdkJsonRpcServer 服务
- SDK 请求处理 + 生命周期 notify(subagent.started/subagent.finished)
- shutdown 协议控制进程退出

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - inject ['agents'] + Agent/AgentHandle 类型与 ctx.agents 工厂
  - 证据: `packages/sdk/server/src/index.ts:22, packages/sdk/server/src/server.ts:10`
- `dsh-llm` [编译依赖] - createUserMessage 构造消息
  - 证据: `packages/sdk/server/src/server.ts:11`
- `dsh-llm-deepseek` [编译依赖] - 默认 provider 初始化
  - 证据: `packages/sdk/server/src/server.ts:16`
- `dsh-session` [编译依赖] - SessionId 类型
  - 证据: `packages/sdk/server/src/server.ts:13`
- `dsh-subagent` [运行时依赖] - SubagentRuntime 类型 + ctx.on('subagent/end') 订阅生命周期
  - 证据: `packages/sdk/server/src/server.ts:14-15, 87-88`

## Dependents (下游被依赖)
- `dsh-sdk-jsonrpc-demo` - doc 契约：外部配置决定是否装载 dsh-sdk-jsonrpc-server 服务插件(运行时经 cordis.yml 装载)
