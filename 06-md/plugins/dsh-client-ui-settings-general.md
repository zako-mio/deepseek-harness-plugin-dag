# dsh-client-ui-settings-general

- 包名: `@deepseek-ai/dsh-client-ui-settings-general`
- 分组: G28 设置输入UI
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-general`

## 为什么需要它（设计初衷）
设置所有者非复制/产品引导插件：General 分区、shell 触发器/头 chrome、设置字典与版本化欢迎页。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-settings-general/package.json

## 实现逻辑
Settings 外壳与 ownerless 拷贝：注册 sidebar.settings occupant（SettingsRoot）并声明 settings.trigger/header/action/close/section/onboarding 子槽（index.ts:142-153），注册 General section（settings.section id=general，:170-177）、触发/头部 chrome、SettingsDocumentAction 本地文档、settings 字典。host 半注册 ui-onboarding 持久命名空间（src/index.ts:21-26）。

## Provides
- sidebar.settings occupant (SettingsRoot)
- settings.trigger / settings.header / settings.close / settings.action / settings.section(general) / settings.onboarding 槽注册
- settings 字典命名空间
- ui-onboarding Host 设置命名空间 (welcomeNoticeVersion)

## Depends On (上游依赖)
- `dsh-client-connection` [运行时依赖] - 本地文档 store 依赖 connection.api
  - 证据: `packages/client/ui-settings-general/src/client/index.ts:71-74 (connection.isLoopback + SettingsDocumentStore(connection.api))`
- `dsh-client-ui-layout` [编译依赖] - 说明壳归因避免引用环
  - 证据: `packages/client/ui-settings/src/client/index.ts:8 (注释：shell 依赖 ui-sidebar 会经 ui-layout/ui-theme 形成环，故 shell 归属本包)`
- `dsh-client-ui-settings` [编译依赖] - 消费 settings slot 契约声明与 slots 注册器
  - 证据: `packages/client/ui-settings-general/src/client/index.ts:17 (type-only import), :57 (inject slots), :98 (ctx.slots.getVersion('settings.section'))`
- `dsh-client-ui-sidebar` [编译依赖] - 占用 sidebar 提供的 settings 洞
  - 证据: `packages/client/ui-settings-general/package.json:62 (peerDep ui-sidebar), src/client/index.ts:142 (ctx.slots.inject('sidebar.settings'))`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
