# dsh-client-shortcuts

- 包名: `@deepseek-ai/dsh-client-shortcuts`
- 分组: G05 客户端运行时
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/client/shortcuts`

## 实现逻辑
Host 半只做配置投影：把校验过的快捷键配置以 __DSH_SHORTCUTS_CONFIG__ 注入产品页面（src/index.ts:15-19）。浏览器半 ShortcutsService 提供 ctx.shortcuts：探测运行环境与平台，构建 ShortcutRegistry（目录、固定目录、配置快照），安装 DOM 或桌面原生键盘适配器，并接浏览器/桌面存储做持久化（src/client/index.ts:27-75）；注册、编辑、绑定描述与冲突检测都经该服务（src/client/index.ts:77-158）。

## Provides
- ctx.shortcuts (窗口级应用命令注册表与生效键位目录，含 register/registerFixed/edit/describeBinding)

## Depends On (上游依赖)
- `dsh-client-locale` [E1+E2] - 语言切换时刷新键位标签
  - 证据: `src/client/index.ts:4 import type + src/client/index.ts:28 static inject ['locale'] + src/client/index.ts:74 ctx.locale.subscribe`
- `dsh-client-ui-primitives` [编译依赖] - 复用基础控件渲染键位与菜单
  - 证据: `src/client/dom.ts:2 import + src/client/native.ts:2 import`
- `dsh-host-webserver` [E1+E2] - 向页面注入快捷键配置全局量
  - 证据: `src/index.ts:5 import type + src/index.ts:16 webserver/index-inject`

## Dependents (下游被依赖)
- `dsh-client-ui-approval` - 注册 Enter/Esc 固定审批快捷键
- `dsh-client-ui-conversation` - 注册停止/提交快捷键
- `dsh-client-ui-layout` - 注册侧栏切换快捷键
- `dsh-client-ui-open-in-app` - 注册打开工作区快捷键
- `dsh-client-ui-settings-general` - 注册 settings.open 快捷键命令并把命令目录暴露给外壳显示
- `dsh-client-ui-shortcuts` - 命令注册、录制、编辑与目录/配置快照全部经 shortcuts 服务，其协议与客户端类型由该包持有
- `dsh-client-ui-sidebar` - 外壳向侧栏暴露快捷键目录快照以显示键位提示
- `dsh-client-ui-sidebar-browser` - 注册 browser.new 命令并绑定各平台默认按键
- `dsh-client-ui-sidebar-files` - 注册 workspace.files 命令及平台默认键
- `dsh-client-ui-sidebar-right` - 注册侧栏切换/关闭等命令并读取按键目录
- `dsh-client-ui-sidebar-terminal` - 注册 terminal.new 命令与各平台默认键
- `dsh-client-ui-workspace` - 工作区与会话动作的快捷键注册
- `dsh-experimental-inspector` - 检查器面板的开关快捷键注册在客户端快捷键目录上
