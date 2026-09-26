# dsh-client-ui-theme

- 包名: `@deepseek-ai/dsh-client-ui-theme`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-theme`

## 实现逻辑
浏览器主题注册表：ThemeRuntime 持有 light/dark/system 偏好、字号与 token 覆盖层，用 prefers-color-scheme 解析 system，发布不可变 ThemeSnapshot 并 emit 'theme/change'（src/client/index.ts:159-360）。apply 安装全局 --dsw-* 样式表、创建 ThemeRuntime 并 ctx.provide('theme')，再向 settings.general.item 注册 appearance 与 font-size 两行（src/client/index.ts:429-478）。Host 半 src/index.ts 通过 webserver/index-inject 注入 boot 调色板与字号脚本，避免首屏闪色（src/index.ts:39-43）。

## Provides
- ctx.theme（主题服务：getTheme/setTheme/setFontSize/register/overrideTokens）
- 事件 theme/change（主题或字号变更）
- slot settings.general.item 的 appearance 与 font-size 设置行
- Host 侧 webserver/index-inject 的 boot 主题行与 Config（preference/fontSize）

## Depends On (上游依赖)
- `dsh-client-locale` [E1+E2] - 注册 settings.theme 字典
  - 证据: `src/client/index.ts:16 + src/client/index.ts:435 ctx.locale.register`
- `dsh-client-ui-renderer` [编译依赖] - 拉入 SlotRegistry 服务合并类型
  - 证据: `src/client/index.ts:18 import type`
- `dsh-client-ui-settings` [E1+E2] - 读取/持久化主题偏好并注册 settings.general.item 槽
  - 证据: `src/client/index.ts:14 import type + src/client/index.ts:431 ctx.configForms.get`
- `dsh-host-webserver` [E1+E2] - 向 HTML index 注入 boot 主题样式与脚本
  - 证据: `src/index.ts:9 import type + src/index.ts:41 ctx.on('webserver/index-inject')`
- `dsh-settings` [E1+E2] - Host 侧设置作用域配置（关闭自动保存）
  - 证据: `src/index.ts:2 import type + src/index.ts:40 child.settings.configure`

## Dependents (下游被依赖)
- `dsh-client-ui-layout` - 读取主题快照并订阅主题变化以投影到 DOM
- `dsh-client-ui-settings-account` - 主题区分账户界面外观
- `dsh-client-ui-sidebar-terminal` - 终端配色跟随全局主题快照，订阅 theme/change
- `dsh-cordis-client-runner` - 动态半渲染时读取主题令牌
