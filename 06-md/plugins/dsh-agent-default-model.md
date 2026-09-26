# dsh-agent-default-model

- 包名: `@deepseek-ai/dsh-agent-default-model`
- 分组: G09 核心运行时
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/core/agent-default-model`

## 实现逻辑
实现 `AgentDefaultModelConfig`（服务名 `agentDefaultModel`），为未显式指定模型的 Agent 提供默认模型选择 (src/index.ts:48-95)。构造时经 `ctx.inject(['settings'], ...)` 关闭 settings 自动模式，并把 provider/model/reasoningEffort 三个 volatile Config 字段投影为 `ModelSelection` (src/index.ts:34-42,57-61)。`currentSelection()` 读取当前默认选择 (src/index.ts:67-73)；`saveSelection()` 在部署装配了 configEditor 时按提交顺序串行写入 profile，无 editor 时保留组合项 (src/index.ts:82-94)。

## Provides
- ctx.agentDefaultModel (默认模型选择服务：currentSelection 读取与 saveSelection 持久化)
- AgentDefaultModelConfig 服务类与 Config 字段 (provider/model/reasoningEffort)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 复用 Agent 侧的 ModelSelection 选择类型
  - 证据: `package.json:34 peerDep + src/index.ts:12 import type ModelSelection`
- `dsh-config-editor` [E1+E2] - 将默认模型选择持久化写入 profile
  - 证据: `package.json:31 dependency + src/index.ts:14 import type + src/index.ts:85 ctx.get('configEditor')`
- `dsh-llm` [编译依赖] - 把存储的 effort 字符串投影为适配器推理强度 id
  - 证据: `package.json:35 peerDep + src/index.ts:13 import ReasoningEffortId`
- `dsh-settings` [E1+E2] - 关闭 settings 自动模式并使默认模型从 settings 读取
  - 证据: `src/index.ts:6 import type + src/index.ts:60 ctx.inject(['settings'])`

## Dependents (下游被依赖)
- `dsh-api-session-controller` - 读取/保存部署默认模型
