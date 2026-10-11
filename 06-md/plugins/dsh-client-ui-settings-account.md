# dsh-client-ui-settings-account

- 包名: `@deepseek-ai/dsh-client-ui-settings-account`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 13
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-account`

## 实现逻辑
桌面端账户设置插件。浏览器半在非 Desktop 渲染器直接 return，仅在 dshDesktop 存在时注册全部账户 UI (src/client/index.ts:43-44)；用一条 ctx.remote.$stream 订阅账户状态流，按 credential-stored 与 attempt.phase==='succeeded' 驱动资料/余额读取与默认模型初始化 (src/client/index.ts:108-135)。bonus 通知控制器负责读未通知奖励、在卡片报告已呈现后才 ack，并在设置面板关闭后仍存活 (src/client/index.ts:58-77)。账户区只在 view 为 credential-stored 时动态注册/撤销 settings.section 条目 (src/client/index.ts:288-304)。Host 半用 schemastery 定义含 volatile 引导进度的 Config，并在 webserver/index-inject 里把联系表单与 bonus 重试参数以 global 注入页面，同时以 settings.configure({auto:false}) 关闭自动注册 (src/index.ts:27-55)。

## Provides

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 账户流、登录、登出、bonus 读/ack 全部经 Remote 账户命名空间
  - 证据: `src/client/index.ts:11 import type {} from '@deepseek-ai/dsh-api-remotes/client' + src/client/index.ts:62 ctx.remote.account.getUnnotifiedBonuses(...)`
- `dsh-client-locale` [E1+E2] - 注册账户字典并按 settings.account 命名空间绑定翻译
  - 证据: `src/client/index.ts:5 import type {} from '@deepseek-ai/dsh-client-locale/client' + src/client/index.ts:45 ctx.locale.register('settings.account', { en, zh })`
- `dsh-client-product-analytics` [E1+E2] - 引导各步与配额通知上报产品分析事件（可选服务用 ctx.get 读取）
  - 证据: `src/client/DesktopOnboarding.tsx:2 import ProductEventMap + src/client/index.ts:102 ctx.get('productAnalytics')?.track(...)`
- `dsh-client-ui-chat` [编译依赖] - 配额通知注册进 chat 声明的 shell.quota-notice 并复用其 owner props 类型；引导写入 chat 的 transcriptView 偏好
  - 证据: `src/client/AccountQuotaNotice.tsx:5 import QuotaNoticeOwnerProps + src/client/index.ts:3 import TranscriptViewMode`
- `dsh-client-ui-layout` [编译依赖] - 平台页宿主与桌面引导条目注册进 layout 声明的 shell.overlay
  - 证据: `src/client/AccountPlatformHost.tsx:2 import type {} from '@deepseek-ai/dsh-client-ui-layout/client' + src/client/DesktopOnboardingEntry.tsx:4 同源`
- `dsh-client-ui-primitives` [编译依赖] - 登录/登出/充值等对话框与账户区复用共享原子控件与图标
  - 证据: `src/client/AccountAvatar.tsx:3 import IconUserOutlineMedium + src/client/AccountSection.tsx:4 import Button/IconRightUpOutlineRegular`
- `dsh-client-ui-renderer` [编译依赖] - 拉入 SlotRegistry 服务合并，使槽注册在此编译单元可用
  - 证据: `src/client/index.ts:7 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-settings` [E1+E2] - 经共享配置表单读写引导进度与 developerTools 偏好
  - 证据: `src/client/index.ts:6 import type {} from '@deepseek-ai/dsh-client-ui-settings/client' + src/client/index.ts:235 ctx.configForms.get<OnboardingSettings>(...)`
- `dsh-client-ui-settings-models` [编译依赖] - 向 ui-settings-models 声明的 settings.models.sign-in 槽注册登录引导（槽位声明依赖）
  - 证据: `src/client/AccountOnboarding.tsx:4 import type {} from '@deepseek-ai/dsh-client-ui-settings-models/client'`
- `dsh-client-ui-theme` [E1+E2] - 账户区跟随主题快照并通过 theme/change 事件重渲染
  - 证据: `src/client/AccountSection.tsx:7 import ThemeSnapshot + src/client/index.ts:202 ctx.theme.getTheme() + src/client/index.ts:203 ctx.on('theme/change', listener)`
- `dsh-host-webserver` [E1+E2] - Host 半借 webserver 的 index-inject 钩子把公开联系配置注入页面初始化数据
  - 证据: `src/index.ts:3 import type {} from '@deepseek-ai/dsh-host-webserver' + src/index.ts:50 ctx.on('webserver/index-inject', table => ...)`
- `dsh-settings` [E1+E2] - 把本插件的 Config 以 auto:false 显式登记进 settings 服务，交由浏览器半经配置表单读取
  - 证据: `src/index.ts:4 import type {} from '@deepseek-ai/dsh-settings' + src/index.ts:47-49 ctx.inject(['settings'], scope => scope.settings.configure({ auto: false }, ctx.fiber))`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
