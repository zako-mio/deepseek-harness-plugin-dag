# dsh-agent-preset

- 包名: `@deepseek-ai/dsh-agent-preset`
- 分组: G27 Agent 预设
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/preset/agent-preset`

## 实现逻辑
作为普通 Cordis 组合中的一行声明式预设：default-export AgentPreset，static inject=['agentPresets']，并设 EntryGroup.key=true 以在其插件激活前保留子表达式（src/index.ts:12-15、:25）。Config 用 schemastery 校验 id/name/description/order 与必填 plugins 数组（src/index.ts:16-23）。初始化时 [Service.init] 调用 ctx.agentPresets.register(this.config) 并把返回的注销器 yield 给 Cordis 以供回收（src/index.ts:27-29）。

## Provides
- 预设声明行（把子插件清单注册进 ctx.agentPresets，src/index.ts:27-29）

## Depends On (上游依赖)
- `cordis-plugin-loader` [编译依赖] - 借用 EntryGroup 语义保留声明式子插件表达式
  - 证据: `src/index.ts:3 import EntryGroup`
- `dsh-agent-preset-registry` [E1+E2] - 把本行声明的预设定义提交给注册表激活
  - 证据: `src/index.ts:5-6 type import PresetDefinition + src/index.ts:13 static inject 'agentPresets' + src/index.ts:28 ctx.agentPresets.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
