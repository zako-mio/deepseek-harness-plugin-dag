# dsh-client-ui-settings-plugins

- 包名: `@deepseek-ai/dsh-client-ui-settings-plugins`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-plugins`

## 实现逻辑
浏览器半向 `settings.section` 注册 Built-in plugins 导航条目（id='plugins' order 15，src/client/index.ts:76-84），并在注册项上声明子槽 `settings.plugins.tab`（list 类型，src/client/index.ts:83）。它把 tab 台账 `ctx.slots.entries('settings.plugins.tab')` 与 locale revision 组合成带缓存的 observable 快照（src/client/index.ts:42-72），使 language 切换时标签重解析。node half 为空 apply，仅用于出现在宿主 Loader（src/index.ts:11）。

## Provides
- settings.plugins locale 命名空间字典
- settings.section 条目 id='plugins' (order 15)：Built-in plugins 设置段外壳，声明 settings.plugins.tab (list) 子槽
- settings.plugins.tab 台账投影为有序 tab 条目 observable 源（标签 locale 跟随）

## Depends On (上游依赖)
- `dsh-client-locale` [E1+E2] - 注册并绑定本段文案，并订阅 locale revision
  - 证据: `src/client/index.ts:11 type-only import + src/client/index.ts:36 ctx.locale.bind(NS)`
- `dsh-client-ui-renderer` [编译依赖] - 引入 ctx.slots 合并
  - 证据: `src/client/index.ts:16 type-only import`
- `dsh-client-ui-settings` [E1+E2] - 复用设置外壳的 section 槽声明
  - 证据: `src/client/index.ts:15 type-only import + 经 settings.section 槽协作（src/client/index.ts:76）`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
