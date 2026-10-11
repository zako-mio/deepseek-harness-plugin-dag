# dsh-agent-tool-presentation

- 包名: `@deepseek-ai/dsh-agent-tool-presentation`
- 分组: G09 核心运行时
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/core/agent-tool-presentation`

## 实现逻辑
以「一行 preset 声明」实现 agent 平面的工具呈现选择。apply() 在 native 模式下直接调用 ctx.tools.presentAs('native') 并按效果自身即 disposer 的方式展开（src/index.ts:63-66）；ptc 模式则先 ctx.inject(['ptcRuntime']) 等待宿主平面的 PTC 运行时，就绪后在子作用域调用 presentAs(config.mode)（src/index.ts:69-71）。因为 presentAs 是按调用作用域登记的，同一进程内 PTC preset 可与 native preset 并存；若部署未组合运行时，该行在挂载期即失败并被 preset 注册表点名为不可用行，而不是拖到首个提示才暴露（src/index.ts:54-71）。Config.mode 为必填，避免「组了这一行却没生效」的静默情况（src/index.ts:38-52）。

## Provides
- 工具呈现模式声明行（native/ptc，按 preset 的常驻作用域对覆盖到的每个 agent 生效，src/index.ts:59-71）

## Depends On (上游依赖)
- `dsh-tools` [E1+E2] - 复用工具注册表的按作用域呈现选择 API，把该 preset 的工具形态声明下推给覆盖的 agent
  - 证据: `src/index.ts:23 import type { ToolPresentationMode } from '@deepseek-ai/dsh-tools' + src/index.ts:64 ctx.tools.presentAs('native')`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
