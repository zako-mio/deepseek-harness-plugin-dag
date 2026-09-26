# dsh-client-ui-shortcuts

- 包名: `@deepseek-ai/dsh-client-ui-shortcuts`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 13
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-shortcuts`

## 实现逻辑
浏览器半注册 `shortcuts` 字典后，先用 `ctx.shortcuts.registerFixed` 批量注册固定命令（src/client/index.ts:37-39），再把快捷键参考行注册进 Settings 的 `settings.general.item`（id='shortcuts' order 20，src/client/index.ts:42-45），并把参考浮层注册进 `shell.overlay`（src/client/index.ts:46-71）。同时注册 `shortcuts.open` 命令（primary+/）在 settings 与 shortcuts 两种模态间切换开合（src/client/index.ts:47-65）。一个 store 句柄在 apply 内创建并同时交给设置行与浮层两处注册（src/client/index.ts:31-33）。

## Provides
- shortcuts locale 命名空间字典
- settings.general.item 条目 id='shortcuts' (order 20)：General 设置中的快捷键参考入口行
- shell.overlay 条目 id='shortcuts'：快捷键参考浮层
- shortcuts.open 命令（primary+/）以及经 shortcuts.registerFixed 注册的固定命令集

## Depends On (上游依赖)
- `dsh-client-locale` [E1+E2] - 注册并绑定本包文案
  - 证据: `src/client/index.ts:5 type-only import + src/client/index.ts:29 ctx.locale.register, src/client/index.ts:30 ctx.locale.bind('shortcuts')`
- `dsh-client-shortcuts` [E1+E2] - 注册命令/固定命令并读写快捷键目录与配置
  - 证据: `src/client/Editor.tsx:6 import (client) + src/client/index.ts:34 ctx.shortcuts.edit, src/client/index.ts:38 ctx.shortcuts.registerFixed`
- `dsh-client-ui-layout` [编译依赖] - 引入 layout 的 Context/SlotMap 合并
  - 证据: `src/client/index.ts:7 type-only import`
- `dsh-client-ui-primitives` [编译依赖] - 复用编辑器/菜单原语并关闭顶层模态
  - 证据: `src/client/Editor.tsx:4 import + src/client/index.ts:4 import closeTopModal`
- `dsh-client-ui-renderer` [编译依赖] - 引入 ctx.slots 合并
  - 证据: `src/client/index.ts:6 type-only import`
- `dsh-client-ui-settings` [E1+E2] - 引入设置域槽声明，General 段的 item 槽由其外壳渲染
  - 证据: `src/client/index.ts:8 type-only import + src/client/index.ts:42 向 settings.general.item 注册`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
