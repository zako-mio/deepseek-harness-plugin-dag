# dsh-sdk-jsonrpc-server

- 包名: `@deepseek-ai/dsh-sdk-jsonrpc-server`
- 分组: G32 SDK 与协议
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/sdk/server`

## 实现逻辑
以 JsonRpcLineTransport 在 stdio 上服务 JSON-RPC：apply() 构造 HarnessSdkJsonRpcServer 并注册 onRequest，initialize 前等待 loader 结算后才宣告就绪，shutdown 在写出响应后 flush/dispose 完整根 runtime 并 exit 0（src/index.ts:46-101）。stdout 专用于协议帧，server.ts 实现请求分发与 agent/session/attachment/llm/subagent 的会话装配（src/server.ts:8-18），并监听 session/event、agent/status、session/created、subagent/end 事件（src/server.ts:95-111）。

## Provides
- SDK JSON-RPC stdio 服务（HarnessSdkJsonRpcServer；initialize 就绪与 shutdown 全量关停）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 经 agent 工厂创建/管理 SDK 会话 agent
  - 证据: `src/server.ts:11 import + src/index.ts:22 static inject (agents)`
- `dsh-llm` [编译依赖] - 处理模型请求/流相关能力
  - 证据: `src/server.ts:13 import`
- `dsh-llm-deepseek-api-key` [编译依赖] - 接入 DeepSeek API key 凭据 seam
  - 证据: `src/server.ts:18 import`
- `dsh-scope` [编译依赖] - 使用作用域能力装配 SDK 运行时
  - 证据: `src/server.ts:14 import`
- `dsh-session` [编译依赖] - 投影会话事件与生命周期到 SDK 结果
  - 证据: `src/server.ts:15 import`
- `dsh-subagent` [编译依赖] - 暴露/跟踪子代理并处理 subagent/end
  - 证据: `src/server.ts:16-17 import`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
