# dsh-sdk-client

- 包名: `@deepseek-ai/dsh-sdk-client`
- 分组: G31 协议与SDK
- 拓扑层: Layer 2
- 来源层: L3 其余
- 源码路径: `packages/sdk/client`

## 为什么需要它（设计初衷）
解决外部程序如何驱动 harness 的问题：提供以子进程方式经 stdio JSON-RPC 驱动 harness 运行时的 TypeScript 客户端 SDK，分 DeepSeekHarness（高层运行 API）与 HarnessClient（低层协议客户端）两层。其核心价值是让自动化、subagent 后端等非浏览器消费方无需 HTTP/浏览器层即可启动完整 harness 会话并收集结果，与 Python SDK 构成设计孪生。

发展史：位于 packages/sdk/client，与 protocol/server 同属 SDK 三件套；起步即定位为 Python SDK 的 TS 设计孪生，共享同一运行时对端与协议分层，启动规格显式化（command/args），为 headless 与 CI 自动化铺路。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/sdk/client/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/tree/master/python

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
