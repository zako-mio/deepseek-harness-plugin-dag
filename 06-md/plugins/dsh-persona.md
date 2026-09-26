# dsh-persona

- 包名: `@deepseek-ai/dsh-persona`
- 分组: G27 Agent 预设
- 拓扑层: Layer 3
- 来源层: L3 其余
- 源码路径: `packages/preset/persona`

## 实现逻辑
作用域级 persona 行：inject=['systemPrompt']，apply() 用 ctx.effect 注册 deployment:persona-prefix 段（order 取 DEPLOYMENT_PERSONA_PREFIX，complete 时令其为完整系统提示）与 deployment:persona-suffix 段（order 取 DEPLOYMENT_PERSONA_SUFFIX）（src/index.ts:62-73）。当 includeRuntimeContext 为假时调用 ctx.systemPrompt.suppressRuntimeContext() 抑制该作用域的运行时上下文快照（src/index.ts:74）。因 dsh-system-prompt 无条件注册部署 persona，本行只能挂载在 agent preset 作用域内遮蔽之，全局挂载会冲突失败（src/index.ts:1-14）。

## Provides
- systemPrompt `deployment:persona-prefix` / `deployment:persona-suffix` 段（作用域级 persona 覆盖，src/index.ts:63-73）

## Depends On (上游依赖)
- `dsh-system-prompt` [E1+E2] - 注册 persona 段落并抑制运行时上下文
  - 证据: `src/index.ts:18-19 import PERSONA_PREFIX_SECTION/PERSONA_SUFFIX_SECTION + src/index.ts:27 inject 'systemPrompt' + src/index.ts:63 ctx.systemPrompt.section`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
