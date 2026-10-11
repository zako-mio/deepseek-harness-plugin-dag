# dsh-client-ui-sidebar-browser

- 包名: `@deepseek-ai/dsh-client-ui-sidebar-browser`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-sidebar-browser`

## 实现逻辑
以「标签类型声明 + 键控槽注册」两段式把 HTTP(S) 浏览器接入右侧边栏：definition.tsx:15-26 声明 kind='browser' 的类型、优先级 builtin 与 guide 入口，client/index.ts:43-104 的 apply 注册 browser.new 快捷键（:46-66）、经 ctx.sidebarRightTabs.register 注册类型（:74），并把 BrowserBody 注入键控 sidebar.right.pane.tab（:82-95）、BrowserTitle 注入 title 槽（:102-104）。运行期按 globalThis.dshDesktop 是否存在分流：Web 走 createIframePage/IframeImpl 的 iframe 载体（:97），Desktop 走 Electron webview 并经 ctx.inject(['workspaces']) 用 browserWorkspace 解析工作区（:98-101）。控制器 BrowserController 统一地址校验、导航状态机与恢复，标签状态由 createBrowserStore 承载（:67、:76-94）。

## Provides
- sidebarRightTabs 标签类型 browser（HTTP(S) 页签；Web=iframe，Desktop=webview）
- 槽位贡献 sidebar.right.pane.tab / sidebar.right.pane.tab.title 的 browser 键视图
- 快捷键命令 browser.new

## Depends On (上游依赖)
- `dsh-api-workspace-controller` [E1+E2] - Desktop 侧按工作区解析存储分区与 canonical CWD
  - 证据: `src/client/electron/workspace.ts:2 import type { WorkspaceSource } from '@deepseek-ai/dsh-api-workspace-controller/client'; src/client/index.ts:98-100 ctx.inject(['workspaces'])`
- `dsh-client-locale` [E1+E2] - 标签标题、guide 文案与快捷键拒绝原因均由 locale 字典提供
  - 证据: `src/client/index.ts:4 import type {} from '@deepseek-ai/dsh-client-locale/client'; src/client/index.ts:45 ctx.locale.bind('sidebarBrowser')`
- `dsh-client-shortcuts` [E1+E2] - 注册 browser.new 命令并绑定各平台默认按键
  - 证据: `src/client/index.ts:2 import type { ShortcutCommandId }; src/client/index.ts:46-47 ctx.inject(['shortcuts']) + ctx.shortcuts.register`
- `dsh-client-ui-dockkit` [编译依赖] - 标签身份与停靠面板 id 使用 dockkit 的 TabId 类型
  - 证据: `src/client/browser/BrowserController.ts:3 import type { TabId } from '@deepseek-ai/dsh-client-ui-dockkit'`
- `dsh-client-ui-primitives` [编译依赖] - guide 入口图标与工具条控件复用共享原语
  - 证据: `src/client/definition.tsx:4 import { GuideArtworkBrowser } from '@deepseek-ai/dsh-client-ui-primitives'`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 服务与槽渲染机制来自 renderer
  - 证据: `src/client/index.ts:5 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'; src/client/index.ts:102-104 ctx.slots 服务由 renderer 提供`
- `dsh-client-ui-session` [编译依赖] - 拉入 uiSession 的 Context 合并，标签按 sessionId 作用域渲染
  - 证据: `src/client/index.ts:6 import type {} from '@deepseek-ai/dsh-client-ui-session/client'`
- `dsh-client-ui-sidebar-right` [E1+E2] - 标签类型与键控槽由 sidebar-right 声明并提供 ctx.sidebarRight/ctx.sidebarRightTabs，browser 只能在其中注册
  - 证据: `src/client/index.ts:7 import type {} from '@deepseek-ai/dsh-client-ui-sidebar-right/client'; src/client/index.ts:60-62 ctx.sidebarRight.commandTarget/openTabFromTarget`

## Dependents (下游被依赖)
- `dsh-client-ui-chat` - 浏览器标签类型
