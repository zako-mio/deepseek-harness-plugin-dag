# dsh-client-ui-sidebar-terminal

- 包名: `@deepseek-ai/dsh-client-ui-sidebar-terminal`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-sidebar-terminal`

## 实现逻辑
浏览器端交互式终端插件：apply 在 ctx.sidebarRightTabs 注册 kind='terminal' 的多开标签类型（src/client/index.ts:71-74），并用 ctx.effect 订阅 sidebarRight.openTabs 快照做 retain/释放，保证只有打开的终端标签持有后台进程（src/client/index.ts:33-38）。它把 TerminalGuide、LazyTerminalBody、TerminalTitle 分别注入 sidebar.right.tab.guide.entry、sidebar.right.pane.tab、sidebar.right.pane.tab.title 三个座位（src/client/index.ts:86-101），并注册 'terminal.new' 快捷键与终端关闭处理器（src/client/index.ts:54-69,75-77）。

## Provides
- sidebarRightTabs 注册 'terminal' 标签类型（标题/引导图标/多开）
- slot sidebar.right.tab.guide.entry 的终端新建引导 (TerminalGuide)
- slot sidebar.right.pane.tab 的终端主体 (LazyTerminalBody，跟随 theme 快照)
- slot sidebar.right.pane.tab.title 的终端标题 (TerminalTitle)
- 快捷键命令 terminal.new（Ctrl+`）与 'terminal' 关闭处理器

## Depends On (上游依赖)
- `dsh-api-terminal-controller` [E1+E2] - 通过 ctx.webTerminals 服务管理 Web 终端视图、shell 启动与关闭
  - 证据: `src/client/index.ts:7 import type + src/client/index.ts:34 ctx.webTerminals.retainTabs`
- `dsh-client-locale` [E1+E2] - 注册并绑定终端字典命名空间 sidebarTerminal
  - 证据: `src/client/index.ts:10 + src/client/index.ts:53 ctx.locale.bind`
- `dsh-client-shortcuts` [E1+E2] - 注册 terminal.new 快捷键并读取快捷键目录
  - 证据: `src/client/TerminalGuide.tsx:3 + src/client/index.ts:54 ctx.shortcuts.register`
- `dsh-client-ui-conversation` [编译依赖] - 引入会话头部动作槽类型，用于终端恢复入口（当前 index 中已注释）
  - 证据: `src/client/TerminalRecovery.tsx:4 import type`
- `dsh-client-ui-layout` [编译依赖] - 引入 shell.overlay 槽类型，用于清理失败提示（当前 index 中已注释）
  - 证据: `src/client/TerminalCleanup.tsx:6 import type`
- `dsh-client-ui-primitives` [编译依赖] - 复用终端图标原语
  - 证据: `src/client/index.ts:13 PluginArtworkTerminal`
- `dsh-client-ui-renderer` [编译依赖] - 拉入 SlotRegistry 服务合并类型
  - 证据: `src/client/index.ts:9 import type`
- `dsh-client-ui-session` [编译依赖] - 拉入会话 UI 服务的类型合并
  - 证据: `src/client/index.ts:11 import type`
- `dsh-client-ui-sidebar-right` [E1+E2] - 注册终端标签类型、读取 occurrence 参数并注册关闭处理器
  - 证据: `src/client/index.ts:5 import + src/client/index.ts:40 ctx.sidebarRight.tabDomain`
- `dsh-client-ui-theme` [E1+E2] - 终端配色跟随全局主题快照，订阅 theme/change
  - 证据: `src/client/index.ts:12 import type + src/client/index.ts:83-84 ctx.theme.getTheme`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/index.ts:6 SessionId`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
