# dsh-client-shortcuts

- 包名: `@deepseek-ai/dsh-client-shortcuts`
- 分组: G05 客户端运行时
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/client/shortcuts`

## 实现逻辑
Host 半把经过校验的键盘配置注入页面全局 `__DSH_SHORTCUTS_CONFIG__` (src/index.ts:15-19)。浏览器半 `ShortcutsService extends Service` 按环境（web/desktop）选择存储适配器与键盘适配器，建立 `ShortcutRegistry`，并暴露 register/registerFixed/observeFixedInput/describeBinding/edit 等命令面 (src/client/index.ts:27-75)。它订阅 locale 变化刷新按键标签，经固定输入监听器链带 consume 语义分发，Desktop 走原生键盘桥 (src/client/index.ts:74, 94-106, 62-63)。

## Provides
- ctx.shortcuts (窗口级应用命令注册表、生效键帽目录、编辑与描述绑定能力)
- 固定快捷键输入观察通道 (observeFixedInput，带 consume 链)
- windows/desktop/web 多运行时的存储与键盘适配

## Depends On (上游依赖)
- `dsh-client-locale` [E1+E2] - 本地化键帽标签并在语言切换时刷新目录
  - 证据: `src/client/index.ts:4 + src/client/index.ts:28 static inject 'locale' + src/client/index.ts:74 ctx.locale.subscribe`
- `dsh-client-ui-primitives` [编译依赖] - 复用 UI 原语渲染/呈现键帽
  - 证据: `src/client/dom.ts:2 + src/client/native.ts:2`
- `dsh-host-webserver` [运行时依赖] - 把键盘配置注入到服务的页面 index
  - 证据: `src/index.ts:5 + src/index.ts:16 ctx.on('webserver/index-inject')`

## Dependents (下游被依赖)
- `dsh-client-ui-approval` - 注册 Enter/Esc 固定审批快捷键
- `dsh-client-ui-conversation` - 注册输入与停转固定快捷键
- `dsh-client-ui-layout` - 注册侧栏切换快捷键命令
- `dsh-client-ui-open-in-app` - 注册 workspace.openLocal 快捷键命令
- `dsh-client-ui-settings-general` - 注册设置打开命令并展示快捷键目录
- `dsh-client-ui-shortcuts` - 注册命令/固定命令并读写快捷键目录与配置
- `dsh-client-ui-sidebar` - 把快捷键目录快照交给侧边栏展示
- `dsh-client-ui-sidebar-browser` - 注册新建浏览器标签命令并声明其可用性
- `dsh-client-ui-sidebar-files` - 注册打开文件面板命令
- `dsh-client-ui-sidebar-right` - 注册右栏快捷键并读取快捷键目录
- `dsh-client-ui-sidebar-terminal` - 注册 terminal.new 快捷键并读取快捷键目录
- `dsh-client-ui-workspace` - 注册/读取工作区快捷键命令
