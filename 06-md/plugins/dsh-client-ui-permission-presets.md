# dsh-client-ui-permission-presets

- 包名: `@deepseek-ai/dsh-client-ui-permission-presets`
- 分组: G28 设置输入UI
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-permission-presets`

## 实现逻辑
权限 preset 双面：注册 /permission popupSelect 装饰（command.decorate，index.ts:148-169），选项读会话 permissions 投影 faceOf('permissions')（:51-53），pick 提交 '/permission <preset>' 命令；Full access 行带确认门。另注册 settings.general.item 的 PermissionRow 写新会话默认 preset（:140-146），经 PermissionPresetSettingsController 读写 host Settings API（settings-store.ts:19 PERMISSION_SETTINGS_NS='permission'）。

## Provides
- /permission popupSelect 装饰
- settings.general.item 'permission' 行 (PermissionRow)
- permission.access / settings.permission 字典

## Depends On (上游依赖)
- `dsh-client-ui-commands` [运行时依赖] - popupSelect 装饰注册
  - 证据: `packages/client/ui-permission-presets/src/client/index.ts:46,84,148 (inject commandUi + command.decorate)`
- `dsh-client-ui-settings` [编译依赖] - General 行槽声明
  - 证据: `packages/client/ui-permission-presets/src/client/index.ts:20 (type-only import), :140 (slots.inject('settings.general.item'))`
- `dsh-permission-presets` [运行时依赖] - permissions 会话投影提供选项/当前值
  - 证据: `packages/client/ui-permission-presets/src/client/index.ts:27,52 (PermissionSelect 类型 + session.projections.faceOf('permissions'))`
- `dsh-session` [运行时依赖] - 会话绑定与命令执行
  - 证据: `packages/client/ui-permission-presets/src/client/index.ts:110-111 (sessions.binding + session.command)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
