# dsh-system-prompt

- 包名: `@deepseek-ai/dsh-system-prompt`
- 分组: G03 核心服务
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/core/system-prompt`

## 实现逻辑
系统提示词装配注册表(ctx.systemPrompt)。SystemPrompt 服务管理分层的 sections/contexts/tools/variables 注册(PromptLayer + ScopedLayers 支持 agent 作用域遮蔽)，assemble() 收集全局+作用域层、按 order 排序、toolOrder 规范工具顺序、插值 {{variable}}，再跑 system-prompt/assemble 瀑布允许插件改写；renderPrompt/renderContextSections 产出最终模型输入。

## Provides
- ctx.systemPrompt(SystemPrompt)
- system-prompt/assemble 瀑布事件
- system-prompt/change 事件
- section()/context()/tools()/variable()/suppressRuntimeContext()/assemble()
- renderPrompt/renderContextSections
- PERSONA_SECTION/PERSONA_ORDER/TOOL_ORDER_REST
- system-prompt-invariant 伴随插件

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - ToolSchema/ContextSnapshotSection 类型
  - 证据: `packages/core/system-prompt/src/index.ts:11`

## Dependents (下游被依赖)
- `dsh-agent` - 监听 system-prompt/assemble 注入模型变量
- `dsh-agent-loop` - ctx.systemPrompt.assemble 装配提示词
- `dsh-agent-presets` - peerDependencies（preset 组合内 prompt 段）
- `dsh-agent-spine-demo` - ctx.plugin(SystemPrompt) 提示词装配
- `dsh-persona` - persona 槽位常量（避免双硬编码漂移）
- `dsh-plan-mode` - plan:policy 段
- `dsh-sandbox-policy` - 策略投影进运行时上下文
- `dsh-tool-cordis` - tool:cordis prompt section 注册
- `dsh-tool-goal` - 模型策略指导
- `dsh-tool-jobs` - 模型跨调用指导
- `dsh-tool-lsp` - inject ['systemPrompt'] 注册指引 section；type-only 模块增强(E1)
- `dsh-tool-ralph` - systemPrompt.section
- `dsh-tool-session-query` - 系统提示 section 注册：模型面向的工具使用指南
- `dsh-tool-subagent` - systemPrompt.section 注册指引
- `dsh-tool-subagent-report` - childCtx.systemPrompt.section
- `dsh-tool-terminal` - 终端使用 prompt 引导
- `dsh-tool-web` - systemPrompt.section
- `dsh-tool-workflow` - systemPrompt.section
- `dsh-tools` - static inject systemPrompt
- `dsh-user-approval` - 向模型暴露 approval policy
- `dsh-web-app` - Context merge（ctx.systemPrompt）
