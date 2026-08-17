# dsh-client-ui-settings

- 包名: `@deepseek-ai/dsh-client-ui-settings`
- 分组: G28 设置输入UI
- 拓扑层: Layer 10
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings`

## 为什么需要它（设计初衷）
设置域的基础层插件（无自绘 UI 的两角色包）：提供 ctx.settingsScope（每个偏好行绑定的 Host 传输通道/命名空间作用域）并声明 settings.trigger/header/close/action/section/plugins.tab/onboarding 等 slot 契约，让任意拥有偏好的功能包都能读写其命名空间设置。解决'浏览器偏好如何分域、并发安全地读写 Host 设置文档'的机制问题。

发展史：设置域的 base 契约层，与 ui-settings-general（shell 外壳）刻意分离以避免 ui-sidebar→ui-layout→ui-theme 的引用图环。RPC 仅 loopback、单字段写入等限制明确记录为 deferred work。版本 0.1.0-rc.5。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-settings/README.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-settings/package.json

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
