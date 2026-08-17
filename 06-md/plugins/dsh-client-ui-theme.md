# dsh-client-ui-theme

- 包名: `@deepseek-ai/dsh-client-ui-theme`
- 分组: G26 客户端runtime
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-theme`

## 为什么需要它（设计初衷）
主题插件：Host 引导预插件调色板、DOM-free ThemeRuntime（light/dark/system）、--dsw-* token 样式与 Appearance 设置行。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-theme/package.json

## 实现逻辑
双面主题插件。node 半：ctx.inject(['settings']) 注册 THEME_SETTINGS_NAMESPACE 的 ThemeSettingsSchema；ctx.inject(['webServer']) 挂 tapIndex→injectBootTheme——在 body 后内联脚本按持久化偏好设置 colorScheme+data-ds-dark-theme（pre-plugin 预着色，system 在浏览器解析）。browser 半：ThemeRuntime——DOM-free（presenter 由 ui-layout 消费 snapshot），持有 prefers-color-scheme media query（system 偏好下 OS 切换触发 publish），register()/overrideTokens()（seq 序层折叠，later 层 per-token 胜出），setTheme 写 settingsScope；注册 'theme/change' 事件；把 AppearanceRow 注册进 settings.general.item slot（order 10）。styles/ 提供 --dsw-* token 与 base/design-platform/scrollbar/shiki CSS。

## Provides
- ctx.theme（ThemeRuntime/ThemeSnapshot）
- 事件：theme/change
- boot-theme 内联脚本（tapIndex 注入）
- settings.general.item slot 行（id: 'appearance'）
- 命名空间：settings.theme
- --dsw-* token stylesheets

## Depends On (上游依赖)
- `dsh-api-remotes` [运行时依赖] - settings 刷新 remote 通道
  - 证据: `packages/client/ui-theme/src/client/index.ts:376（inject ['remote']）`
- `dsh-client-connection` [运行时依赖] - 传输/remote 通道
  - 证据: `packages/client/ui-theme/src/client/index.ts:376（inject ['connection']）`
- `dsh-client-locale` [编译依赖] - locale Context 合并（ctx.locale）
  - 证据: `packages/client/ui-theme/src/client/index.ts:17（import type {} from '@deepseek-ai/dsh-client-locale/client'）；package.json peerDependencies + dsh.client.inject 含 locale`
- `dsh-client-runtime` [编译依赖] - ClientContext/slots 服务
  - 证据: `packages/client/ui-theme/src/client/index.ts:12（import type { ClientContext, SettingsScope } from '@deepseek-ai/dsh-client-runtime/client'）；package.json dsh.client.inject 含 runtime`
- `dsh-client-ui-settings` [运行时依赖] - 持久化主题偏好（settings 文档）
  - 证据: `packages/client/ui-theme/src/client/index.ts:376（inject ['settingsScope']）、:385（ctx.settingsScope.bind({namespace})）`

## Dependents (下游被依赖)
- `dsh-client-ui-layout` - ctx.theme 服务与主题事件流
- `dsh-cordis-client-runner` - 动态包可经 ctx.theme.overrideTokens 挂 token 覆盖层
