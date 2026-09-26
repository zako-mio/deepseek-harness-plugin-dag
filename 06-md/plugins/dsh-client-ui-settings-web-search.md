# dsh-client-ui-settings-web-search

- 包名: `@deepseek-ai/dsh-client-ui-settings-web-search`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-web-search`

## 实现逻辑
浏览器半在 Host 服务 `web-search-deepseek` 命名空间时，把 Web Search 卡片注册进 `plugins.item`（id='web-search' order 40，src/client/index.ts:57-59）。控制器绑定该命名空间的 staged form（src/client/index.ts:48-49），并经 `ctx.remote.$on('credentials/reference-updated')` 在别处写入的密钥变更时刷新凭据态（src/client/index.ts:53-56）——注释说明这是该页能感知 Host 侧凭据更新的唯一信号。node half 为空 apply（src/index.ts:11）。

## Provides
- settings.webSearch locale 命名空间字典
- plugins.item 槽位条目 id='web-search' (order 40)：web 搜索提供者的 key / endpoint / 单次请求预算设置卡片

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 订阅 Host 推送的凭据失效事件以刷新密钥态
  - 证据: `src/client/index.ts:18 type-only import + src/client/index.ts:54 ctx.remote.$on('credentials/reference-updated')`
- `dsh-client-locale` [E1+E2] - 注册并绑定本页文案
  - 证据: `src/client/index.ts:10 type-only import + src/client/index.ts:46 ctx.locale.bind(NS)`
- `dsh-client-ui-plugin-manager` [E1+E2] - Plugins 页拥有 plugins.item 槽位
  - 证据: `src/client/index.ts:15 type-only import + src/client/index.ts:57-58 向 plugins.item 注册`
- `dsh-client-ui-primitives` [编译依赖] - 复用共享设置表单原语
  - 证据: `src/client/WebSearchCard.tsx:8 import + src/client/locales.ts:3 import`
- `dsh-client-ui-renderer` [编译依赖] - 引入 ctx.slots 合并
  - 证据: `src/client/index.ts:16 type-only import`
- `dsh-client-ui-settings` [E1+E2] - 经 configForms 取得命名空间的表单 scope
  - 证据: `src/client/index.ts:13 type-only import + src/client/index.ts:48 ctx.configForms.get(WEB_SEARCH_NS)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
