# dsh-client-ui-settings-plugins

- 包名: `@deepseek-ai/dsh-client-ui-settings-plugins`
- 分组: G28 设置输入UI
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-plugins`

## 实现逻辑
插件配置 section：注册 settings.section id=plugins order=15（index.ts:111-119），其 configurable tab(order=0) 声明 settings.plugin.item 槽并渲染三张 host-plane 卡片 bash/agent-loop/web-search（:123-157）。每卡经 ctx.settingsScope.bind 绑定各自命名空间；订阅 credentials/updated 使 webSearch 刷新凭据（:70）。

## Provides
- settings.section 'plugins' 注册 (PluginsSettingsSection)
- settings.plugins.tab 'configurable' + settings.plugin.item 槽
- BashCard / AgentLoopCard / WebSearchCard 三卡片

## Depends On (上游依赖)
- `dsh-api-remotes` [运行时依赖] - 凭据推送失效事件
  - 证据: `packages/client/ui-settings-plugins/src/client/index.ts:70 (ctx.remote.$on('credentials/updated'))`
- `dsh-client-connection` [运行时依赖] - webSearch 卡凭据/校验远程调用
  - 证据: `packages/client/ui-settings-plugins/src/client/index.ts:58 (ctx.get('connection').api)`
- `dsh-client-locale` [编译依赖] - settings.plugins 字典
  - 证据: `packages/client/ui-settings-plugins/src/client/index.ts:14,60 (type-only + locale.register)`
- `dsh-client-ui-settings` [编译依赖] - settings.section 槽声明 + 命名空间 scope 服务
  - 证据: `packages/client/ui-settings-plugins/src/client/index.ts:18 (type-only), :51 (inject settingsScope), :62-64 (ctx.settingsScope.bind)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
