# dsh-client-ui-permission-presets

- 包名: `@deepseek-ai/dsh-client-ui-permission-presets`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-permission-presets`

## 实现逻辑
浏览器半把权限预设做成挂在宿主 /permission 命令上的 popupSelect 装饰：选项读进程级目录、当前值读会话的 permissions 投影，选择统一提交 '/permission <preset>' 命令行，使两个界面走同一条写入路径（src/client/index.ts:176-191、src/client/index.ts:123-132）。同时向 conversation.input.permission 注册 composer 选择器、向 settings.general.item 注册默认预设设置行，Full access/Auto review 行带确认门（src/client/index.ts:159-174、src/client/index.ts:94-104）。目录失效时关闭过期的斜杠选择（src/client/index.ts:136-142）。

## Provides

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 拉取权限目录并读写设置文档
  - 证据: `src/client/index.ts:34 import type + src/client/catalog.ts:134 ctx.remote`
- `dsh-api-session-controller` [E1+E2] - 按会话读取 permissions 投影
  - 证据: `src/client/index.ts:19 import type + src/client/index.ts:115 ctx.sessions`
- `dsh-client-connection` [编译依赖] - 以真实连接世代为目录结算的栅栏
  - 证据: `src/client/catalog.ts:4 import type + src/client/index.ts:24 import type`
- `dsh-client-locale` [E1+E2] - 注册权限字典
  - 证据: `src/client/index.ts:26 import type + src/client/index.ts:117 ctx.locale.register(PERMISSION_ACCESS_NS)`
- `dsh-client-ui-commands` [E1+E2] - 装饰 /permission 的 popupSelect 界面
  - 证据: `src/client/index.ts:35 import type + src/client/index.ts:176 command.decorate({ name: 'permission' … })`
- `dsh-client-ui-conversation` [编译依赖] - 占用 conversation.input.permission 槽位声明
  - 证据: `src/client/PermissionSelect.tsx:15 import + src/client/index.ts:31 import type`
- `dsh-client-ui-input-trigger` [编译依赖] - 会话输入上下文类型
  - 证据: `src/client/index.ts:36 import type`
- `dsh-client-ui-primitives` [编译依赖] - 复用基础控件渲染选择器
  - 证据: `src/client/PermissionSelect.tsx:8 import`
- `dsh-client-ui-renderer` [编译依赖] - 渲染器槽位服务类型
  - 证据: `src/client/index.ts:29 import type`
- `dsh-client-ui-session` [编译依赖] - 会话标准 seat 类型
  - 证据: `src/client/index.ts:30 import type`
- `dsh-client-ui-settings` [编译依赖] - 注册 General 设置行
  - 证据: `src/client/index.ts:28 import type + src/client/settings-store.ts:13 import`
- `dsh-permission-presets` [编译依赖] - 复用权限目录与选择契约类型
  - 证据: `src/client/PermissionSelect.tsx:12 import + src/client/index.ts:21 import type`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
