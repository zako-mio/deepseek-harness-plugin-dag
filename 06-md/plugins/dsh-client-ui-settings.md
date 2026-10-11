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
- `dsh-client-ui-agent-preset` - 占用 settings.section 声明
- `dsh-client-ui-chat` - 注册三条通用设置行
- `dsh-client-ui-conversation` - 注册提交行为设置行
- `dsh-client-ui-deliverables` - 设置槽位类型
- `dsh-client-ui-permission-presets` - 注册 General 设置行
- `dsh-client-ui-plugin-manager` - 配置表单投影类型
- `dsh-client-ui-settings-account` - 经共享配置表单读写引导进度与 developerTools 偏好
- `dsh-client-ui-settings-agent-loop` - 读取 agent-loop 命名空间的共享配置表单并做暂存/保存
- `dsh-client-ui-settings-general` - Developer Tools 行与本地文档动作经共享配置表单镜像读写
- `dsh-client-ui-settings-models` - 页面经共享配置表单镜像读取命名空间与 revision，并在其推送下刷新
- `dsh-client-ui-settings-plugin-inventory` - 拉入 settings.plugins.tab 槽声明的类型合并（本包不注入 configForms）
- `dsh-client-ui-settings-plugins` - 复用设置外壳的 section 槽声明
- `dsh-client-ui-settings-session-log` - 上传开关的读写经共享配置表单，并以 whileServed 判定命名空间是否被服务
- `dsh-client-ui-settings-shell` - 读 bash/pwsh 两个命名空间的共享配置表单，并以 whileServed 选择生效的那一个
- `dsh-client-ui-settings-subagent` - 两个命名空间的共享配置表单读写与 whileServed 判定都经该服务
- `dsh-client-ui-settings-web-search` - 搜索命名空间的共享配置表单读写与 whileServed 判定都经该服务
- `dsh-client-ui-shortcuts` - 拉入 settings.general.item 槽声明的类型合并（本包不注入 configForms）
- `dsh-client-ui-sidebar-documentpreview` - HTML 预览的交互开关读 settings 提供的 configForms
- `dsh-client-ui-theme` - 偏好经 settings 配置表单持久化，设置行也注册进其 item 槽
- `dsh-experimental-client-ui-cot-translation` - 设置页面的槽位与类型声明来自 settings UI 包
