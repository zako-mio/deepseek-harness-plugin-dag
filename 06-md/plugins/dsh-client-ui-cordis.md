# dsh-client-ui-cordis

- 包名: `@deepseek-ai/dsh-client-ui-cordis`
- 分组: G27 会话交互UI
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/extensions/ui-cordis`

## 为什么需要它（设计初衷）
Cordis 动态插件浏览器端：全局面板操作 host 持有的每个定义 + 只读 cordis_define 卡片记录会话定义。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/extensions/ui-cordis/README.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-client-ui-cordis

## 实现逻辑
cordis 动态插件管理 UI。建立 CordisDynamicPort 经 ctx.remote.dynamicCordisRunner Remote 调 stopFromPanel/undefineFromPanel/inventory；createCordisInventory 订阅 remote.$on('cordis/dynamic-package'|'dynamic-retract'|'request-run'|'request-run-resolved') 与 connection/reset 刷新；注册 sidebar.footer.action id=cordis-panel（CordisPanel：inventory/activeRuns/approve/decline/startUserRun）；注册 tool.call.toolview keyed cordis_define/cordis_run（含 tool.view.cordis keyed child）/cordis_stop/cordis_undefine；以 InputTriggerSource 注册 '@' cordis 源（@pluginId 引用）。

## Provides
- sidebar.footer.action id=cordis-panel(CordisPanel)
- tool.call.toolview keyed cordis_define/cordis_run/cordis_stop/cordis_undefine
- InputTriggerSource '@' cordis（@pluginId 候选/lexicon）
- slot 声明: tool.view.cordis(keyed)

## Depends On (上游依赖)
- `dsh-api-remotes` [运行时依赖] - host 端动态插件生命周期 Remote 调用与事件推送
  - 证据: `index.ts:45-59 ctx.remote.dynamicCordisRunner.stopFromPanel/undefineFromPanel/inventory + index.ts:73-78 remote.$on`
- `dsh-client-connection` [运行时依赖] - 连接重置时刷新 inventory
  - 证据: `index.ts:79-82 ctx.on('connection/reset')`
- `dsh-client-locale` [编译依赖] - 命名空间字典
  - 证据: `index.ts:5 type-only + index.ts:41 locale.register`
- `dsh-client-runtime` [编译依赖] - 客户端运行时与会话上下文
  - 证据: `index.ts:3 ClientContext,SessionId + package.json:57`
- `dsh-client-ui-input-trigger` [运行时依赖] - 注册 '@' cordis 引用源（@pluginId）
  - 证据: `index.ts:8 InputTriggerService + index.ts:167-168 slash.registerSource(source)`
- `dsh-client-ui-sidebar` [编译依赖] - 消费 sidebar.footer.action 座位声明
  - 证据: `index.ts:6 type-only ui-sidebar/client + package.json:59`
- `dsh-client-ui-tool` [编译依赖] - 消费 tool.call.toolview 座位注册业务 Tool 卡片
  - 证据: `index.ts:4 type-only ui-tool/client + package.json:62 peerDependencies`
- `dsh-cordis-client-runner` [运行时依赖] - 浏览器侧 cordis runner 服务：运行状态快照与 approval 对账
  - 证据: `index.ts:36 inject 'remote.dynamicCordisRunner','dynamicCordisRunner' + index.ts:64-71 ctx.dynamicCordisRunner 快照/approve/reconcileApprovals`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
