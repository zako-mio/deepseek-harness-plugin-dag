# dsh-agent-default-model

- 包名: `@deepseek-ai/dsh-agent-default-model`
- 分组: G03 核心服务
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/core/agent-default-model`

## 实现逻辑
默认模型选择服务(ctx.agentDefaultModel)。持有 provider/model/reasoningEffort 组成入口，通过 dsh-settings 的 installSettingsSection 绑定用户层可热更新默认选择；currentSelection() 投影为 dsh-agent 的 ModelSelection，saveSelection() 写回设置文档。

## Provides
- ctx.agentDefaultModel(AgentDefaultModelConfig)
- currentSelection(): ModelSelection
- saveSelection()
- AGENT_DEFAULT_MODEL_SETTINGS_NAMESPACE

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - ModelSelection 类型
  - 证据: `packages/core/agent-default-model/src/index.ts:9`
- `dsh-llm` [编译依赖] - ReasoningEffortId branded 类型
  - 证据: `packages/core/agent-default-model/src/index.ts:10`

## Dependents (下游被依赖)
- `dsh-host-apiproxy` - Context merge（ctx.agentDefaultModel）
