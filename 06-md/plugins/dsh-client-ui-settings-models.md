# dsh-client-ui-settings-models

- 包名: `@deepseek-ai/dsh-client-ui-settings-models`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-models`

## 实现逻辑
浏览器半向 `settings.section` 注册 Models 页（id='models' order 10，声明 settings.models.provider-card 与 settings.models.footer 子槽，src/client/index.ts:136-146），并向 `settings.onboarding` 注册 welcome-notice（order -100）与 deepseek-official（order 0，声明 settings.models.sign-in 子槽）两个引导步骤（src/client/index.ts:147-159）。它经 `ctx.settingsSchema` 与 `ctx.configForms.describe()` 构造 ModelsSettingsStore/operations（src/client/index.ts:84-88），并订阅 settings/document-updated、credentials/record-updated、credentials/reference-updated、llm/adapters-updated 及 connection/reset 推送事件刷新（src/client/index.ts:121-134）。node half 监听 `webserver/index-inject` 把 credentialOnboarding 开关注入页面全局（src/index.ts:14-21）。

## Provides
- settings.section 条目 id='models' (order 10)：模型/供应商编辑页，声明 settings.models.provider-card（keyed）与 settings.models.footer（list）子槽
- settings.onboarding 条目 id='welcome-notice' (order -100) 与 id='deepseek-official' (order 0，声明 settings.models.sign-in 子槽)
- settings.models locale 命名空间字典（Models 页 + 产品引导文案）
- Host 侧页面全局 ONBOARDING_CONFIG_GLOBAL（credentialOnboarding 开关）

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 订阅 Host 推送的设置/凭据/适配器失效事件
  - 证据: `src/client/index.ts:17 type-only import + src/client/index.ts:124-127 ctx.remote.$on(...)`
- `dsh-client-locale` [E1+E2] - 注册并绑定 settings.models 字典
  - 证据: `src/client/index.ts:13 type-only import + src/client/index.ts:91 ctx.locale.bind(NS)`
- `dsh-client-ui-primitives` [编译依赖] - 复用共享 UI 原语渲染模型编辑器
  - 证据: `src/client/ModelsSection.tsx:26 import`
- `dsh-client-ui-renderer` [编译依赖] - 引入 ctx.slots 合并
  - 证据: `src/client/index.ts:14 type-only import`
- `dsh-client-ui-settings` [E1+E2] - 设置槽声明、settingsSchema/configForms 镜像由 ui-settings 提供
  - 证据: `src/client/index.ts:11 type-only import + src/client/index.ts:88 ctx.configForms.describe()`
- `dsh-host-webserver` [E1+E2] - Host 侧向浏览器页面注入引导配置全局
  - 证据: `src/index.ts:4 type-only import + src/index.ts:15 ctx.on('webserver/index-inject')`

## Dependents (下游被依赖)
- `dsh-client-ui-settings-account` - 登录引导复用模型设置区类型
