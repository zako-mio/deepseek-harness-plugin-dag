# dsh-client-ui-sidebar

- 包名: `@deepseek-ai/dsh-client-ui-sidebar`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-sidebar`

## 实现逻辑
侧栏外壳插件。apply 注册 sidebar 字典并占据布局侧栏槽，children 里一次性声明 brand.mark/brand.name/toggle.badge/panellist/workspaces/settings/footer.action 七个洞（声明即授权）(src/client/index.ts:76-89)。面板列表从 slots.entriesOfSlot('sidebar.panellist') 投影为按 order 排序的快照源，仅在 id/order/label 真正变化时 set，并同时订阅该槽与 locale 两处变更（标签可能是随语言变化的 thunk）(src/client/index.ts:48-63)。注入面把 New Session 转发给 uiWorkspace.startSession、面板切换转发给 ctx.layout.selectPanel，并对 plugins/schedules 两个面板记产品分析事件（可选服务经 ctx.get 读取）(src/client/index.ts:65-75)。macOS 桌面折叠时侧栏整体隐藏，另把 HeaderLeadingControls 注册进 shell.leading 复用同一注入面 (src/client/index.ts:90-98)。

## Provides
- 声明侧栏外壳槽 'sidebar' 的子洞：sidebar.brand.mark / sidebar.brand.name / sidebar.toggle.badge / sidebar.panellist（list）/ sidebar.workspaces / sidebar.settings / sidebar.footer.action（list），各功能据此插入品牌位、面板图标与会话浏览区

## Depends On (上游依赖)
- `dsh-api-workspace-controller` [编译依赖] - New Session 动作以 WorkspaceId 为可选参数，其不透明 id 类型由 workspace-controller 持有
  - 证据: `src/client/contract/slots.ts:12 import WorkspaceId + package.json:51 devDependencies`
- `dsh-client-locale` [E1+E2] - 注册 sidebar 字典，并在语言切换时重算面板标签快照
  - 证据: `src/client/index.ts:8 import type {} from '@deepseek-ai/dsh-client-locale/client' + src/client/index.ts:47 ctx.locale.register(NS, { zh, en }) + src/client/index.ts:63 ctx.locale.subscribe(syncPanels)`
- `dsh-client-product-analytics` [E1+E2] - 面板切换时上报产品分析事件（可选服务用 ctx.get 读取，不写进 inject）
  - 证据: `src/client/index.ts:2 import type {} from '@deepseek-ai/dsh-client-product-analytics/client' + src/client/index.ts:71 ctx.get('productAnalytics')?.track('sidebar_menu_click', ...)`
- `dsh-client-shortcuts` [E1+E2] - 外壳向侧栏暴露快捷键目录快照以显示键位提示
  - 证据: `src/client/contract/slots.ts:13 import ShortcutCatalogEntry + src/client/index.ts:74 hooks: { panels, shortcuts: ctx.shortcuts.catalog }`
- `dsh-client-ui-layout` [E1+E2] - 面板 id 类型来自 layout，侧栏折叠与主面板切换由 layout 服务执行
  - 证据: `src/client/contract/slots.ts:14 import MainPanelId + src/client/index.ts:6 import type {} from '@deepseek-ai/dsh-client-ui-layout/client' + src/client/index.ts:69-72 ctx.layout.toggleSidebar() / ctx.layout.selectPanel(id)`
- `dsh-client-ui-renderer` [编译依赖] - 拉入 SlotRegistry 服务合并，使槽注册与 entriesOfSlot/subscribe 在此编译单元可用
  - 证据: `src/client/index.ts:10 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-session` [编译依赖] - 拉入会话根标准 props 合并，供侧栏内会话相关 seat 的类型契约
  - 证据: `src/client/index.ts:12 import type {} from '@deepseek-ai/dsh-client-ui-session/client'`

## Dependents (下游被依赖)
- `dsh-client-ui-brand-official` - 占据侧边栏品牌槽位
- `dsh-client-ui-cordis` - 把 Cordis 面板挂到侧边栏底部动作位
- `dsh-client-ui-plugin-manager` - 占用 sidebar.panellist 槽位声明
- `dsh-client-ui-schedule` - 面板图标注册进 ui-sidebar 声明的 sidebar.panellist 列表槽
- `dsh-client-ui-settings-general` - 外壳占据 ui-sidebar 声明的 sidebar.settings 洞（另有 sidebar.toggle.badge）
- `dsh-client-ui-workspace` - sidebar.workspaces 槽由 ui-sidebar 声明
