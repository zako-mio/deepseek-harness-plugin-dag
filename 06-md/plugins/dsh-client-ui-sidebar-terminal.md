# dsh-client-ui-sidebar-terminal

- 包名: `@deepseek-ai/dsh-client-ui-sidebar-terminal`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-sidebar-terminal`

## 实现逻辑
把交互式终端注册为右侧边栏 terminal 类型：client/index.ts:71-74 向 ctx.sidebarRightTabs 注册定义（kind 'terminal'、priority builtin、guide 入口），:94-98 将 LazyTerminalBody 注入键控 sidebar.right.pane.tab，:99-101 注入 TerminalTitle，:86-93 把 TerminalGuide 注入 sidebar.right.tab.guide.entry。终端生命周期绑定 ctx.webTerminals：:33-38 用 retainTabs 随 openTabs 快照保留窗口（卸载时清空），:75-77 注册关闭处理器调用 webTerminals.close，view()（:45-50）从标签 navigation 参数解析 terminalId/shellPath 并取 state 作为键控 hook。主题经 theme/change 事件订阅（:82-85）传给终端渲染器，快捷键 terminal.new 注册于 :54-69。

## Provides
- sidebarRightTabs 标签类型 terminal（交互式终端标签）
- 槽位贡献 sidebar.right.pane.tab / sidebar.right.pane.tab.title / sidebar.right.tab.guide.entry 的 terminal 键视图
- 快捷键命令 terminal.new

## Depends On (上游依赖)
- `dsh-api-terminal-controller` [E1+E2] - 终端视图、启动 shell、关闭与保留窗口全部经 webTerminals 服务
  - 证据: `src/client/index.ts:4 import type { WebTerminalId } from '@deepseek-ai/dsh-api-terminal-controller/types'; src/client/index.ts:34 ctx.webTerminals.retainTabs`
- `dsh-client-locale` [E1+E2] - 终端类型标题、guide 与快捷键文案本地化
  - 证据: `src/client/index.ts:10 import type {} from '@deepseek-ai/dsh-client-locale/client'; src/client/index.ts:70 ctx.locale.register(namespace, { zh, en })`
- `dsh-client-shortcuts` [E1+E2] - 注册 terminal.new 命令与各平台默认键
  - 证据: `src/client/index.ts:2 import type { ShortcutCommandId }; src/client/index.ts:54 ctx.shortcuts.register`
- `dsh-client-ui-conversation` [编译依赖] - （已停用分支）恢复入口原注册进会话头部动作槽
  - 证据: `src/client/TerminalRecovery.tsx:4 import type {} from '@deepseek-ai/dsh-client-ui-conversation/client'`
- `dsh-client-ui-layout` [编译依赖] - （已停用分支）清理浮层原挂在 shell.overlay，需 layout 的槽合并
  - 证据: `src/client/TerminalCleanup.tsx:6 import type {} from '@deepseek-ai/dsh-client-ui-layout/client'`
- `dsh-client-ui-primitives` [编译依赖] - guide 入口图标与终端控件复用共享原语
  - 证据: `src/client/index.ts:13 import { PluginArtworkTerminal } from '@deepseek-ai/dsh-client-ui-primitives'`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 服务由 renderer 提供
  - 证据: `src/client/index.ts:9 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-session` [编译依赖] - 拉入 uiSession 合并以按会话渲染
  - 证据: `src/client/index.ts:11 import type {} from '@deepseek-ai/dsh-client-ui-session/client'`
- `dsh-client-ui-sidebar-right` [E1+E2] - 标签类型与键控槽、关闭处理器均挂在 sidebar-right 提供的服务上
  - 证据: `src/client/index.ts:5 import type {} from '@deepseek-ai/dsh-client-ui-sidebar-right/client'; src/client/index.ts:71 ctx.sidebarRightTabs.register`
- `dsh-client-ui-theme` [E1+E2] - 终端配色与字号跟随活动主题，主题切换时重绘
  - 证据: `src/client/index.ts:12 import type {} from '@deepseek-ai/dsh-client-ui-theme/client'; src/client/index.ts:82-85 ctx.theme.getTheme + ctx.on('theme/change')`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/index.ts:6 import type { SessionId } from '@deepseek-ai/dsh-session/types'`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
