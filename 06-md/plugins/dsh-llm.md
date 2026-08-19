# dsh-llm

- 包名: `@deepseek-ai/dsh-llm`
- 分组: G04 LLM核心
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/llm/llm`

## 为什么需要它（设计初衷）
为 DeepSeek Harness 定义供应商中立的 LLM 词汇与抽象服务：消息/内容块/流式 chunk 协议 + LlmRuntime 适配器注册表与单一流式调用 API。agent loop、会话日志与所有插件都以它作为模型交互的规范语言；真实适配器（deepseek-official、pi-ai）实现同一 LlmAdapter 接口，llm/stream waterfall 事件供缓存/日志/路由拦截。RC7 引入 ReplayEnvelope 统一回放元数据契约，assembler 确保截断时回放块与结果一致。

发展史：RC8 修复图片累计载荷过高 + 取消流式后回复前缀保留

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/llm/llm/README.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-llm
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md

## 实现逻辑
content.ts:92+ 新增 offloadRequestImages: 按base64长度收集请求内全部图片(含tool-result嵌套)，超 maxRequestImageBytes 时按流序替换最旧图片为 OFFLOADED_IMAGE_TEXT 占位，解决图片累计载荷过高致请求失败。assembler.ts:159-177 新增 interruptedBlocks(): 流被取消时保留已流出的text/reasoning前缀，供agent-loop落地中断回复。

## Provides
- ctx.llm(LlmRuntime)
- llm/stream 瀑布事件
- llm/adapters-updated 通知事件
- registerAdapter/registerConfigurableProviders/registerModelDiscovery
- LlmAdapter 抽象基类
- LlmError/HarnessError
- BlockAssembler(max-tokens 截断同步修剪 replay.blocks)
- ReplayEnvelope 类型(finish.replayState)
- createUserMessage/createAssistantMessage/createToolResultMessage
- llm-invariant 伴随插件

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-agent` - LlmCallConfig/ReasoningEffortId 类型
- `dsh-agent-default-model` - ReasoningEffortId branded 类型
- `dsh-agent-instructions` - createUserMessage
- `dsh-agent-loop` - llm.prepareCall/stream 发起模型调用
- `dsh-agent-spine-demo` - ctx.plugin(LlmRuntime) LLM 服务
- `dsh-commands` - 命令图文输入模型处理
- `dsh-compaction-basic` - summarizeWithLlm 经 ctx.llm.stream()
- `dsh-compaction-tool-result-pruner` - freezeMessage
- `dsh-cordis-host-runner` - createUserMessage 注入用户上下文
- `dsh-experimental-agent-team` - teammate模型推理
- `dsh-goal-round-driver` - createUserMessage
- `dsh-hooks-claude-code` - hook 输出构造 UserMessage 上下文
- `dsh-hooks-codex` - hook 输出构造上下文
- `dsh-host-apiproxy` - createUserMessage/freezeMessage/ReasoningEffortId（llm 域）
- `dsh-llm-deepseek` - inject ['llm']：registerAdapter
- `dsh-llm-pi-ai` - inject ['llm']：registerAdapter 等
- `dsh-llm-retry` - LlmFailure/ResolvedRetryPolicy 类型
- `dsh-lsp-stdio` - assertNever 穷尽检查
- `dsh-message-feedback` - peerDependencies（生成 typert 产物引用）
- `dsh-repeat-tool-reminder` - createUserMessage
- `dsh-sandbox-local` - assertNever
- `dsh-schedule` - 提醒渲染类型
- `dsh-sdk-client` - ContentBlock 类型
- `dsh-sdk-jsonrpc-server` - createUserMessage 构造消息
- `dsh-session` - import deepFreeze 冻结事件/头, Message/UserMessage 类型定义事件载荷
- `dsh-session-checkpoint-policy` - StreamChunk 类型
- `dsh-session-persistence-sqlite` - 打包StreamChunk类型
- `dsh-session-reference` - 构造附加 UserMessage 载荷与事件类型穷尽
- `dsh-session-stats` - isTokenDelta 判定首 token
- `dsh-session-telemetry-otel` - APP_IDENTITY
- `dsh-session-title` - isAgentLoopRequest
- `dsh-session-title-all-prompts-llm` - llm 服务：辅助模型调用生成标题
- `dsh-session-title-first-prompt-llm` - LLM 服务调用
- `dsh-skill` - assertNever + MessageSourceMap 注入
- `dsh-subagent-acp` - ContentBlock 类型
- `dsh-subagent-claude-code` - ContentBlock 类型
- `dsh-subagent-codex` - ContentBlock 类型
- `dsh-subagent-dsh-sdk` - ContentBlock 类型
- `dsh-system-prompt` - ToolSchema/ContextSnapshotSection 类型
- `dsh-time-context` - 构造注入的 UserMessage 载荷
- `dsh-tmux-context` - 构造注入的 UserMessage 载荷
- `dsh-token-meter` - BlockAssembler/deepFreeze；TokenUsage 类型
- `dsh-tool-call-timeout-policy` - ToolExecutionResult 类型
- `dsh-tool-cordis` - @pluginId 上下文 UserMessage 构造
- `dsh-tool-fs` - read_image 能力门控
- `dsh-tool-lsp` - assertNever
- `dsh-tool-session-query` - HarnessError 错误契约（工作区未授权报错）
- `dsh-tool-skill` - createUserMessage + MessageSourceMap
- `dsh-tool-subagent-control` - assertNever
- `dsh-tool-terminal` - 输出内容块类型
- `dsh-tool-web` - ContentBlock/assertNever 类型
- `dsh-tools` - ToolSchema/ContentBlock/HarnessError 类型
- `dsh-user-approval` - createUserMessage
- `dsh-user-questions` - HarnessError 基类
- `dsh-web` - 类型/错误基类声明依赖
