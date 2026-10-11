# dsh-sdk-jsonrpc-server

- 包名: `@deepseek-ai/dsh-sdk-jsonrpc-server`
- 分组: G30 SDK 与协议
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/sdk/server`

## 实现逻辑
以 stdio 上的 JSON-RPC 行传输承载进程外 SDK：apply 构造 JsonRpcLineTransport 与 HarnessSdkJsonRpcServer，把请求分派给 initialize / session/prompt / session/wait / session/working-directory.{get,set} / shutdown 处理器，并在 shutdown 结果写出后 flush、析构根 fiber 并以 0 退出 (src/index.ts:45-100, src/server.ts:324-351)。initialize 校验 reasoningEffort 与 maxTokens，按需挂载 DeepSeek 回退适配器并解析调用配置 (src/server.ts:154-188)；prompt 把编码图片经 attachment 存储落成引用后投递用户消息 (src/server.ts:195-212, src/server.ts:46-59)。服务器构造时订阅 session/event、agent/error、agent/status、session/created、subagent/end，把生命周期转换为 session.event / session.status / subagent.started / subagent.finished 通知 (src/server.ts:102-146)。wait 会等待 agent 空闲与受管子代理排空，并在无后续耐久终态时抛出活失败 (src/server.ts:221-238)；shutdown 摘除订阅、排空子代理、释放适配器与句柄后再返回 (src/server.ts:279-315)。

## Provides
- SDK JSON-RPC 协议面 (stdio 上的 initialize/session.prompt/session.wait/session.working-directory/shutdown 方法与服务端通知)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 创建 SDK 拥有的 agent 会话并在每次投递前校验句柄仍存活
  - 证据: `package.json:35 peerDep + src/server.ts:11 import；src/server.ts:241 ctx.agents.get`
- `dsh-llm` [E1+E2] - 构造用户消息并解析 provider/model/reasoningEffort 调用配置
  - 证据: `package.json:37 peerDep + src/server.ts:13 import createUserMessage；src/server.ts:174 ctx.get('llm')`
- `dsh-llm-deepseek-api-key` [E1+E2] - provider 无适配器且为 deepseek-official 时按需挂载回退适配器
  - 证据: `package.json:38 peerDep + src/server.ts:19 import * as LlmDeepSeek；src/server.ts:171 ctx.plugin(LlmDeepSeek)`
- `dsh-session` [E1+E2] - 订阅已提交会话事件并读取会话标识类型
  - 证据: `package.json:41 peerDep + src/server.ts:15 import type SessionId/SessionLogOffset；src/server.ts:102 ctx.on('session/event')`
- `dsh-subagent` [E1+E2] - 报告子代理起止并在关闭时排空受管子代理
  - 证据: `package.json:42 peerDep + src/server.ts:17-18 import SubagentRuntime/SubagentRunEndInfo；src/server.ts:128 ctx.on('subagent/end')、src/server.ts:226 ctx.get('subagents')`
- `dsh-working-directory` [E1+E2] - 实现 SDK 的会话工作目录读取与切换方法
  - 证据: `package.json:43 peerDep + src/server.ts:16 import type {}；src/server.ts:253 ctx.workingDirectory.ensure`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
