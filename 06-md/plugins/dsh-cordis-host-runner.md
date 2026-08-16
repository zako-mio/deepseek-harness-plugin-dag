# dsh-cordis-host-runner

- 包名: `@deepseek-ai/dsh-cordis-host-runner`
- 分组: G25 宿主服务
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/extensions/cordis-host-runner`

## 实现逻辑
DynamicCordisRunnerService（TypertRemote）：define/undefine/run/stop 模型装配的动态双半 Cordis 插件包；sandbox.ts VM 求值 host code + guard 门禁，lifecycle.ts 把 host 半挂入 cordis-dynamic group 子 fiber；发 cordis/request-run 审批事件；另提供 cordisInspect 注册表（inspect-registry.ts）。

## Provides
- ctx.dynamicCordisRunner（define/undefine/run/stop/approval）
- ctx.cordisInspect（CordisInspectRegistryService）
- cordis/request-run 事件
- dynamic 相关 Typert Remote

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - Agent 类型（会话所有权）
  - 证据: `packages/extensions/cordis-host-runner/package.json:57; src/index.ts:10`
- `dsh-llm` [编译依赖] - createUserMessage 注入用户上下文
  - 证据: `packages/extensions/cordis-host-runner/package.json:60; src/index.ts:11`
- `dsh-session` [编译依赖] - snapshotJsonValue/JsonValue
  - 证据: `packages/extensions/cordis-host-runner/package.json:62; src/inspect-registry.ts:6-7`
- `dsh-tools` [编译依赖] - assertSupportedJsonSchema/JsonSchemaNode（inspect manifest 校验）
  - 证据: `packages/extensions/cordis-host-runner/src/inspect-registry.ts:8; package.json:63`

## Dependents (下游被依赖)
- `dsh-api-remotes` - dynamicCordisRunner Remote 贡献（供 cordis-client-runner 消费）
- `dsh-client-modules` - fiber 构造/处置标记 dirty 名字，增量扫描 loader entries
- `dsh-client-web` - vendored Loader 挂载与 entry 创建
- `dsh-host-apiproxy` - type-only 引用 client-safe ./types（动态包转发事件，避免环）
- `dsh-tool-cordis` - dynamic Cordis 运行时宿主服务 + inspect registry 服务
