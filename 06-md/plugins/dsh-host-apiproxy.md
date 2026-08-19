# dsh-host-apiproxy

- 包名: `@deepseek-ai/dsh-host-apiproxy`
- 分组: G25 宿主服务
- 拓扑层: Layer 7
- 来源层: L2 web-app
- 源码路径: `packages/host/apiproxy`

## 为什么需要它（设计初衷）
所有客户端共用的 API 网关：TS 契约 + fetch 载体 + 网关插件，承载 session/host/events RPC。RC7：设置域去白名单化、分页切页逻辑修复、图片批量写入改 saveImages()。

发展史：RC8 HOME目录~缩写 + 图片上传统一准入

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/host/apiproxy/README.md

## 实现逻辑
api-proxy.ts:135-137 图片上传改用 attachment 包新 admitEncodedImages(ctx.attachments) 统一准入(替换原内联decodeBase64); :2853 host信息新增 home: homedir()，供前端以~缩写HOME目录。

## Provides
- ctx.apiProxy（ApiProxy 网关：sessions/subagents/workspace/host/goals/skills/agentPresets/settings/credentials/llm/events/downloads/respond）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - installModelSelection/Agent 类型，模型切换实现
  - 证据: `packages/host/apiproxy/src/api-proxy.ts:10-11`
- `dsh-agent-default-model` [编译依赖] - Context merge（ctx.agentDefaultModel）
  - 证据: `packages/host/apiproxy/src/index.ts:17`
- `dsh-agent-presets` [编译依赖] - resolveSessionPreset/preset 错误类型（agentPresets.* 域）
  - 证据: `packages/host/apiproxy/src/api-proxy.ts:31-36; package.json:79`
- `dsh-api-gateway` [组合依赖] - E3 override：row id api-gateway 覆盖 base 层 api-gateway 行（name 换为 dsh-host-apiproxy）
  - 证据: `packages/bundle/web-app/cordis.patch.yml:97-100`
- `dsh-api-remotes` [编译依赖] - ApiRemote* 会话/子代理转发事件
  - 证据: `packages/host/apiproxy/src/api-proxy.ts:102-110`
- `dsh-cordis-host-runner` [编译依赖] - type-only 引用 client-safe ./types（动态包转发事件，避免环）
  - 证据: `packages/host/apiproxy/src/api-proxy.ts:76`
- `dsh-goal` [编译依赖] - GoalError/GoalRef（goals 域）
  - 证据: `packages/host/apiproxy/src/api-proxy.ts:68-69`
- `dsh-llm` [编译依赖] - createUserMessage/freezeMessage/ReasoningEffortId（llm 域）
  - 证据: `packages/host/apiproxy/src/api-proxy.ts:15-17`
- `dsh-session` [编译依赖] - Session/SessionEvent/SessionId 类型
  - 证据: `packages/host/apiproxy/src/api-proxy.ts:18-19`
- `dsh-session-projection` [编译依赖] - Context merge（ctx.sessionProjections）
  - 证据: `packages/host/apiproxy/src/api-proxy.ts:60-61`
- `dsh-session-projection-cache` [编译依赖] - Context merge（ctx.sessionProjectionCache）
  - 证据: `packages/host/apiproxy/src/api-proxy.ts:65-66`
- `dsh-session-title` [编译依赖] - SessionTitleInvalidError
  - 证据: `packages/host/apiproxy/src/api-proxy.ts:84-85`
- `dsh-skill` [编译依赖] - isUserInvocable（skills 域）
  - 证据: `packages/host/apiproxy/src/api-proxy.ts:24,77`
- `dsh-subagent` [编译依赖] - SubagentError/SubagentListEntry 类型
  - 证据: `packages/host/apiproxy/src/api-proxy.ts:22-23`
- `dsh-tools` [编译依赖] - Context merge（ctx.tools）
  - 证据: `packages/host/apiproxy/src/api-proxy.ts:37`
- `dsh-user-approval` [编译依赖] - ApprovalOutcome/ApprovalRequestId
  - 证据: `packages/host/apiproxy/src/api-proxy.ts:88-91`
- `dsh-user-questions` [编译依赖] - AskUserQuestion* 类型
  - 证据: `packages/host/apiproxy/src/api-proxy.ts:97-100`
- `dsh-workspace` [编译依赖] - workspace 域值类型与错误
  - 证据: `packages/host/apiproxy/src/api-proxy.ts:25-29`

## Dependents (下游被依赖)
- `dsh-client-connection` - /api 的 dispatch 面——未拦截方法 fallback 到 apiProxy
- `dsh-client-runtime` - wire 层常量（search 结果上限）
- `dsh-session-log-export` - 浏览器下载控制器 fetch /api/session.export，由网关 downloads.sessionLog 端点服务
