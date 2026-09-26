# dsh-llm

- 包名: `@deepseek-ai/dsh-llm`
- 分组: G23 LLM 适配
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/llm/llm`

## 实现逻辑
抽象出 provider 无关的 ctx.llm 服务：LlmAdapter 注册表加上可被 llm/stream waterfall 拦截的流式调用 API (src/index.ts:342-352, 1135-1157)。registerAdapter/registerConfigurableProviders 以 ctx.effect 做全有或全无的原子路由注册/替换，并在每次拓扑变更发布 llm/adapters-updated (src/index.ts:396-471, 490-543)。prepareCall 冻结一次调用的 config、retryPolicy 与模型元数据并绑定同一适配器注册代，防止 HMR 混用能力 (src/index.ts:936-983)。adapterStream 在最终适配器边界把文件/图像投影为文本句柄、按 model 能力裁剪工具，并把适配器失败归一为终止 chunk (src/index.ts:1033-1122)；invariant.ts 的 companion 校验流语法与适配器注册可读性 (src/invariant.ts:87-104)。

## Provides
- ctx.llm (provider 无关的 LLM 适配器注册表与流式调用 API，供各 llm-* 适配器注册路由、供 agent loop 发起请求)
- llm/stream waterfall 扩展点 (可拦截或短路每次流式模型调用)
- llm/adapters-updated 事件 (适配器路由与目录拓扑变更的非否决通知)

## Depends On (上游依赖)
- `dsh-invariants` [E1+E2] - 注册 llm 包拥有的流协议与注册表不变量 companion
  - 证据: `src/invariant.ts:4 import type InvariantInstaller + src/invariant.ts:112 ctx.invariants.register`

## Dependents (下游被依赖)
- `dsh-acp` - 构造用户消息、错误链与模型目录查询
- `dsh-agent` - 复用 LlmCallConfig/ReasoningEffortId 及 createUserMessage/boundContextSummary 生成模型切换通知
- `dsh-agent-default-model` - 把存储的 effort 字符串投影为适配器推理强度 id
- `dsh-agent-instructions` - 把渲染后的指令文本构造成带 source 标记的 user 消息注入上下文
- `dsh-agent-loop` - 构造并执行模型请求，复用 LlmCallConfig/PreparedLlmCall 等
- `dsh-api-remotes` - 装配 llm 命名空间
- `dsh-api-session-controller` - 消息构造、assistant 流与模型目录
- `dsh-authorization` - AuthorizationError 复用 HarnessError 稳定错误分类
- `dsh-client-connection` - 共享 LLM 相关品牌与类型，用于客户端 API 类型面
- `dsh-client-ui-approval` - 关联工具调用标识类型
- `dsh-client-ui-chat` - assistant 消息/品牌类型
- `dsh-client-ui-conversation` - LLM 消息/请求检查类型
- `dsh-client-ui-deliverables` - presented 结果的消息类型
- `dsh-client-ui-trajectory` - 投影 assistant 流事件与 LLM 类型
- `dsh-client-ui-user-questions` - 引入品牌化 ToolCallId 用于重开计划
- `dsh-command-goal` - 为目标附件构造模型可见的用户消息
- `dsh-commands` - 附件以 LLM 块类型参与模型可见输入
- `dsh-compaction-basic` - 解析路由模型上下文容量以计算压力阈值，并通过 llm 流式调用执行摘要、构造备份检查点消息
- `dsh-compaction-image-offload` - 识别适配器上报的 IMAGE_OFFLOAD_REQUIRED 失败码，并按 dsh-llm 的内容块/消息类型改写图像块
- `dsh-compaction-tool-result-pruner` - 构造不可变的替换工具结果消息并复用其内容块/调用 id 类型
- `dsh-cordis-host-runner` - 运行结果以用户消息源写入会话
- `dsh-experimental-auto-review` - 用当前请求路由调用 reviewer 模型并解析流式块
- `dsh-goal` - 目标消息来源类型合并与 GoalError 的错误基类
- `dsh-goal-round-driver` - 构造模型可见的续轮用户消息与提示块
- `dsh-hooks-claude-code` - 构造注入模型的上下文消息及其来源标签
- `dsh-hooks-codex` - 构造注入模型的上下文消息及其来源标签
- `dsh-llm-deepseek-account` - 复用 provider 无关的错误码与错误类型表达鉴权/配额失败
- `dsh-llm-deepseek-api-key` - 复用共享的 API key 可用性校验与错误类型
- `dsh-llm-pi-ai` - 实现并注册 llm seam 适配器，复用其错误类型、图像投影与目录 API
- `dsh-llm-retry` - 消费 provider 中立失败事实与已解析的重试策略类型
- `dsh-mcp-client` - 校验当前模型路由声明了图像输入能力
- `dsh-mcp-resources` - 把资源结果投影为核心内容块
- `dsh-message-feedback` - 关联消息反馈与 LLM 消息标识契约
- `dsh-plan-mode` - 构造模式切换的用户叙述消息
- `dsh-repeat-tool-reminder` - 构造模型可见的提醒消息及其生产者来源标签
- `dsh-schedule` - 构造 schedule 来源的用户消息并标记 MessageId 品牌
- `dsh-sdk-jsonrpc-server` - 处理模型请求/流相关能力
- `dsh-session` - 复用 llm 消息/工具/请求头等类型与派生消息词汇
- `dsh-session-checkpoint-policy` - 在模型流请求边界做检查点
- `dsh-session-persistence-jsonl` - 复用消息组装/流展开与 errorChain 工具
- `dsh-session-reference` - 构造引用上下文 user 消息、冻结直接消息，并识别 NO_ADAPTER 以回退默认字节预算
- `dsh-session-stats` - 复用 assistantStreamFirstTokenTime 计算首 token 延迟
- `dsh-session-telemetry-otel` - 以 APP_IDENTITY 作为 OTel Resource 的 service.name/version
- `dsh-session-title` - 判定 agent 循环请求并读取 model 路由以驱动生成
- `dsh-session-title-all-prompts-llm` - 经 llm 服务调用模型生成标题
- `dsh-session-title-first-prompt-llm` - 经 llm 服务调用模型生成标题
- `dsh-skill` - 声明合并 dsh-llm 的 MessageSourceMap 以注册 'skill-invocation' 消息来源类型 (src/index.ts:154-159)
- `dsh-spill-policy` - 按当前模型路由估算图像 token 定价，并构造 PTC 图像结果的 additionalContexts 用户消息 (src/index.ts:144)
- `dsh-subagent` - 内容块/流文本处理、推理强度与模型图像能力查询
- `dsh-subagent-acp` - 使用内容块类型
- `dsh-subagent-claude-code` - 使用内容块类型
- `dsh-subagent-codex` - 使用内容块类型
- `dsh-subagent-dsh-sdk` - 内容块与推理强度类型
- `dsh-system-prompt` - 复用工具 schema 与上下文快照类型
- `dsh-time-context` - 构造带来源标记的时间快照 user 消息，并复用消息来源合并类型
- `dsh-tmux-context` - 构造带来源标记的 tmux 位置快照 user 消息，并复用消息来源合并类型
- `dsh-token-meter` - 读取路由图像定价与文件请求文本，并重组 assistant 流以估算 provider 输出
- `dsh-tool-bash` - 用 HarnessError/TOOL_ABORTED 表达工具中止
- `dsh-tool-fs` - 图像以 LLM 可消费的内容部件返回
- `dsh-tool-fs-search` - 搜索结果以 LLM 可消费的内容部件返回
- `dsh-tool-goal` - 构造收尾上下文消息与结构化工具错误
- `dsh-tool-jobs` - 构造带来源标记的用户消息作为完成通知并做长度约束
- `dsh-tool-present` - 事件 payload 使用品牌化 ToolCallId
- `dsh-tool-pwsh` - 用 HarnessError/TOOL_ABORTED 表达工具中止
- `dsh-tool-ralph` - 工具结果呈现使用 dsh-llm 的内容块类型
- `dsh-tool-session-query` - 用 HarnessError 承载模型安全的错误码与拒绝语义
- `dsh-tool-skill` - 用 createUserMessage 构造带 source 的目录/注入消息，并注册 'skill-catalog' 消息来源类型
- `dsh-tool-subagent` - 子代理路由发现与 preflight
- `dsh-tool-subagent-control` - 构造模型可见消息内容块
- `dsh-tool-terminal` - 工具结果内容块类型
- `dsh-tool-web` - 声明式 peer 依赖（模型消息/类型兼容面）
- `dsh-tool-workflow` - 工具呈现使用 dsh-llm 的内容块类型
- `dsh-tools` - 复用工具/内容块/调用 id 类型并构造消息与错误
- `dsh-user-approval` - 把策略切换通知注入模型消息
- `dsh-user-questions` - 错误基类与工具调用 id 类型
- `dsh-web` - 以 dsh-llm 的 HarnessError 为基类定义 WebError，保持全仓错误分类一致
- `dsh-workflow-ptc` - 把子代理最终输出块展平为文本作为 agent() 结果
