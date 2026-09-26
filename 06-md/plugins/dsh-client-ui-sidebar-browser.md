# dsh-client-ui-sidebar-browser

- 包名: `@deepseek-ai/dsh-client-ui-sidebar-browser`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-sidebar-browser`

## 实现逻辑
浏览器半把 `browser` tab 类型注册进 `ctx.sidebarRightTabs`（src/client/index.ts:74），并按是否存在协议版本 1 的桌面 carrier 选择 iframe 或 Electron 页面实现（src/client/index.ts:69-72、97-101）。面板主体经键控槽 `sidebar.right.pane.tab` 注册 BrowserBody，按 sessionId 复用控制器并支持行动作重绑（src/client/index.ts:75-95），标题经 `sidebar.right.pane.tab.title` 注册 BrowserTitle（src/client/index.ts:102-104）；另在 shortcuts 服务可见时注册 `browser.new` 命令（src/client/index.ts:46-66）。node half 为空 apply。

## Provides
- sidebarBrowser locale 命名空间字典
- sidebarRightTabs 注册 'browser' tab 类型定义（并扩展 SidebarRightTabParamsMap.browser 参数，src/client/index.ts:32-37）
- sidebar.right.pane.tab 键控条目 key=BROWSER_ID：浏览器面板 body（iframe / Electron webview 两实现）
- sidebar.right.pane.tab.title 键控条目 key=BROWSER_ID：浏览器标签标题
- browser.new 快捷键命令（primary+T）

## Depends On (上游依赖)
- `dsh-api-workspace-controller` [E1+E2] - 经 workspace 服务把浏览器页面映射到工作区
  - 证据: `src/client/electron/workspace.ts:2 import (client) + src/client/index.ts:98 ctx.inject(['workspaces'])`
- `dsh-client-locale` [E1+E2] - 注册并绑定本 tab 文案
  - 证据: `src/client/definition.tsx:3 import + src/client/index.ts:45 ctx.locale.bind(namespace)`
- `dsh-client-shortcuts` [E1+E2] - 注册新建浏览器标签命令并声明其可用性
  - 证据: `src/client/definition.tsx:2 import (client) + src/client/index.ts:47 ctx.shortcuts.register`
- `dsh-client-ui-dockkit` [编译依赖] - 复用 dock 标签/布局原语
  - 证据: `src/client/browser/BrowserController.ts:3 import + src/client/browser/store.ts:3 import`
- `dsh-client-ui-primitives` [编译依赖] - 复用共享 UI 原语
  - 证据: `src/client/definition.tsx:4 import + src/client/view/BrowserTitle.tsx:3 import`
- `dsh-client-ui-renderer` [编译依赖] - 引入 ctx.slots 合并
  - 证据: `src/client/index.ts:5 type-only import`
- `dsh-client-ui-session` [编译依赖] - 引入会话标准 props 合并
  - 证据: `src/client/index.ts:6 type-only import`
- `dsh-client-ui-sidebar-right` [E1+E2] - 把 tab 类型与 body/title 注册进右侧边栏的两级公共路径
  - 证据: `src/client/definition.tsx:5 import (client) + src/client/index.ts:74 ctx.sidebarRightTabs.register`

## Dependents (下游被依赖)
- `dsh-client-ui-chat` - 浏览器 tab 类型声明
