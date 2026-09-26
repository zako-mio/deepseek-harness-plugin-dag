# dsh-client-ui-primitives

- 包名: `@deepseek-ai/dsh-client-ui-primitives`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 0
- 来源层: L3 其余
- 源码路径: `packages/client/ui-primitives`

## 实现逻辑
无 cordis 服务与槽注册的纯 React 组件/工具库：入口 src/index.ts 汇总导出约 80 个组件与工具，覆盖基础控件（Button/Input/Switch/Checkbox/Menu/MenuSurface/SegmentedControl/Modal/Tooltip/Toast 等）、工具输出展示块（ReadBlock/DiffBlock/SearchBlock/WebBlock/TerminalBlock/JsonTree）、Markdown 渲染与高亮（markdown/*、code-highlighting.ts）、设置表单（settings-form/*）以及一批图标与平台/时间工具。组件仅依赖 --dsw-* 设计 token，跨包复用代码集中在少数浏览器安全工具依赖上：PathLabel 用 dsh-util-workspace-path（src/PathLabel.tsx:4）、代码高亮用 dsh-util-code-language（src/code-highlighting.ts:10）、设置表单模型用 dsh-client-store（src/settings-form/form-model.ts:16）。

## Provides
- React 基础控件库（Button/Input/Switch/Checkbox/Menu/MenuSurface/SegmentedControl/Tabs/Modal/HoverCard/Tooltip/Toast/Pill/Tag/DisclosureRow/TextShimmer/StateDot/ConnectionIndicator/RiskConfirmation 等）
- 工具结果展示块（ReadBlock / DiffBlock / SearchBlock / WebBlock / TerminalBlock / JsonTree / CodeBlock / JsonBlock）
- Markdown 渲染与文件/图片链接、数学公式、增量高亮与纯文本提取（MarkdownText / MarkdownDelegateProvider / extractMarkdownPlainText）
- 设置表单组件与模型（SettingsForm / SettingsSecretField / SettingsValueField / SettingsFormModel / settingsTextField / settingsNumberField）
- 图标与品牌图形集合（icons/*、FileTypeIcon、LinkIcon、ReferenceIcon、PermissionIcon、FishLogo、BrandWordmark、plugin-artwork、guide-artwork）
- 通用钩子与工具（useAnchoredPosition/useAnchoredMaxHeight/useDismissOnOutsidePointer/useModalLayer/useCodeHighlighter/relativeTime/rankByName/fileSizeText/writeClipboard/observeComposition）

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-client-locale` - Language 行复用共享 UI 原语
- `dsh-client-shortcuts` - 复用 UI 原语渲染/呈现键帽
- `dsh-client-ui-agent-preset` - 复用基础 UI 组件渲染 chip 与设置行
- `dsh-client-ui-approval` - 审批面板复用基础组件
- `dsh-client-ui-attachment` - 附件卡片与图片画廊的基础组件
- `dsh-client-ui-brand-official` - 品牌标志与品牌名的呈现组件
- `dsh-client-ui-chat` - 聊天行/卡片的基础组件
- `dsh-client-ui-commands` - 命令弹层组件与候选排序函数
- `dsh-client-ui-conversation` - composer 图标与基础组件
- `dsh-client-ui-cordis` - 复用客户端基础 UI 原子组件
- `dsh-client-ui-deliverables` - 卡片与 diff 视图基础组件
- `dsh-client-ui-dockkit` - 菜单/面板等基础组件
- `dsh-client-ui-goal` - 命令输入视图基础组件
- `dsh-client-ui-input-trigger` - 候选菜单列表基础组件
- `dsh-client-ui-message-feedback` - 复用 ui-primitives 的 Toast/Button 等控件
- `dsh-client-ui-model-selection` - 复用图标与 MenuSurface 控件
- `dsh-client-ui-open-in-app` - 复用 Toast/图标/按钮控件
- `dsh-client-ui-permission-presets` - 复用 Menu/Select/图标控件
- `dsh-client-ui-plan` - 复用 Markdown/图标/纯文本提取
- `dsh-client-ui-reference` - 会话候选相对时间展示
- `dsh-client-ui-schedule` - 复用按钮/图标/toast 等控件
- `dsh-client-ui-settings-account` - 复用按钮/图标等控件
- `dsh-client-ui-settings-agent-loop` - 复用共享设置表单原语渲染数值字段
- `dsh-client-ui-settings-general` - 复用共享原语关闭顶层模态并渲染设置行
- `dsh-client-ui-settings-models` - 复用共享 UI 原语渲染模型编辑器
- `dsh-client-ui-settings-plugin-inventory` - 复用菜单、状态点与标签原语
- `dsh-client-ui-settings-shell` - 复用共享设置表单原语
- `dsh-client-ui-settings-subagent` - 复用共享设置字段原语
- `dsh-client-ui-settings-web-search` - 复用共享设置表单原语
- `dsh-client-ui-shortcuts` - 复用编辑器/菜单原语并关闭顶层模态
- `dsh-client-ui-sidebar-browser` - 复用共享 UI 原语
- `dsh-client-ui-sidebar-documentpreview` - 复用加载指示与代码高亮扩展名等共享原语
- `dsh-client-ui-sidebar-files` - 复用共享 UI 原语
- `dsh-client-ui-sidebar-right` - 复用共享 UI 原语
- `dsh-client-ui-sidebar-terminal` - 复用终端图标原语
- `dsh-client-ui-skill` - 候选按名称排序（与命令组一致）
- `dsh-client-ui-subagent` - 复用图标、Tooltip、StateDot 等原语
- `dsh-client-ui-tool` - 复用对话卡片原语与标签
- `dsh-client-ui-trajectory` - 复用表格、时间线等展示原语
- `dsh-client-ui-workflow-run` - 复用折叠行与状态点原语
- `dsh-client-ui-workspace` - 复用菜单项、对话框等原语
- `dsh-client-web` - 种子静态模块表内联 UI 原语库
- `dsh-experimental-client-ui-voice-input` - 复用基础 UI 组件
- `dsh-session-log-export` - 复用 Button/Menu/Modal 等基础组件渲染菜单与下载弹窗
