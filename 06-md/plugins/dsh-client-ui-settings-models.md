# dsh-client-ui-settings-models

- 包名: `@deepseek-ai/dsh-client-ui-settings-models`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-models`

## 实现逻辑
模型设置与产品引导插件。Host 半在 webserver/index-inject 里把 credentialOnboarding 以 global 注入页面 (src/index.ts:14-21)，浏览器半读回该 global 并在非桌面环境决定是否自动弹引导 (src/client/index.ts:79-82)。ModelsSettingsStore 把可配置 provider 目录、设置命名空间与凭据 describe 连接成一份页面快照，Host 始终是唯一事实源 (src/client/store.ts:1-17)；所有写操作经 createModelsOperations 走 credentials/settings/llm 三条 Remote 并区分 written/conflict/refused (src/client/operations.ts:82-100)。apply 注册 settings.section 的 models 段（order 10）并声明 provider-card 与 footer 两个子槽 (src/client/index.ts:138-148)，另注册 welcome-notice 与 deepseek-official 两个 onboarding 步骤，其中后者再声明 settings.models.sign-in 单槽 (src/client/index.ts:149-161)。推送失效只在页面已加载（status!=='idle'）时才触发重取，避免后台失效拉起未打开的页面 (src/client/index.ts:57-60,123-136)。

## Provides
- 声明 settings.section 的 models 导航段，及其子槽 settings.models.provider-card（keyed）与 settings.models.footer（list）
- 声明 settings.models.sign-in 单槽（登录引导的挂载点，供账户插件注册）
- 向 settings.onboarding 列表贡献 welcome-notice 与 deepseek-official 两个引导步骤

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - provider 目录、凭据与模型发现全部经 Remote 命名空间，并订阅四类推送失效
  - 证据: `src/client/ModelListEditor.tsx:19 import LlmDiscoveredModel + src/client/index.ts:126-129 ctx.remote.$on('settings/document-updated'|'credentials/record-updated'|'credentials/reference-updated'|'llm/adapters-updated')`
- `dsh-client-locale` [E1+E2] - 注册 settings.models 字典并绑定导航标签与页面文案的翻译
  - 证据: `src/client/index.ts:14 import type {} from '@deepseek-ai/dsh-client-locale/client' + src/client/index.ts:83 ctx.locale.register(NS, { zh, en })`
- `dsh-client-product-analytics` [E1+E2] - 引导对话框上报产品分析事件（可选服务经 ctx.get 读取）
  - 证据: `src/client/DeepSeekOnboardingDialog.tsx:8 import TrackProductEvent + src/client/index.ts:102 ctx.get('productAnalytics')?.track(...)`
- `dsh-client-ui-primitives` [编译依赖] - 模型页与其编辑器复用共享原子控件与模态
  - 证据: `src/client/ModelsSection.tsx:26 import Button/Modal/SegmentedControl + src/client/ModelInputTypes.tsx:4 import Checkbox + package.json:52 devDependencies`
- `dsh-client-ui-renderer` [编译依赖] - 拉入 SlotRegistry 服务合并，使槽声明与注册在此编译单元可用
  - 证据: `src/client/index.ts:15 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-settings` [E1+E2] - 页面经共享配置表单镜像读取命名空间与 revision，并在其推送下刷新
  - 证据: `src/client/index.ts:12 import type {} from '@deepseek-ai/dsh-client-ui-settings/client' + src/client/index.ts:89 ctx.configForms.describe() + src/client/store.ts:16 import SettingsDescribeFace`
- `dsh-host-webserver` [E1+E2] - Host 半借 webserver 的 index-inject 钩子把 credentialOnboarding 注入页面 global
  - 证据: `src/index.ts:4 import type {} from '@deepseek-ai/dsh-host-webserver' + src/index.ts:15 ctx.on('webserver/index-inject', table => ...)`

## Dependents (下游被依赖)
- `dsh-client-ui-settings-account` - 向 ui-settings-models 声明的 settings.models.sign-in 槽注册登录引导（槽位声明依赖）
