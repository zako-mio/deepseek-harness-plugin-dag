# dsh-tool-cordis

- 包名: `@deepseek-ai/dsh-tool-cordis`
- 分组: G14 宿主扩展
- 拓扑层: Layer 6
- 来源层: L2 web-app
- 源码路径: `packages/extensions/tool-cordis`

## 实现逻辑
以「只读巡检工具 + Host Provider 注册」实现：apply 注册 cordis_inspect_list 与 cordis_inspect_query 两个 defineTool，前者返回 ctx.cordisInspect.list() 的 Provider 目录，后者按 platform/provider/method/input 调 ctx.cordisInspect.query 并把结果包成 {platform, provider, method, data}，两者都要求 Agent 会话 (src/index.ts:21-73)。另有 ./host 入口 cordis-inspect-providers，在 Host 组合中一次性注册 Service/Event/Config/Tool 四个 Provider，其中 Tool Provider 用 ctx.tools.schemas(agent) 返回该 Agent 可见工具，Config Provider 从运行中的 Loader 树投影原生 Schemastery Config (src/host.ts:16-19, src/providers.ts:39-82, src/config.ts:28-38)。

## Provides
- ctx.tools (注册 cordis_inspect_list 与 cordis_inspect_query 两个只读运行时巡检工具)
- ctx.cordisInspect (host 入口注册 Service/Event/Config/Tool 四个 Host Inspect Provider)

## Depends On (上游依赖)
- `cordis-plugin-loader` [编译依赖] - 以 Loader 条目类型遍历运行中的插件树，投影每个条目的 Config 状态
  - 证据: `package.json:36 peerDep + src/config.ts:4 import Entry`
- `dsh-agent` [编译依赖] - 从工具执行上下文取得 Agent，巡检结果按该 Agent 的作用域收敛
  - 证据: `package.json:37 peerDep + src/index.ts:3 import Agent + src/index.ts:12-15 requireAgent`
- `dsh-cordis-host-runner` [E1+E2] - 向 Host Inspect 注册表登记四个 Provider，并让工具侧通过 ctx.cordisInspect 列出与执行只读查询
  - 证据: `package.json:39 peerDep + src/providers.ts:4 import HostCordisInspectProviderRegistration + src/host.ts:7 inject 'cordisInspect' + src/host.ts:18 ctx.cordisInspect.register`
- `dsh-tools` [E1+E2] - 注册两个巡检工具定义，并在 Tool Provider 中按 Agent 读取可见工具 schema
  - 证据: `package.json:40 peerDep + src/index.ts:5-6 import defineTool/ToolExecution + src/index.ts:10 inject 'tools' + src/index.ts:22/41 ctx.tools.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
