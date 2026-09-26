# dsh-client-ui-permission-presets

- 包名: `@deepseek-ai/dsh-client-ui-permission-presets`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-permission-presets`

## 实现逻辑
apply 在 Host 的 /permission 命令上挂 popupSelect 装饰：选项读进程级权限目录 PermissionCatalogDirectory，当前值读 Session 的 permissions 投影（src/client/index.ts:176-195）；选择统一经本地 submit 提交 `/permission <preset>` 命令行，从而与 argued 路径写同一条链路（src/client/index.ts:122-131）。同目录也被 composer 的 conversation.input.permission 座位复用（src/client/index.ts:167），并由 PermissionPresetSettingsController 在 General 设置行写入 defaultPreset（含 revision 校验与 mirror 折叠，src/client/settings-store.ts:88-131）。Full access / Auto review 行带显式风险确认（src/client/index.ts:80-105）。

## Provides
- commandUi 的 /permission popupSelect 装饰（当前会话权限档位选择、Full access/Auto 风险确认）
- conversation.input.permission 座位（composer 权限档位菜单，与 popup 共用进程目录）
- settings.general.item 条目 'permission'（新会话默认权限档位的设置行）

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 写 defaultPreset 与读 Session 投影
  - 证据: `src/client/index.ts:20 import + src/client/settings-store.ts:124 ctx.remote.settings`
- `dsh-api-session-controller` [编译依赖] - Session 外观与命令执行类型
  - 证据: `src/client/index.ts:19 import type { SessionFace }`
- `dsh-client-connection` [编译依赖] - 目录结算以连接世代为围栏
  - 证据: `src/client/index.ts:24 import type {} + src/client/catalog.ts:4 import type { ConnectionHandle }`
- `dsh-client-locale` [运行时依赖] - 注册 permission.access 与设置行文案
  - 证据: `src/client/index.ts:26 import + src/client/index.ts:117 ctx.locale.register`
- `dsh-client-ui-commands` [运行时依赖] - 装饰 /permission 命令为 popup 选择器
  - 证据: `src/client/index.ts:35 import type + src/client/index.ts:176 command.decorate`
- `dsh-client-ui-conversation` [运行时依赖] - 使用 ui-conversation 声明的权限座位
  - 证据: `src/client/index.ts:31 import type + src/client/index.ts:167 slots.inject('conversation.input.permission')`
- `dsh-client-ui-input-trigger` [编译依赖] - 命令/座位回调的会话上下文类型
  - 证据: `src/client/index.ts:36 import type { ClientSessionContext }`
- `dsh-client-ui-primitives` [编译依赖] - 复用 Menu/Select/图标控件
  - 证据: `src/client/PermissionSelect.tsx:8 import + src/client/PermissionRow.tsx:12`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 槽注册表
  - 证据: `src/client/index.ts:29 import type + src/client/index.ts:158 slots.inject`
- `dsh-client-ui-session` [编译依赖] - Session 标准来源类型面
  - 证据: `src/client/index.ts:30 import type {}`
- `dsh-client-ui-settings` [E1+E2] - 设置行使用 ui-settings 的 configForms/describe 面
  - 证据: `src/client/index.ts:28 import + src/client/index.ts:148 ctx.configForms.describe()`
- `dsh-permission-presets` [E1+E2] - 权限目录/选项与预设协议（Host client 面）
  - 证据: `src/client/catalog.ts:6 import + src/client/PermissionSelect.tsx:12 import`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
