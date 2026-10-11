# dsh-subagent

- 包名: `@deepseek-ai/dsh-subagent`
- 分组: G39 子代理
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/subagent/subagent`

## 实现逻辑
本包承担子代理能力 seam 的 Service Definition 角色：`SubagentRuntime` 继承 TypertRemoteService 暴露 `ctx.subagents`，维护命名 provider 注册表（注册即效应、重复名 fail-loud）(src/index.ts:192-198、src/index.ts:543-562)。构造时 `ctx.inject(['agents'])` 绑定 SubagentManager（本地可续跑子代理的启动、结果投递与资源释放），并注入 sessionProjections 注册目录/时序/身份三个投影，另装 archive admission (src/index.ts:207-233)。startActivation 先校验 provider 存在性、maxDepth、能力矩阵、父 Agent 活跃性与 outputSchema，再按 provider 是否具备 prepareContinuable 分派 startExternal/startLocal (src/index.ts:267-282)；sendMessage/interrupt/drainDescendants 等操作全部委托 manager (src/index.ts:308-392)。远端面提供 `@Remote('prompt')` 与 `@Remote('interruptByParent')`，图片先经 attachment store 持久化再投递 (src/index.ts:445-533)。

## Provides
- ctx.subagents（SubagentRuntime：provider 注册表 + 受管子代理启动 API + 本地子代理消息/中断/排水）
- `subagent/provider-added`、`subagent/provider-removed`、`subagent/start`、`subagent/end` 事件
- 远端面 `subagent.prompt` 与 `subagent.interruptByParent`（浏览器/Host 控制通道）
- session projection 定义：子代理目录、时序、身份（含 `subagent/descriptor` durable 事件与结构化输出工具）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 子代理就是 Agent 实体，管理器绑定在 Agent 注册表上
  - 证据: `src/index.ts:40 type Agent + src/index.ts:210 ctx.inject(['agents'], childCtx => new SubagentManager(childCtx, …))`
- `dsh-agent-preset-registry` [编译依赖] - 子代理机会式继承父级预设组合（ctx.get('agentPresets')）
  - 证据: `src/child-agent.ts:27 import type {} from '@deepseek-ai/dsh-agent-preset-registry'`
- `dsh-llm` [编译依赖] - 消息内容与消息源类型贯穿投递路径
  - 证据: `src/index.ts:39 type ContentBlock/MessageId/MessageSource + src/continuation-messages.ts:8-9 import`
- `dsh-permission-presets` [编译依赖] - 子代理继承父级权限预设
  - 证据: `src/child-agent.ts:21 import type {} from '@deepseek-ai/dsh-permission-presets'`
- `dsh-sandbox-policy` [编译依赖] - 委托时机会式消费沙箱策略服务（ctx.get 模式）
  - 证据: `src/child-agent.ts:19 import type {} from '@deepseek-ai/dsh-sandbox-policy'`
- `dsh-session` [编译依赖] - 子代理身份与会话日志读写基于 Session
  - 证据: `src/index.ts:41 type SessionId + src/manager.ts:17-18 import Session/SessionId`
- `dsh-session-projection` [E1+E2] - 子代理目录/时序/身份以 session projection 形式发布
  - 证据: `src/index.ts:225-228 ctx.inject(['sessionProjections']) 注册三个投影 + src/catalog.ts:17 import`
- `dsh-system-prompt` [编译依赖] - 子代理人格/提示段落在创建窗口内 scoped 应用
  - 证据: `src/child-agent.ts:13 import type {} from '@deepseek-ai/dsh-system-prompt'`
- `dsh-tools` [编译依赖] - 校验结构化输出 schema 与子代理工具过滤
  - 证据: `src/index.ts:38 import assertObjectJsonSchema + src/child-agent.ts:14 type ToolRestriction`
- `dsh-user-approval` [编译依赖] - 继承的审批会话事件负载需要该服务类型
  - 证据: `src/child-agent.ts:20 import type {} from '@deepseek-ai/dsh-user-approval'`
- `dsh-working-directory` [运行时依赖] - 解析子代理启动目录
  - 证据: `src/index.ts:197 static inject = ['workingDirectory'] + src/manager.ts:530 ctx.workingDirectory 使用`
- `dsh-workspace` [编译依赖] - 归档准入订阅 workspace 会话活动/停止事件
  - 证据: `src/archive-admission.ts:13 import + src/control-types.ts:13 import type from '@deepseek-ai/dsh-workspace/types'`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 把该业务包的 /remote 命名空间装配进 Client
- `dsh-api-session-controller` - 在会话谱系与快照中标注子 Agent 后代
- `dsh-client-ui-subagent` - 子 Agent 地址与血统类型由 dsh-subagent 定义
- `dsh-client-ui-workspace` - 导航需识别子 Agent 地址以打开子会话
- `dsh-experimental-auto-review` - 类型面需要 subagent 的 Context 声明以读取 in-process 子代理的父会话信息
- `dsh-hooks-claude-code` - 在子 Agent 起止边沿触发 SubagentStart/SubagentStop 钩子，并按 runId 保留子 Agent 以取得其工作目录
- `dsh-schedule` - 拒绝把提醒绑定到委派子会话（投递永远到不了），与委派深度上限共用同一记账
- `dsh-sdk-jsonrpc-server` - 报告子代理起止并在关闭时排空受管子代理
- `dsh-session-reference` - 引入 subagent 投影值的类型以优先使用子代理创建标签作为显示标题
- `dsh-subagent-acp` - provider 契约与注册入口由子代理 seam 提供
- `dsh-subagent-claude-code` - provider 契约、能力常量与注册入口
- `dsh-subagent-codex` - provider 契约、能力常量与注册入口
- `dsh-subagent-dsh-sdk` - provider 契约、能力基线与注册入口
- `dsh-subagent-fork-in-process` - provider 契约与注册入口
- `dsh-subagent-spawn-in-process` - provider 契约与注册入口（子代理 Agent 的构造由子代理 seam 的 manager 负责）
- `dsh-tool-ralph` - 校验并指定每轮新子代理所用的 provider（新鲜、支持结构化输出）
- `dsh-tool-schedule` - 在 dispatch 前拒绝委派子 agent 使用提醒工具，而不只依赖 preset 的工具过滤
- `dsh-tool-subagent` - provider 发现、深度策略解析与子代理启动均由子代理 seam 提供
- `dsh-tool-subagent-control` - 驻留、冷恢复与中断授权全部由子代理服务承担
- `dsh-workflow-ptc` - agent() 钩子通过 subagents seam 的 provider 启动/销毁子 agent，并把结果映射成 ChildResult
