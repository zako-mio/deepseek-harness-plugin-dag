# dsh-tools

- 包名: `@deepseek-ai/dsh-tools`
- 分组: G09 核心运行时
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/core/tools`

## 实现逻辑
工具注册表与执行流水线：`ToolRuntime`（服务名 `tools`）用 `ScopedLayers` 维护作用域化工具注册与呈现模式，构造时向 systemPrompt 注册 tool-schema provider，并在非 native 默认模式下注册 PTC 折叠与 SDK section (src/index.ts:807-859)。`register()` 以 ctx.effect 绑定注册所有权 (src/index.ts:1063-1086)；呈现模式由 `presentAs` 按作用域声明并遮蔽全局默认 (src/index.ts:974-999)；执行走 pre/guard/around/post/result 多段 waterfall (src/index.ts:1325,1505,1605,1782)。ptc.ts 实现 `run_code` 传输，经 `ctx.ptcRuntime` 与 `dsh-sandbox` 执行嵌套子调用，审批经 `ctx.get('approval')` 可选消费 (src/index.ts:947,1731; src/ptc.ts:19-22)。schema/json-schema/ts-types/py-types 提供工具参数校验与 TS/Python SDK 渲染；invariant.ts 校验会话内工具调用关系 (src/invariant.ts:77-129)。

## Provides
- ctx.tools (ToolRuntime 工具注册表与执行流水线：register/presentAs/modeFor/调用调度)
- tools/change 事件
- defineTool/JSON Schema 校验与 ToolDefinition/ToolPresentationMode/ToolCallView 等类型
- TS/Python 工具 SDK 渲染 (renderToolsSdk/renderToolsSdkPy/jsonSchemaToTs/jsonSchemaToPy)
- PTC run_code 工具与沙箱升级审批集成

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 复用 Agent 类型以在调度中引用所属 agent
  - 证据: `src/index.ts:13 import type Agent + package.json:41 peerDep`
- `dsh-invariants` [E1+E2] - 注册会话内工具调用关系不变量
  - 证据: `src/invariant.ts:5 import + src/invariant.ts:13 inject(['invariants']) + src/invariant.ts:129 register`
- `dsh-llm` [编译依赖] - 复用工具/内容块/调用 id 类型并构造消息与错误
  - 证据: `src/index.ts:11-12 import + src/ptc.ts:10 createUserMessage/HarnessError`
- `dsh-sandbox-policy` [编译依赖] - 引入沙箱策略服务的上下文类型合并
  - 证据: `src/index.ts:18 import type {} (声明合并)`
- `dsh-scope` [E1+E2] - 以作用域层存储工具注册与呈现模式
  - 证据: `src/index.ts:9-10 import + src/index.ts:833 new ScopedLayers`
- `dsh-session` [E1+E2] - 复用会话消息类型并在 invariant 中读取会话校验工具调用
  - 证据: `src/index.ts:14 import type UserMessage + src/invariant.ts:4 + src/invariant.ts:121 inject(['sessions']) + src/invariant.ts:77 ctx.sessions`
- `dsh-system-prompt` [E1+E2] - 向提示装配注册 tool-schema provider 与 SDK/折叠 section
  - 证据: `src/index.ts:16 import type + src/index.ts:808 inject(['systemPrompt']) + src/index.ts:854 ctx.systemPrompt.tools`
- `dsh-user-approval` [E1+E2] - 可选消费审批服务以处理升级请求
  - 证据: `src/index.ts:21 import type + src/index.ts:947,1731 ctx.get('approval')`

## Dependents (下游被依赖)
- `dsh-agent-instructions` - 从成功的 read/write/edit 工具结果中提取 file_path，把被触及路径转成指令刷新线索
- `dsh-agent-loop` - 调度工具调用执行流水线
- `dsh-agent-preset-registry` - 预设重绑后通知工具目录变更
- `dsh-agent-tool-presentation` - 在 scope 上声明该组合的工具呈现模式
- `dsh-client-ui-chat` - 工具调用节点与调用树
- `dsh-client-ui-plan` - 工具结果类型
- `dsh-client-ui-tool` - 复用工具类型（todo 历史）
- `dsh-client-ui-trajectory` - 工具类型用于工具轨迹定义
- `dsh-cordis-host-runner` - 动态包经 harness 注册的工具须落入 tools 注册表
- `dsh-experimental-auto-review` - 在工具执行前介入并返回 allow/deny/ask/cancel 决策
- `dsh-experimental-browser-use-chrome-devtools-mcp` - 把 MCP 工具注册进工具注册表
- `dsh-experimental-browser-use-playwright-mcp` - 把 MCP 工具注册进工具注册表
- `dsh-experimental-browser-use-stagehand-native` - 注册浏览器工具并接管其执行信号
- `dsh-experimental-computer-use-cua-driver-mcp` - MCP 工具注册进工具注册表的前提服务
- `dsh-experimental-computer-use-cua-driver-native` - 注册原生工具并接管其执行信号
- `dsh-experimental-tool-agent-team` - 注册模型可见工具并声明输出 schema
- `dsh-file-reference-local` - 仅在 read 工具存在时展示 @ 提示词，并在工具结果后使工作区索引失效
- `dsh-hooks-claude-code` - 在工具执行前后拦截点运行 hook 并映射为工具决策
- `dsh-hooks-codex` - 在工具执行前后拦截点运行 hook 并映射为工具决策
- `dsh-mcp-client` - 把发现的 MCP 工具注册进 harness 工具运行时
- `dsh-mcp-resources` - 注册并注销三条共享资源工具
- `dsh-plan-mode` - 注册常驻的 exit_plan_mode 工具
- `dsh-plugin-manager` - 注册面向模型的 plugin_manager 工具
- `dsh-repeat-tool-reminder` - 订阅工具执行后瀑布点以观察重复调用并附加提醒
- `dsh-schedule` - 用 defineTool 向 agent 作用域注册四个 schedule 工具
- `dsh-session-checkpoint-policy` - 在工具执行边界做检查点并复用中止错误码
- `dsh-shell-env` - 按一次工具执行上下文解析并贡献环境变量
- `dsh-spill-policy` - 挂载工具结果后处理与 PTC dispatch 日志的 token 保留策略
- `dsh-subagent` - 校验输出 schema、工具过滤与判定标准 send_message 工具
- `dsh-tool-ask-user` - 注册模型可用工具
- `dsh-tool-bash` - 注册 bash 工具定义并消费工具运行上下文
- `dsh-tool-bash-persistent` - 注册持久 bash 工具定义
- `dsh-tool-call-timeout-policy` - 包装工具执行瀑布点并读取工具声明的超时预算
- `dsh-tool-cordis` - defineTool 注册工具并用 ctx.tools 读取 Agent 可见 schema
- `dsh-tool-fs` - 通过工具注册表发布文件系统工具
- `dsh-tool-fs-search` - 通过工具注册表发布 glob/grep 工具
- `dsh-tool-goal` - 以 defineTool 定义并注册三个目标工具
- `dsh-tool-jobs` - 以上游工具定义注册三个作业控制工具并挂接 tools/pre-execute 拦截
- `dsh-tool-lsp` - 定义并注册 lsp 工具与其输出 schema/渲染
- `dsh-tool-present` - 注册工具并订阅 tools/result
- `dsh-tool-pwsh` - 注册 pwsh 工具定义并消费工具运行上下文
- `dsh-tool-pwsh-persistent` - 注册持久 pwsh 工具定义
- `dsh-tool-ralph` - 注册 ralph 工具定义与结果呈现
- `dsh-tool-session-query` - 注册工具定义并消费工具运行上下文
- `dsh-tool-skill` - 注册 skill 工具并据其在当前 agent 的可见性决定是否发布技能目录
- `dsh-tool-str-replace-editor` - 通过工具注册表发布 str_replace_editor
- `dsh-tool-subagent` - 注册委派工具定义
- `dsh-tool-subagent-control` - 注册控制与发现工具
- `dsh-tool-terminal` - 注册工具定义与 schema
- `dsh-tool-todo` - 注册 todo_write 工具
- `dsh-tool-web` - 通过 ctx.tools 注册 web_search/web_fetch 工具定义（含 schema、render、presentationMeta）
- `dsh-tool-workflow` - 注册 workflow 工具定义与呈现
- `dsh-tool-workspace-dependencies` - 向工具注册表注册其读路径查询工具
- `dsh-workflow-ptc` - 校验 agent() 的结构化输出 schema 是否在支持子集内
- `dsh-workspace-changes` - 在工具执行前捕获文件编辑以覆盖 git 未跟踪路径
