# dsh-client-ui-shortcuts

- 包名: `@deepseek-ai/dsh-client-ui-shortcuts`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 13
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-shortcuts`

## 实现逻辑
快捷键参考与本地偏好编辑插件。apply 注册 shortcuts 字典、创建唯一的 root 级 store 实例，并把 fixedCommands 里的菜单保留键逐条经 ctx.shortcuts.registerFixed 注册（每个命令一个 effect 便于回收）(src/client/index.ts:29-39, src/client/fixed.ts:10-16)。注册 shortcuts.open 命令（六个平台默认 primary+/，regions 覆盖 page/editable/terminal，在 settings/shortcuts 模态内可解析并负责关闭顶层弹窗），并在同一 fiber 内注册 shell.overlay 的参考面板，返回一个同时回收命令与槽的 disposer (src/client/index.ts:46-71)。同一 store 另把 ShortcutsRow 注册进 settings.general.item（order 16）(src/client/index.ts:42-45)。store 只持有 open/query/focusRequest 三个跨入口共享的交互状态 (src/client/store.ts:11-19)。

## Provides

## Depends On (上游依赖)
- `dsh-client-locale` [E1+E2] - 注册 shortcuts 字典并按命名空间绑定翻译（命令标签与面板文案）
  - 证据: `src/client/index.ts:5 import type {} from '@deepseek-ai/dsh-client-locale/client' + src/client/index.ts:29-30 ctx.locale.register('shortcuts', { zh, en }) / ctx.locale.bind('shortcuts')`
- `dsh-client-shortcuts` [E1+E2] - 命令注册、录制、编辑与目录/配置快照全部经 shortcuts 服务，其协议与客户端类型由该包持有
  - 证据: `src/client/Editor.tsx:5-6 import ShortcutBinding/ShortcutCatalogEntry + src/client/index.ts:34-38 ctx.shortcuts.edit/recording/describeBinding/registerFixed + src/client/index.ts:47 ctx.shortcuts.register({ id: 'shortcuts.open' ... })`
- `dsh-client-ui-layout` [编译依赖] - 参考面板注册进 layout 声明的 shell.overlay 槽（槽位声明依赖）
  - 证据: `src/client/index.ts:7 import type {} from '@deepseek-ai/dsh-client-ui-layout/client'`
- `dsh-client-ui-primitives` [编译依赖] - 参考面板、录制编辑器与快捷键键位显示复用共享原语
  - 证据: `src/client/Editor.tsx:4 import ShortcutKeys/focusWithoutRing/observeComposition + src/client/index.ts:4 import closeTopModal + package.json:53 devDependencies`
- `dsh-client-ui-renderer` [编译依赖] - 拉入 SlotRegistry 服务合并，使槽注册在此编译单元可用
  - 证据: `src/client/index.ts:6 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-settings` [编译依赖] - 拉入 settings.general.item 槽声明的类型合并（本包不注入 configForms）
  - 证据: `src/client/index.ts:8 import type {} from '@deepseek-ai/dsh-client-ui-settings/client'`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
