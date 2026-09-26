# dsh-client-ui-sidebar

- 包名: `@deepseek-ai/dsh-client-ui-sidebar`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-sidebar`

## 实现逻辑
浏览器半注册 `sidebar` 槽并声明 brand.mark/brand.name/toggle.badge/panellist/workspaces/settings/footer.action 子槽（src/client/index.ts:72-85）。它把 `sidebar.panellist` 台账投影为有序面板元数据快照，并在台账或 locale 变化时重算（src/client/index.ts:47-62）。注入面暴露 startSession（经 uiWorkspace 共享动作，src/client/index.ts:45、67）、toggleSidebar/selectPanel（经 ctx.layout，src/client/index.ts:68-69）与 shortcuts 目录（src/client/index.ts:70）；同一注入面还被 `shell.leading` 头部控件复用（src/client/index.ts:90-94）。node half 为空 apply（src/index.ts:4）。

## Provides
- sidebar locale 命名空间字典
- sidebar 槽位占用者（侧边栏外壳），声明 sidebar.brand.mark / sidebar.brand.name / sidebar.toggle.badge / sidebar.panellist / sidebar.workspaces / sidebar.settings / sidebar.footer.action 子槽
- shell.leading 槽的头部前置控件（折叠侧栏 / 新建会话，用于 macOS 隐藏侧栏场景）
- sidebar.panellist 台账投影为有序面板元数据 observable 源

## Depends On (上游依赖)
- `dsh-api-workspace-controller` [编译依赖] - startSession 的 workspace 参数类型
  - 证据: `src/client/contract/slots.ts:12 import type WorkspaceId`
- `dsh-client-locale` [E1+E2] - 注册并绑定 sidebar 文案，并订阅 locale 变化重算面板标签
  - 证据: `src/client/index.ts:7 type-only import + src/client/index.ts:46 ctx.locale.register`
- `dsh-client-shortcuts` [E1+E2] - 把快捷键目录快照交给侧边栏展示
  - 证据: `src/client/contract/slots.ts:13 import type ShortcutCatalogEntry + src/client/index.ts:70 ctx.shortcuts.catalog`
- `dsh-client-ui-layout` [E1+E2] - 经布局服务切换/选择面板并引用面板 id 类型
  - 证据: `src/client/index.ts:5 import type MainPanelId + src/client/index.ts:68 ctx.layout.toggleSidebar`
- `dsh-client-ui-renderer` [编译依赖] - 引入 ctx.slots 合并
  - 证据: `src/client/index.ts:9 type-only import`
- `dsh-client-ui-session` [编译依赖] - 引入会话标准 props 合并
  - 证据: `src/client/index.ts:11 type-only import`

## Dependents (下游被依赖)
- `dsh-client-ui-brand-official` - 占据侧边栏品牌槽位
- `dsh-client-ui-cordis` - 把 cordis 面板挂载到侧边栏页脚动作位
- `dsh-client-ui-plugin-manager` - 使用 ui-sidebar 声明的面板列表槽
- `dsh-client-ui-schedule` - 向侧栏面板列表注册任务入口
- `dsh-client-ui-settings-general` - 引用 sidebar 的 SlotMap 与 owner props 类型以渲染该槽占位
- `dsh-client-ui-workspace` - 引入 sidebar.workspaces 等槽的声明类型
