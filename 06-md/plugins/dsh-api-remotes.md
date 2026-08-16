# dsh-api-remotes

- 包名: `@deepseek-ai/dsh-api-remotes`
- 分组: G26 客户端runtime
- 拓扑层: Layer 6
- 来源层: L2 web-app
- 源码路径: `packages/api/remotes`

## 实现逻辑
Remote BFF 装配与 Host Agent/Session lookup 策略。index.ts（host 面）：空 apply，仅通过 API_REMOTE_FORWARDED_EVENTS satisfies TypertForwardableEvent[] 做编译期形状门（forwarded event 必须是已声明事件、不能绑定 Scope、必须单向）。agent-lookup.ts：createApiRemoteAgentResolver 构建共享解析器——live Agent 复用、cold session 经 inspectApiRemoteSession(持久化检查)后 resume 一次/身份、subagent-owned 身份保留 agent-busy fence；ctx.inject(['typert']) 配置 agent/session Typert lookups。client/index.ts：platform-neutral 装配——ctx.remote.$mount 挂载 commands/goals/dynamicCordisRunner/pluginInventory/messageFeedback 五个 Remote 命名空间，type-only 再导出传输与负载词汇。

## Provides
- ctx.remote（browser: TypertClientRemote 装配面）
- agent/session Typert lookups + host agent context 配置（host）
- API_REMOTE_FORWARDED_EVENTS allowlist（11 个事件）
- createApiRemoteAgentResolver / hasApiRemoteSubagentOwner

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - Agent 类型与 ctx.agents.get/resume/isOwnedBy 服务（:70-71,128,162）
  - 证据: `packages/api/remotes/src/agent-lookup.ts:4（import type { Agent… } from '@deepseek-ai/dsh-agent'）；peerDependencies`
- `dsh-api-gateway` [编译依赖] - client 面声明依赖网关 client（remote 装配需要其类型面）
  - 证据: `packages/api/remotes/package.json dsh.client.inject: ['@deepseek-ai/dsh-api-gateway']；src/client/index.ts:45（import type {} from '@deepseek-ai/dsh-api-gateway/client'）`
- `dsh-cordis-host-runner` [编译依赖] - dynamicCordisRunner Remote 贡献（供 cordis-client-runner 消费）
  - 证据: `packages/api/remotes/src/index.ts:11（import type {} from '@deepseek-ai/dsh-cordis-host-runner/types'）；client/index.ts:6（import dynamicRemote）`
- `dsh-session` [编译依赖] - SessionHeader/SessionEvent/SessionId 类型与 ctx.sessions.get 服务（:139）
  - 证据: `packages/api/remotes/src/agent-lookup.ts:5（import type { Session… } from '@deepseek-ai/dsh-session'）；peerDependencies`
- `dsh-typert-registry` [运行时依赖] - 配置 Agent/Session Typert lookups
  - 证据: `packages/api/remotes/src/agent-lookup.ts:199（ctx.inject(['typert'])）、:205-207（typeCtx.typert.lookups.configure）`

## Dependents (下游被依赖)
- `dsh-client-locale` - settings 刷新 remote 通道
- `dsh-client-runtime` - 类型面（remote 合并）
- `dsh-client-ui-conversation` - ctx.remote 远程调用底座（conversation 事件经 connection 传输）
- `dsh-client-ui-cordis` - host 端动态插件生命周期 Remote 调用与事件推送
- `dsh-client-ui-goal` - goal 域 Remote 端点（host goals 服务）
- `dsh-client-ui-message-feedback` - host messageFeedback Remote（dsh-message-feedback 域的生成端点）
- `dsh-client-ui-model-selection` - 模型目录加载与选择提交
- `dsh-client-ui-settings` - settings 命名空间读写走 Host wire
- `dsh-client-ui-settings-models` - 订阅 settings/credentials/adapters 失效事件
- `dsh-client-ui-settings-plugin-inventory` - remote 面与转发事件键
- `dsh-client-ui-settings-plugins` - 凭据推送失效事件
- `dsh-client-ui-theme` - settings 刷新 remote 通道
- `dsh-client-ui-tool` - remote 类型底座
- `dsh-client-ui-user-questions` - 提问应答负载类型
- `dsh-cordis-client-runner` - dynamicCordisRunner Remote 命名空间——声明的注入让页面在 host 半不可达时不加载浏览器半
- `dsh-host-apiproxy` - ApiRemote* 会话/子代理转发事件
