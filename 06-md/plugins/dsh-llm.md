# dsh-llm

- 包名: `@deepseek-ai/dsh-llm`
- 分组: G22 LLM 适配
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/llm/llm`

## 实现逻辑
提供者中立的 LLM seam：LlmRuntime 维护 provider→adapter 注册表与可配置 provider 目录，registerAdapter / registerConfigurableProviders 以 effect 作用域注册并支持全量校验后原子 replace（冲突时不改变现状）(src/index.ts:389-536)。stream() 经 llm/stream waterfall 进入 adapterStream，完成适配器选择、模型元数据校验、调用配置默认化、文件/图片投影与工具更新投影，并把适配器失败收敛为终结 finish 块（reason 为 aborted 或 error）(src/index.ts:1041-1157, src/index.ts:1160-1169)。prepareCall 把一次调用的配置、重试策略与适配器代际绑定为一次性 handle，使 HMR 或设置变更不会混用两代能力 (src/index.ts:933-991)。另定义 LlmAdapter 抽象基类、消息/内容块词汇、重试策略 schema 解析与 BlockAssembler 等公共构件 (src/index.ts:208-291, src/retry-policy.ts:100-195)。

## Provides
- ctx.llm (LlmRuntime：适配器注册、模型目录与发现、流式调用与 prepareCall)
- Cordis 事件 llm/stream（waterfall 拦截每次流式调用）与 llm/adapters-updated（拓扑变更通知）
- LlmAdapter 抽象基类与 StreamChunk/GenerateOptions/ContentBlock 等提供者词汇
- 重试策略模型 RetryPolicySchema / resolveRetryPolicy（供各 provider 配置内嵌）
- 消息与内容块工具（createUserMessage、freezeMessage、projectFilesToText、BlockAssembler 等）

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-acp` - 构造模型选择控制并探测当前路由的图像输入能力
- `dsh-agent` - 复用 LLM 的消息、工具调用与模型选择类型，使 agent 选项与请求配置对齐
- `dsh-agent-default-model` - 把存储的 effort 字符串投影为适配器推理强度 id
- `dsh-agent-instructions` - 构造承载指令文本的 user 角色消息，并扩展 MessageSourceMap 声明 agent-instructions 源
- `dsh-agent-loop` - 调用模型流式接口、构造 assistant/tool-result 消息并复用 LlmError 与失败分类
- `dsh-api-remotes` - 把该业务包的 /remote 命名空间装配进 Client
- `dsh-api-session-controller` - 构建模型目录与推理档选项
- `dsh-authorization` - 授权错误继承 HarnessError，复用统一的错误分类与展示
- `dsh-client-connection` - 浏览器 API 复用 LLM 品牌与类型
- `dsh-client-product-analytics` - 事件属性中的模型标识类型
- `dsh-client-ui-approval` - 关联工具调用标识类型
- `dsh-client-ui-chat` - LLM 品牌与消息类型
- `dsh-client-ui-conversation` - 助手记录与请求检查类型
- `dsh-client-ui-deliverables` - 助手消息标识类型
- `dsh-client-ui-plan` - 计划内容的模型类型
- `dsh-client-ui-trajectory` - assistant 节点按 LLM 流块与首 token 时刻投影
- `dsh-client-ui-user-questions` - 卡片以 ToolCallId 品牌类型关联工具调用
- `dsh-command-goal` - 为目标附件构造模型可见的用户消息
- `dsh-commands` - 准入后的附件以 LLM 内容块类型交给命令处理器
- `dsh-compaction-basic` - 解析路由模型上下文容量以计算压力阈值，并通过 llm 流式调用执行摘要、构造备份检查点消息
- `dsh-compaction-image-offload` - 识别适配器上报的 IMAGE_OFFLOAD_REQUIRED 失败码，并按 dsh-llm 的内容块/消息类型改写图像块
- `dsh-compaction-tool-result-pruner` - 构造不可变的替换工具结果消息并复用其内容块/调用 id 类型
- `dsh-cordis-host-runner` - 构造带 cordis-host-runner 来源标记的用户消息向模型汇报运行结果，并校验动态工具的渲染内容块
- `dsh-experimental-auto-review` - 审查请求经 llm seam 以会话当前 provider/model 路由发出，流式结果由 BlockAssembler 解析
- `dsh-experimental-claude-code-mods` - $.session 的消息构造与 callId 品牌类型来自 llm 包
- `dsh-experimental-session-inspector` - 会话日志行需要按 llm 的流式块与消息类型解释
- `dsh-goal` - GoalError 继承 HarnessError 携带稳定 code；目标轮次消息来源沿用 LLM 消息来源词汇
- `dsh-goal-round-driver` - 构造并渲染模型可见的目标轮次提示与用户消息
- `dsh-hooks-claude-code` - 构造携带 hooks-claude-code 来源标记的用户消息，把钩子 additionalContext 注入模型上下文
- `dsh-hooks-codex` - 构造带 hooks-codex 来源标记的用户消息，承载钩子产出的 additionalContext
- `dsh-llm-deepseek-account` - 复用 provider 无关的错误码与错误类型表达鉴权/配额失败
- `dsh-llm-deepseek-api-key` - 适配器必须注册进 LLM seam 才能被路由与发现
- `dsh-llm-pi-ai` - 实现 LlmAdapter 并注册进 LLM seam 才能服务请求
- `dsh-llm-retry` - 失败事实与解析后的重试策略类型由 LLM seam 定义
- `dsh-mcp-client` - 校验当前模型路由声明了图像输入能力
- `dsh-mcp-resources` - 把资源结果投影为核心内容块
- `dsh-message-feedback` - 关联消息反馈与 LLM 消息标识契约
- `dsh-plan-mode` - 构造模式切换旁白消息并声明 plan-mode 消息来源映射
- `dsh-repeat-tool-reminder` - 构造模型可见的提醒消息及其生产者来源标签
- `dsh-sandbox-local` - 编译期依赖基线对齐（沙箱 provider 与工具/llm 层共用同一工作区依赖图）；仅声明式依赖
- `dsh-schedule` - 以 schedule 来源构造投递消息，并用 MessageId 记录投递回执身份
- `dsh-sdk-jsonrpc-server` - 构造用户消息并解析 provider/model/reasoningEffort 调用配置
- `dsh-session` - 把事件日志折叠成 LLM 请求所需的消息历史与工具历史类型
- `dsh-session-checkpoint-policy` - 在模型流请求边界做检查点
- `dsh-session-persistence-jsonl` - 错误链格式化与 assistant 流展开以比对恢复后的行
- `dsh-session-reference` - 构造引用上下文 user 消息、冻结直接消息，并识别 NO_ADAPTER 以回退默认字节预算
- `dsh-session-stats` - 复用 assistantStreamFirstTokenTime 计算首 token 延迟
- `dsh-session-telemetry-otel` - 取产品身份写入 OTel resource 属性
- `dsh-session-title` - 识别主循环请求并读取其 provider/model 路由
- `dsh-session-title-all-prompts-llm` - 声明 llm 服务依赖，并按路由支持的最低 reasoning effort 为标题调用选择推理档
- `dsh-session-title-first-prompt-llm` - 解析模型信息并选择 reasoning effort
- `dsh-skill` - 声明合并 dsh-llm 的 MessageSourceMap 以注册 'skill-invocation' 消息来源类型 (src/index.ts:154-159)
- `dsh-spill-policy` - 按当前模型路由估算图像 token 定价，并构造 PTC 图像结果的 additionalContexts 用户消息 (src/index.ts:144)
- `dsh-subagent` - 消息内容与消息源类型贯穿投递路径
- `dsh-subagent-acp` - 把模型内容块转换为 ACP 内容块
- `dsh-subagent-claude-code` - 把模型内容块/结果文本转换为 SDK 输入输出
- `dsh-subagent-codex` - 内容块与消息类型用于构造/解析协议载荷
- `dsh-subagent-dsh-sdk` - 内容块与结果文本用于协议载荷
- `dsh-system-prompt` - 复用 LLM 的工具 schema 与上下文快照类型，使组装结果可直接作为模型输入
- `dsh-time-context` - 构造时间快照 user 消息，并声明 time-context 消息源参与上下文形成
- `dsh-tmux-context` - 构造带来源标记的 tmux 位置快照 user 消息，并复用消息来源合并类型
- `dsh-token-meter` - 读取路由图像定价与文件请求文本，并重组 assistant 流以估算 provider 输出
- `dsh-tool-bash` - 中止时抛出带 TOOL_ABORTED 码的 HarnessError
- `dsh-tool-fs` - 解析当前路由模型是否声明 image 输入（严格能力闸门），并构造图像内容块
- `dsh-tool-fs-search` - SearchError 以 HarnessError 为基类，携带稳定 code 供重试/权限/UI 层分流
- `dsh-tool-goal` - 构造收尾上下文消息与结构化工具错误
- `dsh-tool-jobs` - 构造带来源标记的用户消息作为完成通知并做长度约束
- `dsh-tool-lsp` - 编译期契约对齐：工具结果经 dsh-tools 呈现时与 llm 内容类型同一基线；仅声明式依赖
- `dsh-tool-present` - 会话事件里的 callId 使用 llm 的 branded ToolCallId 类型
- `dsh-tool-pwsh` - 中止时抛 TOOL_ABORTED 结构化错误
- `dsh-tool-ralph` - 工具结果呈现使用 dsh-llm 的内容块类型
- `dsh-tool-schedule` - 工具结果渲染函数返回 llm 内容块，保证输出形状与其它工具一致
- `dsh-tool-session-query` - 用 HarnessError 承载模型安全的错误码与拒绝语义
- `dsh-tool-skill` - 目录与注入消息需要 LLM 消息源类型扩展
- `dsh-tool-subagent` - 子代理模型路由与内容块类型
- `dsh-tool-subagent-control` - 构造要投递的消息内容
- `dsh-tool-terminal` - 构造模型可见的文本内容块作为工具结果
- `dsh-tool-web` - 声明式 peer 依赖（模型消息/类型兼容面）
- `dsh-tool-workflow` - 结果渲染卡片类型需要 llm 的内容块词汇
- `dsh-tools` - 复用模型可见的内容块/工具 schema 类型与统一错误基类，保证工具结果可直接入请求历史
- `dsh-user-approval` - 策略切换以用户消息注入会话，并复用 LLM 的 ToolCallId brand
- `dsh-user-questions` - 构造回流用户消息并使用 LLM 的 brand 与内容块类型
- `dsh-web` - 以 dsh-llm 的 HarnessError 为基类定义 WebError，保持全仓错误分类一致
- `dsh-workflow-ptc` - 无 schema 的 agent() 结果需要把子 agent 的 llm 内容块压平成文本
- `dsh-working-directory` - 构造 source 为 working-directory 的模型可见变更通知
