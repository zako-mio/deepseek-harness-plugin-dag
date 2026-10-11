# dsh-tools

- 包名: `@deepseek-ai/dsh-tools`
- 分组: G09 核心运行时
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/core/tools`

## 实现逻辑
以作用域分层注册表实现工具 seam 与执行流水线。ToolRuntime（ctx.tools）用 ScopedLayers 维护工具定义、限制与 guard（src/index.ts:735-778、src/index.ts:834-837），register/restrict/guard/presentAs 均返回精确 disposer（src/index.ts:1069、src/index.ts:1103、src/index.ts:1142、src/index.ts:983）。同一次可见性解析（view）同时喂给提示 schema 提供者、查找与分发，保证模型所见与可调用集合一致（src/index.ts:1017-1050、src/index.ts:1184-1236）。执行按 pre-execute 瀑布 → 审批解析 → tools/execute 瀑布 → post-execute 瀑布推进，含调用方取消信号融合、结果归一化与冻结快照（src/index.ts:1375-1397、src/index.ts:1510-1513、src/index.ts:1610-1613）。ptc 模式经 createRunCodeTool 生成唯一 run_code 传输与语言化 SDK 段，并由 TOOL_RUNTIME_SCHEDULER 符号向 agent-loop 暴露分阶段调度（src/index.ts:481、src/ptc.ts:30）。

## Provides
- ctx.tools（工具注册表与执行流水线，src/index.ts:138-141、src/index.ts:808-822）
- 工具事件词汇：tools/pre-execute、tools/execute、tools/post-execute、tools/ptc-dispatch-log、tools/result、tools/change（src/index.ts:143-210）
- 工具定义与 schema 构造助手：defineTool/validateArgs/parameterSchemaSpecToJsonSchema（src/schema.ts:449、src/schema.ts:478、src/schema.ts:554）
- 内部调度器符号 TOOL_RUNTIME_SCHEDULER 与工具呈现选择 presentAs（src/index.ts:481、src/index.ts:983）
- 工具 UI 呈现视图类型：ToolCallView/ToolResultView（src/presentation.ts:46、src/presentation.ts:140）
- 工具错误类型与中止码：ToolNotFoundError/ToolOutputError/TOOL_ABORTED/TOOL_ABORTED_BEFORE_DISPATCH（src/index.ts:484、src/index.ts:487、src/index.ts:511、src/index.ts:530）
- JSON Schema 校验能力：assertSupportedJsonSchema/validateJsonSchemaValue（src/json-schema.ts:385、src/json-schema.ts:654）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 把调用方 agent 作为工具执行的主体，用于作用域解析、审批路由与 PTC 工作目录归属
  - 证据: `src/index.ts:14 import type { Agent } from '@deepseek-ai/dsh-agent' + src/index.ts:1403 const agent = exec.agent`
- `dsh-llm` [编译依赖] - 复用模型可见的内容块/工具 schema 类型与统一错误基类，保证工具结果可直接入请求历史
  - 证据: `src/index.ts:12 import type { ToolCallId, ContentBlock, ToolSchema } + src/index.ts:13 import { HarnessError }`
- `dsh-sandbox-policy` [E1+E2] - 解析调用方 session 的沙箱策略并下传给受限 PTC 运行时；缺失时响亮失败
  - 证据: `src/index.ts:19 import type {} from '@deepseek-ai/dsh-sandbox-policy' + src/index.ts:958 const policy = this.ctx.get('sandboxPolicy')`
- `dsh-session` [编译依赖] - 承载工具延迟到下一步的上下文消息类型，使工具可声明下一步才可见的输入
  - 证据: `src/index.ts:15 import type { UserMessage } from '@deepseek-ai/dsh-session' + src/index.ts:426 deferContext(context: UserMessage): void`
- `dsh-system-prompt` [E1+E2] - 把可见工具 schema 与 ptc-only/SDK 提示段注册进系统提示组装
  - 证据: `src/index.ts:17 import type { PromptSection, ToolProviderResult } from '@deepseek-ai/dsh-system-prompt' + src/index.ts:855 ctx.systemPrompt.tools(context => this.wireSchemas(context.scope))`
- `dsh-user-approval` [E1+E2] - 把 pre-execute 的 ask 决策路由到人工审批通道；无通道时按契约降级为拒绝
  - 证据: `src/ptc.ts:22 import type { ApprovalService } from '@deepseek-ai/dsh-user-approval' + src/index.ts:1737 const approval = this.ctx.get('approval')`
- `dsh-working-directory` [E1+E2] - 为 Agent 所属的 run_code 解析工作目录；缺失时报错而不是静默使用进程目录
  - 证据: `src/index.ts:7 import type {} from '@deepseek-ai/dsh-working-directory' + src/index.ts:951 const directories = this.ctx.get('workingDirectory')`

## Dependents (下游被依赖)
- `dsh-agent-instructions` - 订阅工具结果事件，从 read/write/edit 的参数中提取被触碰文件路径以触发指令刷新
- `dsh-agent-loop` - 经内部调度器符号准备/派发/收尾工具调用，并按 executionMode 决定串行或并行
- `dsh-agent-preset-registry` - preset 重新挂载后通知工具目录变更
- `dsh-agent-tool-presentation` - 复用工具注册表的按作用域呈现选择 API，把该 preset 的工具形态声明下推给覆盖的 agent
- `dsh-client-ui-chat` - 工具调用与结果类型
- `dsh-client-ui-plan` - 工具调用标识类型
- `dsh-client-ui-tool` - todo 历史重建依赖工具结果类型
- `dsh-client-ui-trajectory` - 工具节点按工具结果元数据投影
- `dsh-cordis-host-runner` - 把沙箱返回的工具定义规范化后注册进真实 Tool 注册表，并在 Inspect 侧校验 JSON Schema 与按 Agent 读取工具 schema
- `dsh-experimental-auto-review` - 以工具预执行为唯一拦截点，决定放行/拒绝/询问，并排除 run_code 外层传输
- `dsh-experimental-browser-use-chrome-devtools-mcp` - 上游工具目录要注册进会话的工具表
- `dsh-experimental-browser-use-playwright-mcp` - 上游工具目录要注册进会话的工具表
- `dsh-experimental-browser-use-stagehand-native` - 注册浏览器工具并接管其执行信号
- `dsh-experimental-claude-code-mods` - mod 的工具注册与 tool.call 拦截都通过 tools seam
- `dsh-experimental-computer-use-cua-driver-mcp` - MCP 工具注册进工具注册表的前提服务
- `dsh-experimental-computer-use-cua-driver-native` - 注册原生工具并接管其执行信号
- `dsh-experimental-tool-agent-team` - 工具定义、输出 schema 校验与作用域注册由 tools seam 提供
- `dsh-experimental-tool-worktree` - 工具定义与注册由 tools seam 提供
- `dsh-file-reference-local` - 查询该 agent 可见的 read 工具，仅在有读取能力时才对模型暴露文件引用提示
- `dsh-hooks-claude-code` - 在工具执行前后拦截点把钩子结果映射成 deny/ask/block 决策与 additionalContexts
- `dsh-hooks-codex` - 把 Codex 钩子的 deny 映射为工具前置 deny 与后置 block/feedback，并附加 additionalContexts
- `dsh-mcp-client` - 把发现的 MCP 工具注册进 harness 工具运行时
- `dsh-mcp-resources` - 注册并注销三条共享资源工具
- `dsh-plan-mode` - 注册常驻的 exit_plan_mode 工具，保持跨模式工具目录不变
- `dsh-plugin-manager` - 向 Agent 暴露 plugin_manager 工具
- `dsh-repeat-tool-reminder` - 订阅工具执行后瀑布点以观察重复调用并附加提醒
- `dsh-schedule` - 编译期契约对齐：提醒工具的 schema/错误码词汇与本包导出的类型共用同一基线；仅声明式依赖
- `dsh-session-checkpoint-policy` - 在工具执行边界做检查点并复用中止错误码
- `dsh-shell-env` - 按一次工具执行上下文解析并贡献环境变量
- `dsh-spill-policy` - 挂载工具结果后处理与 PTC dispatch 日志的 token 保留策略
- `dsh-subagent` - 校验结构化输出 schema 与子代理工具过滤
- `dsh-tool-ask-user` - 工具必须注册进工具注册表才能被模型调用
- `dsh-tool-bash` - 工具必须注册进工具注册表才能被模型调用
- `dsh-tool-bash-persistent` - 工具必须注册进工具注册表
- `dsh-tool-call-timeout-policy` - 包装工具执行瀑布点并读取工具声明的超时预算
- `dsh-tool-cordis` - 注册两个巡检工具定义，并在 Tool Provider 中按 Agent 读取可见工具 schema
- `dsh-tool-fs` - 注册工具定义与参数/输出 schema，并在 execute 期取得 ToolExecution 与渲染钩子
- `dsh-tool-fs-search` - 注册两个工具定义并取得工具执行上下文与结果呈现钩子
- `dsh-tool-goal` - 以 defineTool 定义并注册三个目标工具
- `dsh-tool-jobs` - 以上游工具定义注册三个作业控制工具并挂接 tools/pre-execute 拦截
- `dsh-tool-lsp` - 定义并注册 lsp 工具到工具注册表，复用其 schema/render/presentCall 契约
- `dsh-tool-present` - 工具注册、执行信封与 tools/result 扩展点都由 tools seam 提供
- `dsh-tool-pwsh` - 工具必须注册进工具注册表
- `dsh-tool-pwsh-persistent` - 工具必须注册进工具注册表
- `dsh-tool-ralph` - 注册 ralph 工具定义与结果呈现
- `dsh-tool-schedule` - 以 defineTool 定义四个工具并注册进工具注册表
- `dsh-tool-session-query` - 注册工具定义并消费工具运行上下文
- `dsh-tool-skill` - 注册模型可见工具，并以定义身份判定目录可见性
- `dsh-tool-str-replace-editor` - 通过工具注册表发布 str_replace_editor
- `dsh-tool-subagent` - 注册委托工具并按定义身份判定可见性
- `dsh-tool-subagent-control` - 三个模型可见工具都要注册进工具注册表
- `dsh-tool-terminal` - 声明 tools 服务并注册六个工具定义（含参数 schema、输出 schema、渲染与呈现回调）
- `dsh-tool-todo` - 用 defineTool 定义 schema/输出渲染并把 todo_write 登记进工具注册表
- `dsh-tool-web` - 通过 ctx.tools 注册 web_search/web_fetch 工具定义（含 schema、render、presentationMeta）
- `dsh-tool-workflow` - 用 defineTool 声明参数与 oneOf 输出 schema，并把工具登记进注册表
- `dsh-tool-working-directory` - 把工具定义注册进工具注册表
- `dsh-tool-workspace-dependencies` - 向工具注册表注册其读路径查询工具
- `dsh-user-questions` - 投影读取 tool/call、tool/result 事件需要工具事件类型声明合并
- `dsh-workflow-ptc` - 校验脚本传入的 structured-output schema 属于受支持的 object-rooted JSON Schema 子集
- `dsh-workspace-changes` - 以工具预执行为界把执行信封与会话 recorder 绑定，捕获工具产生的文件改动
