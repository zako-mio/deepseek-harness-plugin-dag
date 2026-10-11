# dsh-client-ui-layout

- 包名: `@deepseek-ai/dsh-client-ui-layout`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 13
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-layout`

## 实现逻辑
浏览器半一次 register() 把 AppFrame 放进运行时内置的 'root' 槽，同时声明 sidebar/main/rightbar/shell.bottom/shell.overlay/shell.leading 六个子槽、给布局 store 落座并提供面板信息源（src/client/index.ts:178-190）。它通过 ctx.reflect.provide('layout', …) 暴露 ctx.layout（主面板选择与列几何），注册侧栏切换快捷键，并用第二个 effect 把 ctx.theme 快照投影到 document.body（src/client/index.ts:174-226）。

## Provides
- ctx.layout (主面板选择、列几何与 panelInfo 可观察源) (src/client/index.ts:177)
- root 槽及其六个子槽声明 (src/client/index.ts:178-190)

## Depends On (上游依赖)
- `dsh-client-locale` [E1+E2] - 注册快捷键标签字典
  - 证据: `src/client/index.ts:11 import type + src/client/index.ts:159 ctx.locale.register('shortcuts.layout')`
- `dsh-client-shortcuts` [E1+E2] - 注册侧栏切换快捷键
  - 证据: `src/client/index.ts:20 import type + src/client/index.ts:191 ctx.shortcuts.register`
- `dsh-client-ui-renderer` [编译依赖] - 渲染器槽位服务类型
  - 证据: `src/client/index.ts:12 import type`
- `dsh-client-ui-session` [编译依赖] - 会话标准 seat 类型
  - 证据: `src/client/index.ts:13 import type`
- `dsh-client-ui-theme` [E1+E2] - 把主题快照投影到 document.body
  - 证据: `src/client/index.ts:14 import type + src/client/index.ts:220 ctx.theme.getTheme()`

## Dependents (下游被依赖)
- `dsh-client-ui-chat` - 布局槽位类型
- `dsh-client-ui-conversation` - 布局槽位类型
- `dsh-client-ui-open-in-app` - 按当前主面板判断是否可打开
- `dsh-client-ui-plugin-manager` - 注册 main keyed 面板并读取面板选择
- `dsh-client-ui-schedule` - 删除 Toast 注册进 layout 声明的 shell.overlay，任务管理面板 id 取自 layout 的 MainPanelId
- `dsh-client-ui-settings-account` - 平台页宿主与桌面引导条目注册进 layout 声明的 shell.overlay
- `dsh-client-ui-settings-session-log` - Toast 注册进 layout 声明的 shell.overlay 槽（槽位声明依赖）
- `dsh-client-ui-shortcuts` - 参考面板注册进 layout 声明的 shell.overlay 槽（槽位声明依赖）
- `dsh-client-ui-sidebar` - 面板 id 类型来自 layout，侧栏折叠与主面板切换由 layout 服务执行
- `dsh-client-ui-sidebar-right` - 面板显隐与轨道宽度由 frame 的 layout 服务决定，本插件只上报事实
- `dsh-client-ui-sidebar-terminal` - （已停用分支）清理浮层原挂在 shell.overlay，需 layout 的槽合并
- `dsh-client-ui-workspace` - 导航切页需驱动 frame 的 layout 面板动作
- `dsh-experimental-inspector` - 面板的布局约束与类型声明来自布局包
