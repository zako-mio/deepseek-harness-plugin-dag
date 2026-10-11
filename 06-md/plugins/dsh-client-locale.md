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
- `dsh-client-shortcuts` - 语言切换时刷新键位标签
- `dsh-client-ui-agent-preset` - 注册 settings.agentPreset 字典
- `dsh-client-ui-approval` - 注册 approval 字典与 resolveText
- `dsh-client-ui-chat` - 注册 Chat 字典
- `dsh-client-ui-commands` - 注册 command 字典
- `dsh-client-ui-conversation` - 注册 conversation 字典
- `dsh-client-ui-cordis` - 注册 ui-cordis 命名空间的中英文字典，供面板与卡片取文案
- `dsh-client-ui-deliverables` - 注册 deliverables 字典
- `dsh-client-ui-directory-picker-browse` - 注册并绑定对话框字典
- `dsh-client-ui-goal` - 注册 goal 字典
- `dsh-client-ui-input-trigger` - 注册并观察菜单字典
- `dsh-client-ui-jobs` - 注册 job 字典
- `dsh-client-ui-layout` - 注册快捷键标签字典
- `dsh-client-ui-message-feedback` - 注册 feedback 字典
- `dsh-client-ui-model-selection` - 注册 model 字典
- `dsh-client-ui-open-in-app` - 注册 open-in-app 字典
- `dsh-client-ui-permission-presets` - 注册权限字典
- `dsh-client-ui-plan` - 注册 plan 字典
- `dsh-client-ui-plugin-manager` - 注册 pluginManager 字典
- `dsh-client-ui-reference` - 注册 reference 文案
- `dsh-client-ui-schedule` - 两套字典（schedule.catalog / schedule.manager）由 locale 服务注册并按命名空间绑定翻译
- `dsh-client-ui-settings-account` - 注册账户字典并按 settings.account 命名空间绑定翻译
- `dsh-client-ui-settings-agent-loop` - 页面文案必须经 locale 服务注册并按命名空间绑定翻译
- `dsh-client-ui-settings-general` - 注册 settings 字典（外壳 chrome + General 文案）并跟随 locale revision 刷新导航标签
- `dsh-client-ui-settings-models` - 注册 settings.models 字典并绑定导航标签与页面文案的翻译
- `dsh-client-ui-settings-plugin-inventory` - 注册清单页字典并绑定翻译；另借 locale 逐次解析预设名
- `dsh-client-ui-settings-plugins` - 注册并绑定本段文案，并订阅 locale revision
- `dsh-client-ui-settings-session-log` - 注册 settings.sessionLog 字典并作为两个槽的 locale 命名空间
- `dsh-client-ui-settings-shell` - 注册 settings.shell 字典并按命名空间绑定翻译
- `dsh-client-ui-settings-subagent` - 注册 settings.subagent 字典并按命名空间绑定翻译
- `dsh-client-ui-settings-web-search` - 注册 settings.webSearch 字典并按命名空间绑定翻译
- `dsh-client-ui-shortcuts` - 注册 shortcuts 字典并按命名空间绑定翻译（命令标签与面板文案）
- `dsh-client-ui-sidebar` - 注册 sidebar 字典，并在语言切换时重算面板标签快照
- `dsh-client-ui-sidebar-browser` - 标签标题、guide 文案与快捷键拒绝原因均由 locale 字典提供
- `dsh-client-ui-sidebar-documentpreview` - 各格式渲染器的标题与失败文案由 locale 拥有
- `dsh-client-ui-sidebar-files` - 类型标题与快捷键拒绝文案来自字典
- `dsh-client-ui-sidebar-right` - 标签标签、guide 与菜单文案本地化
- `dsh-client-ui-sidebar-terminal` - 终端类型标题、guide 与快捷键文案本地化
- `dsh-client-ui-skill` - 菜单与工具行文案本地化
- `dsh-client-ui-subagent` - 目录、血统与只读提示文案本地化
- `dsh-client-ui-theme` - 外观与字体设置行文案本地化
- `dsh-client-ui-tool` - 工具行文案走 locale 字典（复用 conversation 命名空间）
- `dsh-client-ui-trajectory` - 视图页标签与表头文案本地化
- `dsh-client-ui-user-questions` - 问答界面文案本地化
- `dsh-client-ui-workflow-run` - 运行状态与面板文案本地化
- `dsh-client-ui-workspace` - 浏览区、菜单与浮层文案本地化
- `dsh-experimental-client-ui-agent-team` - 注册中英文 Team 文案字典
- `dsh-experimental-client-ui-claude-code-mods` - band 文案走客户端字典而非硬编码
- `dsh-experimental-client-ui-cot-translation` - 译文区与表单文案走客户端字典
- `dsh-experimental-client-ui-voice-input` - 录音与准备流程的全部文案走客户端字典
- `dsh-experimental-inspector` - 检查器面板文案走客户端字典
- `dsh-experimental-session-inspector` - tab 标题与描述走客户端字典
- `dsh-session-log-export` - 注册 session-log-download 命名空间的中英文字典
