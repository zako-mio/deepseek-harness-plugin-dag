# dsh-client-ui-primitives

- 包名: `@deepseek-ai/dsh-client-ui-primitives`
- 分组: G29 UI底座
- 拓扑层: Layer 0
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-primitives`

## 实现逻辑
通用 UI atoms 底座（零 cordis 运行时依赖）。纯 React 组件库：Button/Input/Menu/Modal/Tooltip/HoverCard/Pill/Toast/StateDot/DisclosureRow/JsonTree/DiffBlock/ReadBlock/SearchBlock/TerminalBlock/WebBlock/RiskConfirmation/OnboardingSurface/ConnectionBanner/Button 等控件、icons 图标集、markdown 管线（parse/render/CodeBlock/JsonBlock/MessageText/MarkdownText/katex/shiki 高亮/ansi）与 MarkdownFileMentions 类型。不注册任何 slot/service，作为 import 底座被全部 UI 插件消费。

## Provides
- React atoms（Button/Input/Menu/Modal/Tooltip/StateDot/DisclosureRow/ReadBlock/SearchBlock/TerminalBlock/WebBlock/DiffBlock/JsonTree 等）
- 图标集 icons
- Markdown 渲染管线（MarkdownText/MessageText/CodeBlock/JsonBlock/katex/shiki/ansi）
- 类型 MarkdownFileMentions/extractMarkdownPlainText

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-client-ui-attachment` - 基础 atoms
- `dsh-client-ui-conversation` - 通用 UI atoms/图标/Markdown 渲染底座
- `dsh-client-ui-deliverables` - 产物内联提及类型
- `dsh-client-ui-directory-picker-browse` - UI atoms
- `dsh-client-ui-goal` - UI atoms
- `dsh-client-ui-jobs` - 状态点/图标 atoms
- `dsh-client-ui-message-feedback` - UI atoms
- `dsh-client-ui-sidebar` - UI atoms
- `dsh-client-ui-tool` - 图标/组件 atoms
- `dsh-client-ui-trajectory` - UI atoms + markdown 纯文本提取
- `dsh-client-ui-user-questions` - UI atoms
- `dsh-client-ui-workflow-run` - UI atoms
