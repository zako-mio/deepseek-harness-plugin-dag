# dsh-sdk-client

- 包名: `@deepseek-ai/dsh-sdk-client`
- 分组: G31 协议与SDK
- 拓扑层: Layer 2
- 来源层: L3 其余
- 源码路径: `packages/sdk/client`

## 实现逻辑
TypeScript 客户端 SDK（纯库，不注册 Cordis 服务）：spawn 子进程运行 dsh-jsonrpc-agent runtime，经 stdio JSON-RPC 驱动 agent turns。DeepSeekHarness 为高层 turn API，HarnessClient 为底层协议客户端；封装 dsh-sdk-protocol 的 JsonRpcLineTransport 请求-响应帧并扇出 notifications（订阅过滤）；invariant.ts 注册包属伴随插件。

## Provides
- DeepSeekHarness/HarnessSession 高层 turn API
- HarnessClient 底层协议客户端
- JsonRpcResponseError 再导出
- RunOptions/HarnessClientOptions/HarnessNotification 类型
- sdk-client-invariant 伴随插件

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - ContentBlock 类型
  - 证据: `packages/sdk/client/src/client.ts:23, packages/sdk/client/src/types.ts:8`
- `dsh-session` [编译依赖] - SessionEvent 类型
  - 证据: `packages/sdk/client/src/api.ts:12, packages/sdk/client/src/types.ts:9`

## Dependents (下游被依赖)
- `dsh-subagent-dsh-sdk` - DeepSeekHarness/HarnessNotification 驱动子 runtime
