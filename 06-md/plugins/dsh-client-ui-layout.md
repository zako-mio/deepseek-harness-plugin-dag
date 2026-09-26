# dsh-client-ui-layout

- 包名: `@deepseek-ai/dsh-client-ui-layout`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 13
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-layout`

## 实现逻辑
客户端 shell 插件：apply 里用一次 ctx.slots.register 把 AppFrame 装进内建 'root' 槽，并同时声明 sidebar/main/rightbar/shell.overlay/shell.leading 五个子槽与布局 store（src/client/index.ts:171-182），同时把 store 实例绑到 LayoutController 暴露 ctx.layout（src/client/index.ts:167-170）。LayoutController 只写 store 声明的动作集，提供主面板选择、右栏轨道/全屏上报与侧栏开关（src/client/service.ts:57-105）；AppFrame 用 ResizeObserver + rAF 测量 frame 宽度并解算三栏几何（src/client/AppFrame.tsx:139-163）。另一条 effect 把 ThemePresenter 挂上，用纯 DOM 写入把 ctx.theme 快照投到 document（src/client/index.ts:210-218、src/client/theme-presenter.ts:49-75）。

## Provides
- ctx.layout (面板布局/导航服务 ILayout：selectPanel / beginNavigation / toggleSidebar / openRightbar / closeRightbar)
- 'root' 槽的 AppFrame 三栏框架（并声明 sidebar/main/rightbar/shell.overlay/shell.leading 子槽作为唯一渲染权威）
- hooks.usePanelInfo (根作用域主面板选择的可订阅源，随 provideRoot 发布)
- ctx.shortcuts 命令 sidebar.left.toggle（含桌面/Web 平台默认键位）
- 主题 DOM 呈现（ThemePresenter：html color-scheme、body 暗色属性、alias token 变量、theme-color meta）

## Depends On (上游依赖)
- `dsh-client-locale` [运行时依赖] - 注册并绑定 shortcuts.layout 文案命名空间
  - 证据: `src/client/index.ts:11 import type + src/client/index.ts:152 ctx.locale.register / index.ts:153 ctx.locale.bind`
- `dsh-client-shortcuts` [运行时依赖] - 注册侧栏切换快捷键命令
  - 证据: `src/client/index.ts:20 import type + src/client/index.ts:183 ctx.shortcuts.register`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 渲染组合注册表由 ui-renderer 提供，layout 借此注册/查询槽
  - 证据: `src/client/index.ts:12 import type + src/client/index.ts:168 ctx.slots.entries('main')`
- `dsh-client-ui-session` [编译依赖] - 引入 ui-session 的声明合并（Session 标准来源类型面）
  - 证据: `src/client/index.ts:13 import type {}`
- `dsh-client-ui-theme` [E1+E2] - 读取主题快照并订阅主题变化以投影到 DOM
  - 证据: `src/client/index.ts:14 import type + src/client/index.ts:212 ctx.theme.getTheme / index.ts:213 ctx.on('theme/change')`

## Dependents (下游被依赖)
- `dsh-client-ui-chat` - Chat 面板布局约束
- `dsh-client-ui-conversation` - 会话内容布局约束
- `dsh-client-ui-open-in-app` - 读主面板选择以判断当前无全局面板时才有打开目标
- `dsh-client-ui-plugin-manager` - 注册 main 面板并订阅主面板切换重置视图
- `dsh-client-ui-schedule` - 读主面板选择并复用布局类型
- `dsh-client-ui-settings-account` - 壳层布局类型面
- `dsh-client-ui-shortcuts` - 引入 layout 的 Context/SlotMap 合并
- `dsh-client-ui-sidebar` - 经布局服务切换/选择面板并引用面板 id 类型
- `dsh-client-ui-sidebar-right` - 经布局服务开合/全屏右栏面板
- `dsh-client-ui-sidebar-terminal` - 引入 shell.overlay 槽类型，用于清理失败提示（当前 index 中已注释）
- `dsh-client-ui-workspace` - 导航取消信号与面板选择
