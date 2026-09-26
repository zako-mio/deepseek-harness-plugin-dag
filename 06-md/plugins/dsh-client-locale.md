# dsh-client-locale

- 包名: `@deepseek-ai/dsh-client-locale`
- 分组: G05 客户端运行时
- 拓扑层: Layer 11
- 来源层: L2 web-app
- 源码路径: `packages/client/locale`

## 实现逻辑
Host 半仅把 locale 偏好接到 settings 配置投影 (src/index.ts:30-31)。浏览器半 `LocaleRuntime` 维护语言目录、按 fallback 链解析词典并按 revision 发布不可变快照，`translate` 先查 entry 命名空间再查 common 命名空间，缺失回退到 key 本身 (src/client/index.ts:165-513)。激活时从 `__DSH_LOCALE__` 桥读取原生语言、注册内置 zh/en 词典、provide `locale` 服务并经 `installLocale` 合成渲染层 `t` 座位，最后把 Language 行注册进 settings General 槽 (src/client/index.ts:563-622)。

## Provides
- ctx.locale (LocaleRuntime：字典注册 register、绑定 bind、快照 getSnapshot/subscribe、setLocale/addLanguage)
- locale/change 事件与 LocaleFace (供渲染层合成 t 座位)
- Language 设置行 (settings.general.item 槽贡献)

## Depends On (上游依赖)
- `dsh-client-ui-primitives` [编译依赖] - Language 行复用共享 UI 原语
  - 证据: `src/client/LanguageRow.tsx:9`
- `dsh-client-ui-renderer` [E1+E2] - 提供 ctx.slots 服务并安装 LocaleFace 供渲染机器合成 t 座位
  - 证据: `src/client/index.ts:18 + src/client/index.ts:554 inject 'slots' + src/client/index.ts:588 ctx.slots.installLocale`
- `dsh-client-ui-settings` [E1+E2] - 经 configForms 读取持久语言偏好并把 Language 行注册进设置区
  - 证据: `src/client/index.ts:15 + src/client/index.ts:554 inject 'configForms' + src/client/index.ts:577 ctx.configForms.get`
- `dsh-settings` [E1+E2] - 声明 locale 命名空间的 settings 配置面（auto:false）
  - 证据: `src/index.ts:2 + src/index.ts:31 ctx.inject(['settings']).settings.configure`

## Dependents (下游被依赖)
- `dsh-client-shortcuts` - 本地化键帽标签并在语言切换时刷新目录
- `dsh-client-ui-agent-preset` - 注册并绑定 settings.agentPreset 字典
- `dsh-client-ui-approval` - 注册 approval 字典与 resolveText
- `dsh-client-ui-chat` - 注册 chat 字典并绑定 t
- `dsh-client-ui-commands` - 注册命令字典
- `dsh-client-ui-conversation` - 注册 conversation 字典
- `dsh-client-ui-cordis` - 注册本插件的 zh/en 文案字典
- `dsh-client-ui-deliverables` - 注册 deliverables 字典
- `dsh-client-ui-directory-picker-browse` - 注册并绑定对话框字典
- `dsh-client-ui-goal` - 注册 goal 字典
- `dsh-client-ui-input-trigger` - 注册并观察菜单字典
- `dsh-client-ui-jobs` - 注册作业字典
- `dsh-client-ui-layout` - 注册并绑定 shortcuts.layout 文案命名空间
- `dsh-client-ui-message-feedback` - 注册 feedback 字典
- `dsh-client-ui-model-selection` - 注册 model 文案命名空间
- `dsh-client-ui-open-in-app` - 注册 open-in-app 文案
- `dsh-client-ui-permission-presets` - 注册 permission.access 与设置行文案
- `dsh-client-ui-plan` - 注册 plan 文案
- `dsh-client-ui-plugin-manager` - 注册 pluginManager 文案
- `dsh-client-ui-reference` - 注册 reference 文案
- `dsh-client-ui-schedule` - 注册 schedule.catalog 与 schedule.manager 文案
- `dsh-client-ui-settings-account` - 注册账户文案
- `dsh-client-ui-settings-agent-loop` - 注册并绑定本页文案字典
- `dsh-client-ui-settings-general` - 注册 settings 字典并投影本地化标签
- `dsh-client-ui-settings-models` - 注册并绑定 settings.models 字典
- `dsh-client-ui-settings-plugin-inventory` - 注册并绑定本 tab 文案
- `dsh-client-ui-settings-plugins` - 注册并绑定本段文案，并订阅 locale revision
- `dsh-client-ui-settings-shell` - 注册并绑定本页文案
- `dsh-client-ui-settings-subagent` - 注册并绑定本页文案
- `dsh-client-ui-settings-web-search` - 注册并绑定本页文案
- `dsh-client-ui-shortcuts` - 注册并绑定本包文案
- `dsh-client-ui-sidebar` - 注册并绑定 sidebar 文案，并订阅 locale 变化重算面板标签
- `dsh-client-ui-sidebar-browser` - 注册并绑定本 tab 文案
- `dsh-client-ui-sidebar-documentpreview` - 注册并绑定预览文案
- `dsh-client-ui-sidebar-files` - 注册并绑定本 tab 文案
- `dsh-client-ui-sidebar-right` - 注册并绑定本包文案
- `dsh-client-ui-sidebar-terminal` - 注册并绑定终端字典命名空间 sidebarTerminal
- `dsh-client-ui-skill` - 注册 skill 字典
- `dsh-client-ui-subagent` - 注册 subagent 字典
- `dsh-client-ui-theme` - 注册 settings.theme 字典
- `dsh-client-ui-tool` - 引入本地化命名空间类型
- `dsh-client-ui-trajectory` - 注册 trajectory 字典
- `dsh-client-ui-user-questions` - 注册 question 字典
- `dsh-client-ui-workflow-run` - 注册 workflowRun 字典
- `dsh-client-ui-workspace` - 注册 workspace 字典
- `dsh-experimental-client-ui-agent-team` - 注册中英文 Team 文案字典
- `dsh-experimental-client-ui-voice-input` - 注册语音相关中英文文案
- `dsh-session-log-export` - 注册 session-log-download 命名空间的中英文字典
