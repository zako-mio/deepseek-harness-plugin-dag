# dsh-client-ui-cordis

- 包名: `@deepseek-ai/dsh-client-ui-cordis`
- 分组: G14 宿主扩展
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/extensions/ui-cordis`

## 实现逻辑
以 Web 客户端 Cordis 插件形式把动态插件（cordis_define / cordis_run）的 UI 接入客户端：apply() 先构造 CordisDynamicPort，经 ctx.remote.dynamicCordisRunner 读取库存并执行停止/移除 (src/client/index.ts:45-62)；随后建立 inventory，并订阅 remote 转发的 cordis/dynamic-package、cordis/dynamic-retract、cordis/request-run(-resolved) 事件触发刷新，且在连接重置时 reset+refresh (src/client/index.ts:75-84)。最后向 sidebar.footer.action 与 tool.call.toolview 分别注册 CordisPanel 与 cordis_define/cordis_run/cordis_stop/cordis_undefine 工具卡片 (src/client/index.ts:86-145)。

## Provides
- Web 客户端 UI 表面：在 sidebar.footer.action 注入 cordis 动态插件面板，在 tool.call.toolview 注入 cordis_define/cordis_run/cordis_stop/cordis_undefine 工具卡片

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 经 Remote 命名空间同步宿主侧 cordis 事件与库存
  - 证据: `src/client/index.ts:75-80 ctx.remote.$on + src/client/CordisPanel.tsx:13 import`
- `dsh-client-locale` [E1+E2] - 注册本插件的 zh/en 文案字典
  - 证据: `src/client/index.ts:43 ctx.locale.register + src/client/index.ts:6 import`
- `dsh-client-ui-primitives` [编译依赖] - 复用客户端基础 UI 原子组件
  - 证据: `src/client/CordisPreparingRow.tsx:3 import`
- `dsh-client-ui-renderer` [编译依赖] - 接入客户端渲染面类型与能力
  - 证据: `src/client/index.ts:9 import`
- `dsh-client-ui-session` [编译依赖] - 接入会话 UI 集成面
  - 证据: `src/client/index.ts:10 import`
- `dsh-client-ui-sidebar` [编译依赖] - 把 cordis 面板挂载到侧边栏页脚动作位
  - 证据: `src/client/index.ts:86 sidebar.footer.action 注册 + src/client/CordisPanel.tsx:11 import`
- `dsh-client-ui-tool` [E1+E2] - 为 cordis_* 工具调用提供 tool view 卡片渲染
  - 证据: `src/client/index.ts:117-136 tool.call.toolview 注册 + src/client/CordisActionRow.tsx:7 import`
- `dsh-cordis-client-runner` [E1+E2] - 读取客户端运行面快照并驱动审批、启动与停止
  - 证据: `src/client/index.ts:66 ctx.dynamicCordisRunner + src/client/CordisPanel.tsx:12 import`
- `dsh-session` [编译依赖] - 以 SessionId 标识会话作用域的运行卡片
  - 证据: `src/client/index.ts:4 SessionId 类型 import`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
