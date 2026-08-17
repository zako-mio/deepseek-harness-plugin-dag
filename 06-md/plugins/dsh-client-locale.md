# dsh-client-locale

- 包名: `@deepseek-ai/dsh-client-locale`
- 分组: G26 客户端runtime
- 拓扑层: Layer 11
- 来源层: L2 web-app
- 源码路径: `packages/client/locale`

## 为什么需要它（设计初衷）
解决浏览器 UI 多语言需求：提供 zh/en 偏好存储（settings.yaml 中 locale.preference），并在浏览器端提供 ns×locale 字典注册表，支持框架注入的 t() 翻译座位，使 UI 文案可本地化并实时切换，是 Web 客户端的国际化基础设施。

发展史：定位为 client 侧的 locale 运行时服务。2026-08-06 的 Host-backed preferences 决策确定了持久化边界（浏览器偏好由 Host settings 管理而非仅浏览器本地），早期部分界面仍保留内联文案。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/locale/README.md
- https://www.npmjs.com/package/@deepseek-ai/dsh-client-locale

## 实现逻辑
双面。node 半：ctx.inject(['settings']) 注册 LOCALE_SETTINGS_NAMESPACE 的 LocaleSettingsSchema（settingsNamespace）。browser 半：LocaleRuntime——字典注册（namespace×locale→dict，双语文档强制）、lookup 链（entry 命名空间 active→zh 回退→common 共享命名空间→key 原文）、bind(ns) 稳定 translate 引用、setLocale 写 settingsScope、浏览器语言检测（navigator.languages 主 subtag→zh/en，window 存在性测试防 node）。提供 LocaleFace（getSnapshot/subscribe/bind）经 ctx.slots.installLocale 装入渲染机制（t 座位），注册 'locale/change' 事件，并把 LanguageRow 注册进 settings.general.item slot（order 0）。

## Provides
- ctx.locale（LocaleRuntime/LocaleFace）
- 事件：locale/change
- LocaleFace 安装（t 座位）
- settings.general.item slot 行（id: 'language'）
- 命名空间：common、settings.locale

## Depends On (上游依赖)
- `dsh-api-remotes` [运行时依赖] - settings 刷新 remote 通道
  - 证据: `packages/client/locale/src/client/index.ts:347（inject ['remote']）`
- `dsh-client-connection` [运行时依赖] - 传输/remote 通道
  - 证据: `packages/client/locale/src/client/index.ts:347（inject ['connection']）`
- `dsh-client-runtime` [编译依赖] - ClientContext/类型与 slots 服务
  - 证据: `packages/client/locale/src/client/index.ts:16（import type { ClientContext, SettingsScope } from '@deepseek-ai/dsh-client-runtime/client'）；package.json dsh.client.inject 含 runtime`
- `dsh-client-ui-settings` [运行时依赖] - 持久化语言偏好
  - 证据: `packages/client/locale/src/client/index.ts:347（inject ['settingsScope']）、:356（ctx.settingsScope.bind({namespace})）`

## Dependents (下游被依赖)
- `dsh-client-ui-conversation` - 命名空间字典注册与 t 座位
- `dsh-client-ui-cordis` - 命名空间字典
- `dsh-client-ui-deliverables` - deliverables 命名空间字典
- `dsh-client-ui-directory-picker-browse` - 对话框字典（zh/en）
- `dsh-client-ui-goal` - goal 命名空间字典
- `dsh-client-ui-input-trigger` - 候选菜单本地化
- `dsh-client-ui-jobs` - job 命名空间字典
- `dsh-client-ui-message-feedback` - feedback 命名空间字典
- `dsh-client-ui-settings-plugins` - settings.plugins 字典
- `dsh-client-ui-sidebar` - sidebar 命名空间字典
- `dsh-client-ui-theme` - locale Context 合并（ctx.locale）
- `dsh-client-ui-tool` - locale 命名空间（复用 conversation 命名空间文案）
- `dsh-client-ui-trajectory` - 轨迹命名空间字典
- `dsh-client-ui-user-questions` - question 命名空间字典
- `dsh-client-ui-workflow-run` - workflowRun 命名空间字典
- `dsh-client-ui-workspace` - workspace 命名空间字典
- `dsh-client-web-react` - t 座位绑定与 locale 切换重渲染
