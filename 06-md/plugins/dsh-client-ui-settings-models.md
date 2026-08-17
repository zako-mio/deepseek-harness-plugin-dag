# dsh-client-ui-settings-models

- 包名: `@deepseek-ai/dsh-client-ui-settings-models`
- 分组: G28 设置输入UI
- 拓扑层: Layer 11
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-models`

## 为什么需要它（设计初衷）
模型设置与共享产品引导对话框，叠在既有设置与凭据连接之上。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-settings-models/package.json

## 实现逻辑
Models 设置页与产品 onboarding：注册 settings.section id=models order=10（ModelsSection，index.ts:118-124），settings.onboarding welcome-notice(order=-100) 与 deepseek-official(order=0) 两个对话框。ModelsSettingsStore/WelcomeNoticeStore 经 connection.api 读写 Host settings/credentials；订阅 settings/document-updated、credentials/updated、llm/adapters-updated 推送失效（:107-113）。

## Provides
- settings.section 'models' 注册
- settings.onboarding 'welcome-notice' / 'deepseek-official' 注册
- settings.models 字典命名空间
- ModelsSettingsStore / WelcomeNoticeStore (connection.api 上)

## Depends On (上游依赖)
- `dsh-api-remotes` [运行时依赖] - 订阅 settings/credentials/adapters 失效事件
  - 证据: `packages/client/ui-settings-models/src/client/index.ts:107-113 (ctx.remote.$on 推送失效事件)`
- `dsh-client-connection` [运行时依赖] - settings/credentials 远程调用载体
  - 证据: `packages/client/ui-settings-models/src/client/index.ts:70-71 (connection.api 构造 store)`
- `dsh-client-ui-settings` [编译依赖] - settings.section 槽声明与 settingsScope 契约
  - 证据: `packages/client/ui-settings-models/src/client/index.ts:13 (type-only import), :118 (slots.inject('settings.section'))`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
