# dsh-client-ui-settings

- 包名: `@deepseek-ai/dsh-client-ui-settings`
- 分组: G28 设置输入UI
- 拓扑层: Layer 10
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings`

## 实现逻辑
Settings 域基础插件：browser 半注册 ctx.settingsScope 服务（SettingsScopeBinder，settings-scope.ts:227-232），定义 settings 表面规范 slot 契约（contract/slots.ts:53-88：settings.section/plugins.tab/onboarding/general.item）。host 半为空 apply。不依赖任何 ui-* 呈现包，任意偏好拥有者经 ctx.settingsScope.bind 读写 Host settings 命名空间（api.settings.mutate）。

## Provides
- ctx.settingsScope (SettingsScopeBinder 服务)
- settings 规范 slot 契约 (settings.section / settings.plugins.tab / settings.onboarding / settings.general.item 等类型声明)

## Depends On (上游依赖)
- `dsh-api-remotes` [运行时依赖] - settings 命名空间读写走 Host wire
  - 证据: `packages/client/ui-settings/src/client/settings-scope.ts:121 (api.settings.mutate 远程调用)`
- `dsh-client-runtime` [编译依赖] - SnapshotStore/uSES 状态基建
  - 证据: `packages/client/ui-settings/src/client/settings-scope.ts:16-17 (import createSnapshotStore from runtime/client)`

## Dependents (下游被依赖)
- `dsh-client-locale` - 持久化语言偏好
- `dsh-client-ui-agent-preset` - Settings 槽声明与命名空间 scope
- `dsh-client-ui-conversation` - settingsScope 服务承载 busy-Enter 设置绑定
- `dsh-client-ui-permission-presets` - General 行槽声明
- `dsh-client-ui-settings-general` - 消费 settings slot 契约声明与 slots 注册器
- `dsh-client-ui-settings-models` - settings.section 槽声明与 settingsScope 契约
- `dsh-client-ui-settings-plugin-inventory` - settings.plugins.tab 槽声明
- `dsh-client-ui-settings-plugins` - settings.section 槽声明 + 命名空间 scope 服务
- `dsh-client-ui-theme` - 持久化主题偏好（settings 文档）
