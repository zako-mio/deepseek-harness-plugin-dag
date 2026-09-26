# dsh-agent-tool-presentation

- 包名: `@deepseek-ai/dsh-agent-tool-presentation`
- 分组: G09 核心运行时
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/core/agent-tool-presentation`

## 实现逻辑
函数插件（named export `name`/`inject`/`Config`/`apply`，无默认导出）。`apply` 依据 Config 的 mode 在挂载 scope 上调用 `ctx.tools.presentAs('native')`；对 `ptc`/`both` 模式先 `ctx.inject(['ptcRuntime'], ...)` 等待 PTC 运行时再声明呈现，未装配运行时的行在挂载期显式失败 (src/index.ts:59-72)。该行按组合（preset 常驻 scope）而非按会话声明工具呈现模式 (src/index.ts:1-19,27-35)。

## Provides
- 无 ctx 服务；作为 preset 行声明挂载 scope 的工具呈现模式 (native/ptc/both)

## Depends On (上游依赖)
- `dsh-tools` [E1+E2] - 在 scope 上声明该组合的工具呈现模式
  - 证据: `package.json:33 peerDep + src/index.ts:23 import type + src/index.ts:35 inject(['tools']) + src/index.ts:64 ctx.tools.presentAs`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
