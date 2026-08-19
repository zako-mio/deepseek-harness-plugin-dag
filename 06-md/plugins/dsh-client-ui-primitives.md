# dsh-client-ui-primitives

- 包名: `@deepseek-ai/dsh-client-ui-primitives`
- 分组: G29 UI底座
- 拓扑层: Layer 0
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-primitives`

## 为什么需要它（设计初衷）
解决浏览器端 UI 原子组件复用问题：提供纯 React 原子组件库（零 cordis 依赖），包括按钮/弹窗/菜单、Markdown/TeX 渲染、终端输出、diff、read、search、web 结果等工具结果卡片，供各业务 UI 插件复用，保证对话区渲染一致性与安全性（对非可信模型输出做链接/HTML 消毒）。

发展史：定位为 UI 基础层，独立于应用逻辑。含大量基于实现笔记的迭代（如 2026-07-28 web-terminal-card、2026-07-30 web-read/diff/search/result-card、2026-08-06 web-markdown-incremental-ast-renderer），持续强化流式渲染与安全。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-primitives/README.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-client-ui-primitives

## 实现逻辑
通用 UI atoms 底座（零 cordis 运行时依赖）。纯 React 组件库：Button/Input/Menu/Modal/Tooltip/HoverCard/Pill/Toast/StateDot/DisclosureRow/JsonTree/DiffBlock/ReadBlock/SearchBlock/TerminalBlock/WebBlock/RiskConfirmation/OnboardingSurface/ConnectionBanner/Button 等控件、icons 图标集、markdown 管线（parse/render/CodeBlock/JsonBlock/MessageText/MarkdownText/katex/shiki 高亮/ansi）与 MarkdownFileMentions 类型。RC7 新增 useDismissOnOutsidePointer hook(外部点击关闭，ui-jobs/ui-cordis 等 popover 复用)。不注册任何 slot/service，作为 import 底座被全部 UI 插件消费。

## Provides
- React atoms（Button/Input/Menu/Modal/Tooltip/StateDot/DisclosureRow/ReadBlock/SearchBlock/TerminalBlock/WebBlock/DiffBlock/JsonTree 等）
- 图标集 icons
- Markdown 渲染管线（MarkdownText/MessageText/CodeBlock/JsonBlock/katex/shiki/ansi）
- useDismissOnOutsidePointer(外部点击关闭 hook，RC7 新增)
- 类型 MarkdownFileMentions/extractMarkdownPlainText

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- `dsh-client-ui-attachment` - 基础 atoms
- `dsh-client-ui-brand-official` - 复用官方品牌图形组件
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
