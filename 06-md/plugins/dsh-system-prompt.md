# dsh-system-prompt

- 包名: `@deepseek-ai/dsh-system-prompt`
- 分组: G09 核心运行时
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/core/system-prompt`

## 实现逻辑
系统提示装配注册表：`SystemPrompt`（服务名 `systemPrompt`）以 `ScopedLayers` 维护 section/context/tool-provider/variable 四类作用域层，构造时注册若干内建 section (src/index.ts:405-450)。`section/context/tools/variable` 分别在调用上下文作用域内注册贡献 (src/index.ts:454-547)；`assemble()` 合并全局与作用域 provider、脱离 tool 参数并按序产出权威装配 (src/index.ts:549-585)。对外声明 `system-prompt/assemble` 瀑布与 `system-prompt/change` 事件 (src/index.ts:18-38)；invariant.ts 前置校验装配结果的 section/context/tool/variable 合法性 (src/invariant.ts:16-51)。

## Provides
- ctx.systemPrompt (SystemPrompt 装配注册表：section/context/tools/variable/assemble/getSectionOrder)
- system-prompt/assemble 瀑布与 system-prompt/change 事件
- PromptSection/PromptContext/PromptAssembly/ToolProviderResult/AssembleContext 类型

## Depends On (上游依赖)
- `dsh-invariants` [E1+E2] - 注册提示装配结果合法性不变量
  - 证据: `src/invariant.ts:4 import + src/invariant.ts:13 inject(['invariants']) + src/invariant.ts:60 register`
- `dsh-llm` [编译依赖] - 复用工具 schema 与上下文快照类型
  - 证据: `src/index.ts:11 import type ContextSnapshotSection/ToolSchema`
- `dsh-scope` [E1+E2] - 以作用域层存储并合并各作用域的提示贡献
  - 证据: `src/index.ts:9-10 import AnonymousEntries/NamedEntries/ScopedLayers/scopeTarget`

## Dependents (下游被依赖)
- `dsh-agent` - assembleContextFor 返回 AssembleContext，并向该类型声明合并 agent 字段
- `dsh-agent-loop` - 注册 provider/model/cwd 提示变量并驱动提示装配
- `dsh-agent-preset-registry` - 在模型组装水线校验 Agent 已加入某预设
- `dsh-client-ui-deliverables` - 注册 Web 文件引用指引节
- `dsh-experimental-browser-use-chrome-devtools-mcp` - 在 system prompt 中声明浏览器能力
- `dsh-experimental-browser-use-playwright-mcp` - 在 system prompt 中声明浏览器能力
- `dsh-experimental-browser-use-stagehand-native` - 注入 Stagehand 使用与安全 guidance
- `dsh-experimental-computer-use-cua-driver-native` - 注入桌面操作 guidance 段落
- `dsh-experimental-tool-agent-team` - 注入 Team 协作策略段落
- `dsh-mcp-client` - 把服务端 attributed instructions 写入系统提示段
- `dsh-mcp-resources` - 发布资源服务器清单提示段
- `dsh-persona` - 注册 persona 段落并抑制运行时上下文
- `dsh-sandbox-policy` - 向模型请求注入解析后的文件策略文本
- `dsh-session-reference` - 在系统提示装配完成后捕获 provider/model 变量作为引用字节预算的模型来源
- `dsh-subagent` - 为子代理注册委派作用域上下文与 persona 段
- `dsh-tool-bash` - 注入 bash 交叉调用指引段落
- `dsh-tool-fs` - 向系统提示注入工具使用指引
- `dsh-tool-fs-search` - 向系统提示注入搜索工具使用指引
- `dsh-tool-goal` - 注册目标工具策略段并按序插入系统提示词
- `dsh-tool-jobs` - 注入 tool:jobs 段系统提示，指导模型跟踪/收集后台作业
- `dsh-tool-lsp` - 注入 lsp 工具的模型可见使用指导段落
- `dsh-tool-pwsh` - 注入 pwsh 交叉调用与 Windows 退出码指引段落
- `dsh-tool-ralph` - 注册 ralph 的显式请求使用策略提示章节
- `dsh-tool-session-query` - 注入会话检索工具的使用引导段落
- `dsh-tool-subagent` - 为可续后台委派注册提示段
- `dsh-tool-terminal` - 注入终端使用指引段落
- `dsh-tool-web` - 注册工具使用与外部内容信任指引的 system prompt 章节
- `dsh-tool-workflow` - 注册 workflow 工具的使用策略提示章节
- `dsh-tools` - 向提示装配注册 tool-schema provider 与 SDK/折叠 section
- `dsh-user-approval` - 声明当前审批策略的模型可见上下文
