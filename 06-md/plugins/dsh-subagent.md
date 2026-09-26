# dsh-subagent

- 包名: `@deepseek-ai/dsh-subagent`
- 分组: G41 子代理
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/subagent/subagent`

## 实现逻辑
定义子代理 seam 服务 ctx.subagents（SubagentRuntime）：命名 provider 注册表加 capability 校验的 start()、startContinuable()、sendMessage()、prompt/interruptByParent 远程面与 listChildren/listDescendants 发现 API (src/index.ts:199-661)。continuation.ts 管理可续子代理的稳定 id、descriptor 持久化、冷恢复与消息路由 (src/continuation.ts:82-550)；child-agent.ts 统一 in-process 子代理的深度、血缘、策略播种与作用域组合 (src/child-agent.ts:50-280)。catalog/projection 记录并投影父目录子项身份，lifecycle 统一发射 subagent/start|end 生命周期边 (src/catalog.ts:143-165, src/projection.ts:68-190, src/lifecycle.ts:101-219)。

## Provides
- ctx.subagents (子代理 seam 服务定义：命名 provider 注册表 + 启动/续跑/消息/中断/发现 API)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 创建与检索子 Agent、读取其会话与状态
  - 证据: `src/index.ts:40 (import type Agent) + src/child-agent.ts:12 (import type Agent,AgentOptions,CreateAgentOptions) + src/index.ts:217 (ctx.inject(['agents'])) + src/continuation.ts:210 (ctx.agents.get)`
- `dsh-agent-preset-registry` [E1+E2] - 让子代理加入父的 preset 组合
  - 证据: `src/child-agent.ts:29 (type import) + src/child-agent.ts:205 (ctx.get('agentPresets')?.composeFrom)`
- `dsh-invariants` [E1+E2] - 注册 provider 注册表与 start/end 配对不变量
  - 证据: `src/invariant.ts:4 (import type InvariantFailure, InvariantInstaller) + src/invariant.ts:12 (inject ['invariants']) + src/invariant.ts:92 (ctx.invariants.register)`
- `dsh-llm` [E1+E2] - 内容块/流文本处理、推理强度与模型图像能力查询
  - 证据: `src/descriptor.ts:26 (import type ReasoningEffortId) + src/assistant-output.ts:13 (import joinAssistantStreamText) + src/continuation.ts:515 (ctx.get('llm'))`
- `dsh-permission-presets` [E1+E2] - 继承 auto/full-access 权限预设身份
  - 证据: `src/child-agent.ts:23 (type import) + src/child-agent.ts:250 (ctx.get('permissionPresets')?.current)`
- `dsh-sandbox-policy` [E1+E2] - 捕获父会话沙箱覆盖并播种给子代理
  - 证据: `src/child-agent.ts:21 (type import) + src/child-agent.ts:253 (ctx.get('sandboxPolicy')?.overrideOf)`
- `dsh-scope` [E1+E2] - 按委派父级做作用域过滤的事件派发
  - 证据: `src/index.ts:36-37 (import scopeTarget, Scoped) + src/index.ts:216 (scopeTarget(this, parent))`
- `dsh-session` [E1+E2] - 读写会话事件、会话 id 与会话注册表
  - 证据: `src/descriptor.ts:25 (import type SessionEvent) + src/types.ts:15 (import type SessionEvent,SessionId) + src/list-children.ts:69 (ctx.get('sessions'))`
- `dsh-session-projection` [E1+E2] - 注册父目录、身份与时长投影
  - 证据: `src/catalog.ts:17 (import type ProjectionDefinition) + src/index.ts:228 (ctx.inject(['sessionProjections'])) + src/index.ts:230 (projections.register)`
- `dsh-system-prompt` [E1+E2] - 为子代理注册委派作用域上下文与 persona 段
  - 证据: `src/child-agent.ts:15 (type import) + src/child-agent.ts:206 (childCtx.systemPrompt.context)`
- `dsh-tools` [E1+E2] - 校验输出 schema、工具过滤与判定标准 send_message 工具
  - 证据: `src/index.ts:38 (import assertObjectJsonSchema) + src/types.ts:16 (import type ObjectJsonSchema,ToolRestriction) + src/continuation.ts:179 (ctx.get('tools')?.get('send_message'))`
- `dsh-user-approval` [E1+E2] - 将子代理审批策略固定为 never
  - 证据: `src/child-agent.ts:22 (type import) + src/child-agent.ts:254 (ctx.get('approval'))`
- `dsh-workspace` [E1+E2] - 响应工作区归档准入与活动上报
  - 证据: `src/archive-admission.ts:13 (import type SessionActivity, SessionActivityItem) + src/archive-admission.ts:23 (ctx.on('workspace/session-activity')) + src/archive-admission.ts:30 (ctx.on('workspace/session-stop'))`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配 subagent 命名空间与客户端类型
- `dsh-api-session-controller` - 子代理所有权与客户端地址类型
- `dsh-client-ui-subagent` - 子代理地址/模式类型
- `dsh-client-ui-workspace` - 导航到子代理会话地址
- `dsh-experimental-auto-review` - 解析子 Agent 的直接父指令初始提示边界
- `dsh-hooks-claude-code` - 把子代理 start/end 映射到 SubagentStart/SubagentStop hook
- `dsh-sdk-jsonrpc-server` - 暴露/跟踪子代理并处理 subagent/end
- `dsh-session-reference` - 引入 subagent 投影值的类型以优先使用子代理创建标签作为显示标题
- `dsh-subagent-acp` - 复用 seam 契约并注册 acp provider
- `dsh-subagent-claude-code` - 复用 seam 契约与共享辅助并注册 provider
- `dsh-subagent-codex` - 复用 seam 契约与共享辅助并注册 provider
- `dsh-subagent-dsh-sdk` - 复用 seam 契约与共享辅助并注册 provider
- `dsh-subagent-fork-in-process` - 实现并注册 fork provider
- `dsh-subagent-spawn-in-process` - 实现并注册 spawn provider
- `dsh-tool-ralph` - 校验并指定每轮新子代理所用的 provider（新鲜、支持结构化输出）
- `dsh-tool-subagent` - 启动子代理并复用 seam 辅助
- `dsh-tool-subagent-control` - 转发消息/中断并复用相邻 Agent 工具标记
- `dsh-workflow-ptc` - 为脚本的 agent() 钩子启动/等待/释放子代理
