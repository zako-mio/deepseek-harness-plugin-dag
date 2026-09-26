# dsh-tool-cordis

- 包名: `@deepseek-ai/dsh-tool-cordis`
- 分组: G14 宿主扩展
- 拓扑层: Layer 6
- 来源层: L2 web-app
- 源码路径: `packages/extensions/tool-cordis`

## 实现逻辑
注册两个只读运行时 API 发现工具：cordis_inspect_list 返回 ctx.cordisInspect.list() 的全部 provider 目录 (src/index.ts:22-39)，cordis_inspect_query 按 platform/provider/method/input 执行只读查询并需 Agent 背书的会话 (src/index.ts:41-72)。host.ts 另把四个 Host Inspect provider 注册进 ctx.cordisInspect：Service/Event 基于生成的 api-catalog 静态目录，Config 从活 Loader 树投影 Config schema，Tool 返回当前 Agent 可见的工具 schema (src/host.ts:16-19, src/providers.ts:39-81, src/config.ts:98-119)。

## Provides
- 工具 cordis_inspect_list / cordis_inspect_query
- Host Inspect provider：Service / Event / Config / Tool

## Depends On (上游依赖)
- `cordis-plugin-loader` [编译依赖] - Config provider 遍历 Loader entry 树并解析条目
  - 证据: `src/config.ts:4 import`
- `dsh-agent` [编译依赖] - 查询需以 Agent 为其作用域主体
  - 证据: `src/index.ts:3 import`
- `dsh-cordis-host-runner` [E1+E2] - 消费宿主 Inspect 注册表以注册 provider 与执行查询
  - 证据: `src/providers.ts:4 import + src/index.ts:10 cordisInspect 由该包提供`
- `dsh-tools` [E1+E2] - defineTool 注册工具并用 ctx.tools 读取 Agent 可见 schema
  - 证据: `src/index.ts:10 inject ['tools','cordisInspect'] + src/index.ts:5 import`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
