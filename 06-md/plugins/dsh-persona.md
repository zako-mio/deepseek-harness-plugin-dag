# dsh-persona

- 包名: `@deepseek-ai/dsh-persona`
- 分组: G36 Hooks工具扩展
- 拓扑层: Layer 2
- 来源层: L3 其余
- 源码路径: `packages/preset/persona`

## 为什么需要它（设计初衷）
解决『一个 agent 一个身份』的可组合问题：system-prompt 注册表持有 deployment persona 且无条件注册，进程内唯一；此插件提供可在 agent preset 作用域内挂载的 persona 行，遮蔽部署级 persona 或（complete 模式下）独占整个系统提示词，使不同 agent 拥有独立身份。

发展史：定位为『可组合的 persona 行』，只能挂载在 agent preset 作用域内（scope-only），避免与注册表自身 deployment:persona 冲突。支持 text 模板与 includeRuntimeContext 开关。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/preset/persona/README.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-persona

## 实现逻辑
组合式部署人设行（scope-only）。name='persona', inject=['systemPrompt']（src/index.ts:28-31）。挂载在 agent preset 内为单个 agent 遮蔽部署人设：apply 时向 systemPrompt 注册 deployment:persona section（PERSONA_SECTION/PERSONA_ORDER 从 dsh-system-prompt 导入，:23,61-66），config.text 为模板（{{…}} 变量渲染），complete:true 时成为唯一 system prompt（:65），includeRuntimeContext:false 抑制运行时上下文快照（:67）。在 agent scope 之外挂载会与注册表自身的 deployment:persona 冲突并 fail loud。

## Provides
- deployment:persona prompt section 注册（scope-only, order 0）
- complete 模式（该 agent 唯一 system prompt）
- includeRuntimeContext 抑制能力

## Depends On (上游依赖)
- `dsh-system-prompt` [编译依赖] - persona 槽位常量（避免双硬编码漂移）
  - 证据: `packages/preset/persona/src/index.ts:23 (import PERSONA_ORDER/PERSONA_SECTION); package.json:36 (peerDep)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
