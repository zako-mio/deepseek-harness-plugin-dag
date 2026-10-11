# dsh-client-resources

- 包名: `@deepseek-ai/dsh-client-resources`
- 分组: G05 客户端运行时
- 拓扑层: Layer 0
- 来源层: L2 web-app
- 源码路径: `packages/client/resources`

## 实现逻辑
Host 半为空实现，资源模型全在浏览器半 (src/index.ts:1-4)。浏览器半 `apply` 构建 `ResourceRegistry` 并 provide `ctx.resources`，再经 `slots.provideRoot` 贡献 `resource` keyed hook，使任意槽组件获得 `useResource` (src/client/index.ts:30-41)。`resources.ts` 按 `dsh-resource://` 地址维护 per-address 记录，以 holders 引用计数启停 provider 流，并把流帧折叠为 live/failed 快照，记录永不销毁以保证 source() 引用稳定 (src/client/resources.ts:75-211)。

## Provides
- ctx.resources (资源提供者注册表、pin、按地址的 ObservableSnapshot)
- useResource 全局标准 hook (经 slots.provideRoot 贡献给所有槽组件)

## Depends On (上游依赖)
- `dsh-client-ui-renderer` [编译依赖] - 类型面激活 ctx.slots 服务合并，参与渲染机器组装
  - 证据: `src/client/index.ts:7`

## Dependents (下游被依赖)
- `dsh-api-workspace-files` - 客户端 file 资源 provider 注册
- `dsh-client-ui-plan` - 注册 plan 资源提供者
- `dsh-client-ui-sidebar-documentpreview` - 预览把依赖文件注册为资源并按引用计数回收
- `dsh-client-ui-sidebar-right` - 资源型标签打开时对资源加引用钉住
- `dsh-client-ui-subagent` - subagentchat 作为资源类型接入资源模型
