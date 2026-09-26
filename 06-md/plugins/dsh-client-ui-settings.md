# dsh-client-ui-settings

- 包名: `@deepseek-ai/dsh-client-ui-settings`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 10
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings`

## 实现逻辑
提供共享的配置表单与 Host describe 镜像：apply 构造 SettingsSchemaService（ctx.settingsSchema，同步 schema 内省/校验）与 SettingsDescribeMirror（按 remote.$host.isLoopback 决定 host/memory 持久化模式），并在 settings/document-updated 与 connection/reset 时重新 load 镜像（src/client/index.ts:37-52）。随后 new ConfigForms(ctx, { mirror, schema, persistence }) 注册 ctx.configForms（src/client/index.ts:53、config-form.ts:266），为各域表单提供按命名空间的派生视图与串行写入（config-form.ts:50-90）。

## Provides
- ctx.configForms (ConfigForms 服务：按命名空间的配置表单派生视图、describe 镜像与串行写入)
- ctx.settingsSchema (SettingsSchemaService：schemastery schema 反序列化、校验与草稿编辑)
- SettingsDescribeMirror (Host 配置 describe 的共享镜像与失效订阅面)
- 设置页各槽位契约类型（settings.launcher / settings.section / settings.general.item / settings.models.sign-in 等 OwnerProps）

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 读配置 describe 与写 settings 命名空间
  - 证据: `src/client/index.ts:5 import + src/client/index.ts:43 ctx.remote.$on('settings/document-updated')`
- `dsh-settings` [编译依赖] - 设置命名空间与 wire 类型
  - 证据: `src/index.ts:2 import + src/client/config-form.ts:27 import type`

## Dependents (下游被依赖)
- `dsh-client-locale` - 经 configForms 读取持久语言偏好并把 Language 行注册进设置区
- `dsh-client-ui-agent-preset` - 向设置壳注册 agent-presets 段
- `dsh-client-ui-chat` - 注册 Chat 三项 General 设置行
- `dsh-client-ui-conversation` - 读取 Enter 行为等运行时设置
- `dsh-client-ui-deliverables` - 开发者工具开关控制 diff 展示
- `dsh-client-ui-permission-presets` - 设置行使用 ui-settings 的 configForms/describe 面
- `dsh-client-ui-plugin-manager` - 插件配置页复用 ui-settings 的 configForms
- `dsh-client-ui-settings-account` - 读/写 onboarding 等设置命名空间
- `dsh-client-ui-settings-agent-loop` - 经 configForms 服务取得 agent-loop 命名空间的设置表单 scope
- `dsh-client-ui-settings-general` - 设置槽声明与 configForms 镜像由 ui-settings 提供
- `dsh-client-ui-settings-models` - 设置槽声明、settingsSchema/configForms 镜像由 ui-settings 提供
- `dsh-client-ui-settings-plugin-inventory` - 复用 Plugins 设置段的 tab 槽声明
- `dsh-client-ui-settings-plugins` - 复用设置外壳的 section 槽声明
- `dsh-client-ui-settings-shell` - 经 configForms 取得 shell 命名空间的表单 scope
- `dsh-client-ui-settings-subagent` - 经 configForms 取得两个命名空间的表单 scope
- `dsh-client-ui-settings-web-search` - 经 configForms 取得命名空间的表单 scope
- `dsh-client-ui-shortcuts` - 引入设置域槽声明，General 段的 item 槽由其外壳渲染
- `dsh-client-ui-sidebar-documentpreview` - html 预览经设置服务注册其配置表单
- `dsh-client-ui-theme` - 读取/持久化主题偏好并注册 settings.general.item 槽
