# dsh-client-ui-theme

- 包名: `@deepseek-ai/dsh-client-ui-theme`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-theme`

## 实现逻辑
主题与排版偏好的 Host+浏览器双半插件：Host 侧 src/index.ts:38-46 用 schemastery 声明 Volatile Config（preference、三档字号、三档字体），:52-64 在 webserver/index-inject 上 prepend 启动脚本注入（boot-theme.ts:9 提供 IndexInjection），使首屏在插件启动前就有调色板。浏览器侧 client/index.ts:163-396 的 ThemeRuntime 持有主题注册表、preference、字号/字体与 override 层，:391-395 每次变更 emit theme/change，:380-389 按 seq 叠加 override 并挑选当前配色模式的值；:486-490 的 apply 用 ctx.provide('theme', theme) 提供服务，:512-535 把 AppearanceRow 与 FontSettingsGroup 注册进 settings.general.item。

## Provides
- ctx.theme (主题注册表与 preference/字号/字体运行时，含 overrideTokens)
- 事件 theme/change（主题或排版变更时发布不可变快照）
- 槽位贡献 settings.general.item 的 appearance / font-size 行
- Host 侧启动期调色板与字体变量注入（webserver/index-inject）

## Depends On (上游依赖)
- `dsh-client-locale` [E1+E2] - 外观与字体设置行文案本地化
  - 证据: `src/client/index.ts:17 import type {} from '@deepseek-ai/dsh-client-locale/client'; src/client/index.ts:492 ctx.locale.register(SETTINGS_NS, { zh, en })`
- `dsh-client-ui-primitives` [编译依赖] - 设置行控件复用共享原语
  - 证据: `src/client/FontFamilyRow.tsx:8 import ... from '@deepseek-ai/dsh-client-ui-primitives'`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 服务由 renderer 提供
  - 证据: `src/client/index.ts:19 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-settings` [E1+E2] - 偏好经 settings 配置表单持久化，设置行也注册进其 item 槽
  - 证据: `src/client/index.ts:15 import type { ConfigForm } from '@deepseek-ai/dsh-client-ui-settings/client'; src/client/index.ts:488 ctx.configForms.get<ThemeSettings>(THEME_SETTINGS_NAMESPACE)`
- `dsh-host-webserver` [E1+E2] - 把启动期主题与字体注入浏览器页面索引
  - 证据: `src/index.ts:9 import type {} from '@deepseek-ai/dsh-host-webserver'; src/index.ts:54-55 ctx.on('webserver/index-inject', ...)`
- `dsh-settings` [E1+E2] - Host 侧把主题偏好登记为不可自动生成设置的字段
  - 证据: `src/index.ts:2 import type {} from '@deepseek-ai/dsh-settings'; src/index.ts:53 child.settings.configure({ auto: false }, ctx.fiber)`

## Dependents (下游被依赖)
- `dsh-client-ui-layout` - 把主题快照投影到 document.body
- `dsh-client-ui-settings-account` - 账户区跟随主题快照并通过 theme/change 事件重渲染
- `dsh-client-ui-sidebar-terminal` - 终端配色与字号跟随活动主题，主题切换时重绘
- `dsh-cordis-client-runner` - 在浏览器门面中把主题覆写来源钉到包 id，并向 Client Inspect 暴露主题能力
