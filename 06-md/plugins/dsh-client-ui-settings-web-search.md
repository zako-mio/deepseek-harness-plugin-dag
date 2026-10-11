# dsh-client-ui-settings-web-search

- 包名: `@deepseek-ai/dsh-client-ui-settings-web-search`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-web-search`

## 实现逻辑
DeepSeek 搜索提供方设置页（浏览器半）。apply 绑定 settings.webSearch 字典，用 web-search-deepseek 命名空间的表单构造 WebSearchCardController，并订阅 credentials/reference-updated 以刷新凭据状态（该凭据不属任何 settings 段，此事件是「别处写入的 key 已到 Host」的唯一信号）(src/client/index.ts:45-56)。页面注册进 plugins.item（order 20）(src/client/index.ts:57-59)。控制器把 apiKeyEnv/baseURL/maxUses 三个段内字段与一个段外凭据字段（默认引用 DEEPSEEK_API_KEY，草稿每次加载都从空开始）统一暂存，使一次保存覆盖页面显示的全部内容 (src/client/web-search-card-controller.ts:25-41)。Host 半是空 apply，命名空间由搜索提供方注册 (src/index.ts:11)。

## Provides

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 凭据状态读取与凭据引用更新事件都经 Remote 的 credentials 命名空间
  - 证据: `src/client/index.ts:18 import type {} from '@deepseek-ai/dsh-api-remotes/client' + src/client/index.ts:54 ctx.remote.$on('credentials/reference-updated', ...)`
- `dsh-client-locale` [E1+E2] - 注册 settings.webSearch 字典并按命名空间绑定翻译
  - 证据: `src/client/index.ts:10 import type {} from '@deepseek-ai/dsh-client-locale/client' + src/client/index.ts:46-47 ctx.locale.bind(NS) / ctx.locale.register(NS, { zh, en })`
- `dsh-client-ui-plugin-manager` [E1+E2] - 页面必须注册进 Plugins 页声明的 plugins.item 槽
  - 证据: `src/client/WebSearchCard.tsx:7 import type {} from '@deepseek-ai/dsh-client-ui-plugin-manager/client' + src/client/index.ts:57 ctx.slots.inject('plugins.item', ...)`
- `dsh-client-ui-primitives` [编译依赖] - 设置页复用共享表单、密钥字段与字典标签契约
  - 证据: `src/client/WebSearchCard.tsx:8 import SettingsForm/SettingsSecretField 等 + src/client/locales.ts:3 import SettingsFormLabels + package.json:54 devDependencies`
- `dsh-client-ui-renderer` [编译依赖] - 拉入 SlotRegistry 服务合并，使槽注册与 slots.inject 在此编译单元可用
  - 证据: `src/client/index.ts:16 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-settings` [E1+E2] - 搜索命名空间的共享配置表单读写与 whileServed 判定都经该服务
  - 证据: `src/client/index.ts:13 import type {} from '@deepseek-ai/dsh-client-ui-settings/client' + src/client/index.ts:48 ctx.configForms.get(WEB_SEARCH_NS)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
