# dsh-client-ui-settings-shell

- 包名: `@deepseek-ai/dsh-client-ui-settings-shell`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-shell`

## 实现逻辑
shell 执行器设置页（浏览器半）。apply 绑定 settings.shell 字典，为 bash 与 pwsh 两个命名空间各建一个 ShellCardController，再在 whileServed 回调里按实际被服务的命名空间选择对应注入面，把 shell 页注册进 plugins.item（order 40），未被服务则页面上毫无痕迹 (src/client/index.ts:43-52)。两个控制器的 dispose 都在同一 effect 里回收 (src/client/index.ts:49)。页面在 summary 视图只渲染一行描述，否则渲染含 timeoutMs 与 maxOutputBytes 两个数值字段的 SettingsForm，字段 overridden/invalid/reset 文案全走字典 (src/client/ShellCard.tsx:20-45)。Host 半是空 apply，命名空间由 shell 执行器注册，本包不注册任何命名空间 (src/index.ts:10)。

## Provides

## Depends On (上游依赖)
- `dsh-client-locale` [E1+E2] - 注册 settings.shell 字典并按命名空间绑定翻译
  - 证据: `src/client/index.ts:10 import type {} from '@deepseek-ai/dsh-client-locale/client' + src/client/index.ts:44-45 ctx.locale.bind(NS) / ctx.locale.register(NS, { zh, en })`
- `dsh-client-ui-plugin-manager` [E1+E2] - 页面必须注册进 Plugins 页声明的 plugins.item 槽
  - 证据: `src/client/ShellCard.tsx:3 import type {} from '@deepseek-ai/dsh-client-ui-plugin-manager/client' + src/client/index.ts:50 ctx.slots.inject('plugins.item', ...)`
- `dsh-client-ui-primitives` [编译依赖] - 设置页复用共享表单与字段控件，字典类型也取自其 labels 契约
  - 证据: `src/client/ShellCard.tsx:4 import SettingsForm/SettingsValueField + src/client/locales.ts:3 import SettingsFormLabels + package.json:53 devDependencies`
- `dsh-client-ui-renderer` [编译依赖] - 拉入 SlotRegistry 服务合并，使槽注册与 slots.inject 在此编译单元可用
  - 证据: `src/client/index.ts:16 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-settings` [E1+E2] - 读 bash/pwsh 两个命名空间的共享配置表单，并以 whileServed 选择生效的那一个
  - 证据: `src/client/index.ts:13 import type {} from '@deepseek-ai/dsh-client-ui-settings/client' + src/client/index.ts:47-48 ctx.configForms.get(BASH_NS) / ctx.configForms.get(PWSH_NS)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
