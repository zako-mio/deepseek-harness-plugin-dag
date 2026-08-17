# dsh-tools

- 包名: `@deepseek-ai/dsh-tools`
- 分组: G03 核心服务
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/core/tools`

## 为什么需要它（设计初衷）
作为『一切皆插件』架构的执行中枢，为所有工具插件提供统一的注册表与执行管线：工具插件在此注册 schema 与 executor，管线依次经过 pre-execute 策略门（allow/deny/ask）→ guard → execute 包装（超时/重试/指标）→ post-execute 改写 → 结果冻结，并支持并行/独占并发分类与协作式取消。解决 Agent 框架最核心问题——工具如何被定义、向模型呈现、被策略拦截、被安全执行。

发展史：core 产品组『产品 API 脊梁』之一（stable API），与 session/system-prompt/agent 并列；随仓库 2026-06 起步、2026-08-13 公开。迭代出 Code Mode（run_code 传输）、canonical tool output 契约、render-intent 卡片体系等。

来源：
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/core/tools
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/tool-execution-pipeline.md

## 实现逻辑
工具注册表与执行管线(ctx.tools)。ToolRuntime 服务(static inject ['systemPrompt']) 管理分层工具注册(ScopedLayers)与可见性解析器(view)，按 mode(native/code/both) 决定模型可见工具集；execute() 走 pre-execute → execute → post-execute 三个瀑布(pre 允许/拒绝/询问、execute 包装超时/重试、post 接受/替换/阻断)，最后发 tools/result 观察事件；approval 请求经 ctx.get('approval') 可选 seam 路由，codeRuntime 经 ctx.get('codeRuntime') 可选。

## Provides
- ctx.tools(ToolRuntime)
- tools/pre-execute|tools/execute|tools/post-execute|tools/code-dispatch-log 瀑布事件
- tools/result 观察事件
- tools/change 通知事件
- defineTool/schema.ts 工具定义 API
- ToolExecutionInput/ToolRunContext
- TOOL_RUNTIME_SCHEDULER
- run_code 保留工具(code mode)
- tools-invariant 伴随插件

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - ToolExecutionInput.agent 关联调用归属
  - 证据: `packages/core/tools/src/index.ts:13`
- `dsh-code-runtime-worker-thread` [运行时依赖] - Code Mode 工具经 ctx.get('codeRuntime') 解析运行时, 缺失 loud 报错
  - 证据: `packages/core/tools/src/index.ts:1020-1022`
- `dsh-llm` [编译依赖] - ToolSchema/ContentBlock/HarnessError 类型
  - 证据: `packages/core/tools/src/index.ts:11-12`
- `dsh-session` [编译依赖] - snapshotJsonValue 快照工具参数
  - 证据: `packages/core/tools/src/index.ts:14-15, 102`
- `dsh-system-prompt` [运行时依赖] - static inject systemPrompt
  - 证据: `packages/core/tools/src/index.ts:788, 832-835`
- `dsh-user-approval` [运行时依赖] - ctx.get('approval') 可选 seam：ask 决策转 approval.request
  - 证据: `packages/core/tools/src/index.ts:18-20, 1693, 1706`

## Dependents (下游被依赖)
- `dsh-agent-instructions` - 订阅 tools/result 捕获触碰
- `dsh-agent-loop` - ctx.tools.executionMode 调度工具
- `dsh-agent-spine-demo` - ctx.plugin(ToolRuntime) 工具注册表
- `dsh-agent-tool-presentation` - 呈现模式类型
- `dsh-client-ui-conversation` - Tool 调用 wire 类型契约（tool/call、tool/result）
- `dsh-client-ui-deliverables` - 产物来源为 mutation tools 的 callView.locations（运行时契约）
- `dsh-client-ui-trajectory` - tool 调用轨迹事件类型
- `dsh-cordis-host-runner` - assertSupportedJsonSchema/JsonSchemaNode（inspect manifest 校验）
- `dsh-hooks-claude-code` - tool 前后决策类型
- `dsh-hooks-codex` - tool 前后决策类型
- `dsh-host-apiproxy` - Context merge（ctx.tools）
- `dsh-plan-mode` - exit_plan_mode 工具注册
- `dsh-repeat-tool-reminder` - 监听 tools/post-execute
- `dsh-schedule` - 工具注册
- `dsh-session-checkpoint-policy` - ToolExecutionResult 类型
- `dsh-shell-env` - ToolExecution 类型
- `dsh-spill-policy` - 订阅 tools/post-execute waterfall
- `dsh-subagent` - assertObjectJsonSchema 校验
- `dsh-subagent-spawn-in-process` - 子代理工具链由 agents 工厂提供
- `dsh-tool-ask-user` - 工具注册
- `dsh-tool-bash` - 工具注册管线
- `dsh-tool-bash-persistent` - 工具注册
- `dsh-tool-call-timeout-policy` - inject tools; 监听 tools/execute
- `dsh-tool-cordis` - 工具定义与执行上下文类型
- `dsh-tool-fs` - 工具注册管线
- `dsh-tool-fs-search` - 工具注册与 post-execute 瀑布
- `dsh-tool-goal` - 工具注册
- `dsh-tool-jobs` - 工具注册与执行管道
- `dsh-tool-lsp` - inject ['tools'] 注册工具；defineTool/GenericCallView/ToolExecution 类型(E1)
- `dsh-tool-pwsh` - 工具注册管线
- `dsh-tool-ralph` - defineTool + register
- `dsh-tool-session-query` - 工具注册表：defineTool 契约与注册
- `dsh-tool-skill` - 工具注册
- `dsh-tool-str-replace-editor` - 工具注册管线
- `dsh-tool-subagent` - defineTool + register
- `dsh-tool-subagent-control` - defineTool + register
- `dsh-tool-subagent-report` - childCtx.tools.register
- `dsh-tool-terminal` - 工具注册与 ToolDefinition
- `dsh-tool-todo` - 工具注册
- `dsh-tool-web` - defineTool + register
- `dsh-tool-workflow` - defineTool + register
- `dsh-workflow-worker-thread` - agent() 选项 schema
