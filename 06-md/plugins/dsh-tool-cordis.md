# dsh-tool-cordis

- 包名: `@deepseek-ai/dsh-tool-cordis`
- 分组: G36 Hooks工具扩展
- 拓扑层: Layer 6
- 来源层: L3 其余
- 源码路径: `packages/extensions/tool-cordis`

## 实现逻辑
Model 面向的 Cordis 运行时/包管理工具集。name='tool-cordis', inject=['tools','systemPrompt','dynamicCordisRunner','cordisInspect']（src/index.ts:26-27）。注册 7 个工具：cordis_inspect_list/query/self、cordis_define、cordis_run、cordis_stop、cordis_undefine（:41-378）；注册 tool:cordis system prompt section（order 115, :36）；经 ctx.cordisInspect.register 注册 Host Inspect Provider（Service/Event/Builtin/Tool, providers.ts:26-64）；agent/pre-step 侦测用户 @pluginId（正则 @([a-z]{3,6}-\d+), :381-398,497-506）注入 DynamicCordisReference 上下文。所有运行时操作走 dsh-cordis-host-runner 的 dynamicCordisRunner（define/run/stop/undefine/reference/snapshot/inspectPlugin/inspectPackage）。presentCall 卡片经 dsh-tools GenericCallView。

## Provides
- 7 个 cordis_* 工具（inspect_list/query/self, define, run, stop, undefine）
- tool:cordis system prompt section (order 115)
- Host Inspect Provider 注册（Service/Event/Builtin/Tool）
- agent/pre-step @pluginId 上下文注入
- inject ['tools','systemPrompt','dynamicCordisRunner','cordisInspect']

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - agent 类型与 pre-step 决策
  - 证据: `packages/extensions/tool-cordis/src/index.ts:7 (Agent/PreStepDecision); package.json:35 (peerDep)`
- `dsh-cordis-host-runner` [运行时依赖] - dynamic Cordis 运行时宿主服务 + inspect registry 服务
  - 证据: `packages/extensions/tool-cordis/src/index.ts:27 (inject ['dynamicCordisRunner','cordisInspect']); :38 (:cordisInspect.register), :55 (:cordisInspect.list), :83 (:cordisInspect.query), :121,126,221,291,344,374,388,459-460 (:dynamicCordisRunner.listPlugins/inspectPlugin/define/run/stop/undefine/reference/snapshot/inspectPackage); package.json:36 (peerDep)`
- `dsh-llm` [编译依赖] - @pluginId 上下文 UserMessage 构造
  - 证据: `packages/extensions/tool-cordis/src/index.ts:12 (createUserMessage); package.json:38 (peerDep)`
- `dsh-session` [编译依赖] - JSON 值/消息类型
  - 证据: `packages/extensions/tool-cordis/src/index.ts:13-14 (JsonValue/UserMessage); package.json:40 (peerDep)`
- `dsh-system-prompt` [运行时依赖] - tool:cordis prompt section 注册
  - 证据: `packages/extensions/tool-cordis/src/index.ts:17 (type-only), :36 (ctx.systemPrompt.section); package.json:41 (peerDep)`
- `dsh-tools` [编译依赖] - 工具定义与执行上下文类型
  - 证据: `packages/extensions/tool-cordis/src/index.ts:15-16 (defineTool/ToolExecution); package.json:42 (peerDep)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
