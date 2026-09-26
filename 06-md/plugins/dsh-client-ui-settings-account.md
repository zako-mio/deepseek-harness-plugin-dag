# dsh-client-ui-settings-account

- 包名: `@deepseek-ai/dsh-client-ui-settings-account`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 17
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-account`

## 实现逻辑
仅在桌面渲染器下生效（apply 开头检测 globalThis.dshDesktop，src/client/index.ts:42）。桌面半 src/index.ts 注册 webserver/index-inject 以注入联系方式配置（src/index.ts:50）。客户端核心是 account 状态流：订阅 ctx.remote.$stream({name:'account'})，逐帧 publish 账户视图并在首次登录成功时初始化默认模型（src/client/index.ts:150-176）；refresh 并行读 profile/balance，notices 控制器读/确认未通知奖励（index.ts:64-93）。UI 面注册 settings.launcher（AccountMenu）、settings.section（登录后才有 AccountSection，index.ts:265-282）、settings.models.sign-in 的 AccountOnboarding、shell.quota-notice 的 AccountQuotaNotice，以及桌面引导与原生平台 overlay（index.ts:230-260）。

## Provides
- settings.launcher 条目 AccountMenu（账户头像/菜单）
- settings.section 条目 'account'（仅凭据已存储时注册的账户设置区）
- settings.models.sign-in 条目 AccountOnboarding（登录/引导面板）
- shell.quota-notice 条目 AccountQuotaNotice（额度耗尽提示）
- shell.overlay 条目 'desktop-onboarding' 与 'account.platform-page'（桌面引导与原生平台页宿主）
- Host 侧账户联系信息配置注入（src/index.ts 的 webserver/index-inject）

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 调用 account/session Remote 与订阅转发事件
  - 证据: `src/client/index.ts:10 import + src/client/index.ts:107 ctx.remote.account.getProfile`
- `dsh-client-locale` [运行时依赖] - 注册账户文案
  - 证据: `src/client/index.ts:4 import + src/client/index.ts:44 ctx.locale.register('settings.account')`
- `dsh-client-ui-chat` [E1+E2] - 复用 chat 的类型面并写 ui-chat 设置（transcriptView/performanceUsage）
  - 证据: `src/client/AccountQuotaNotice.tsx:5 import + src/client/index.ts:2 import type { TranscriptViewMode }`
- `dsh-client-ui-layout` [编译依赖] - 壳层布局类型面
  - 证据: `src/client/index.ts:9 import type + src/client/AccountPlatformHost.tsx:2 import`
- `dsh-client-ui-primitives` [编译依赖] - 复用按钮/图标等控件
  - 证据: `src/client/AccountAvatar.tsx:3 import + src/client/AccountMenu.tsx:5`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 槽注册表
  - 证据: `src/client/index.ts:6 import type + src/client/index.ts:40 inject 'slots'`
- `dsh-client-ui-settings` [E1+E2] - 读/写 onboarding 等设置命名空间
  - 证据: `src/client/index.ts:5 import + src/client/index.ts:213 ctx.configForms.get`
- `dsh-client-ui-settings-models` [编译依赖] - 登录引导复用模型设置区类型
  - 证据: `src/client/AccountOnboarding.tsx:4 import`
- `dsh-client-ui-theme` [E1+E2] - 主题区分账户界面外观
  - 证据: `src/client/AccountSection.tsx:7 import + src/client/index.ts:180 ctx.theme.getTheme`
- `dsh-host-webserver` [E1+E2] - 向 webserver 注入账户联系方式配置
  - 证据: `src/index.ts:3 import + src/index.ts:50 ctx.on('webserver/index-inject')`
- `dsh-settings` [编译依赖] - Host 侧设置命名空间类型/接口
  - 证据: `src/index.ts:4 import`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
