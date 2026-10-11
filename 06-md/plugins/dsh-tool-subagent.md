# dsh-tool-subagent

- 包名: `@deepseek-ai/dsh-tool-subagent`
- 分组: G39 子代理
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/subagent/tool-subagent`

## 实现逻辑
把 `ctx.subagents` 的某个具名 provider 暴露为模型侧委托工具：apply 校验 maxDepth/toolFilter 配置，先注册 model-selection 投影，再监听 `subagent/provider-added`/`-removed` 动态挂载或卸载工具定义，并按 provider 的 `inheritsParentContext` 选择“继承会话”或“自包含任务”两套措辞 (src/index.ts:163-230、src/index.ts:356-385)。execute 里做模型选择预检：解析父/配置/请求三方路由、按策略校验可选模型，必要时经 `ctx.get('llm')` 预飞子路由，然后调用 `ctx.subagents.startActivation` 并把 childId 作为 activation 结果返回 (src/index.ts:280-342)。开启 modelSelectionSettings 时按 composition scope 对每个 Agent 单独 install/remove，监听 agent/created、agent/disposed 与 tools/change 做协调 (src/index.ts:388-490)。

## Provides
- ctx.tools 上的委托工具定义（默认名 `subagent`，按 provider 生成措辞与可选模型选择参数）
- system prompt 片段 `tool:subagent`（并行委派指引，按可见工具定义动态生成）
- 子代理模型选择 session projection 与可选的 `list_subagent_models` 工具
- `subagent-model-selection-settings` 配置入口（web-app 装配的 Host 设置采样）

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 委托需要精确的活跃父 Agent 与父子路由继承
  - 证据: `src/index.ts:14 import type { Agent, AgentOptions } + src/index.ts:281 const parent = exec.agent`
- `dsh-llm` [编译依赖] - 子代理模型路由与内容块类型
  - 证据: `src/index.ts:15-16 import ReasoningEffortId/ContentBlock + src/index.ts:307 runtimeCtx.get('llm') 预检路由`
- `dsh-session` [编译依赖] - 按会话采样并记录子代理模型选择
  - 证据: `src/index.ts:17-18 import SessionSeq/type Session + src/index.ts:400 selectForSession(target: Session)`
- `dsh-session-projection` [E1+E2] - 模型选择策略以 session projection 持久化
  - 证据: `src/index.ts:174 ctx.sessionProjections.register(...) + src/model-selection-state.ts:5 import`
- `dsh-subagent` [E1+E2] - provider 发现、深度策略解析与子代理启动均由子代理 seam 提供
  - 证据: `src/index.ts:23 import type SubagentProvider + src/index.ts:201 ctx.subagents.getProvider + src/index.ts:334 ctx.subagents.startActivation`
- `dsh-system-prompt` [运行时依赖] - 注册并行委派提示片段
  - 证据: `src/index.ts:41 inject 'systemPrompt' + src/index.ts:372 runtimeCtx.systemPrompt.section({ name: `tool:${toolName}` })`
- `dsh-tools` [E1+E2] - 注册委托工具并按定义身份判定可见性
  - 证据: `src/index.ts:12-13 import defineTool/ToolDefinition + src/index.ts:41 inject 'tools' + src/index.ts:345 ctx.tools.register`

## Dependents (下游被依赖)
- `dsh-subagent-claude-code` - 该后端必须与委托工具一起装配，模型侧才有入口启动它
- `dsh-subagent-codex` - 必须与委托工具同装配，模型侧才能启动该后端
