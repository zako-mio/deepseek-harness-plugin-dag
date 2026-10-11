# dsh-client-ui-settings-plugin-inventory

- 包名: `@deepseek-ai/dsh-client-ui-settings-plugin-inventory`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-plugin-inventory`

## 实现逻辑
只读的 Host 插件清单设置页。apply 注册 settings.pluginInventory 字典，把 remote.pluginInventory.list() 的结果（!ok 即抛带错误码的异常）暴露为注入面的 list (src/client/index.ts:34-43)；预设显示名按当前 locale 经 ui-agent-preset 的字典逐次解析，用户自定义元数据原样透传 (src/client/index.ts:46-48)；客户端模块图同步状态与重试直接取自 ctx.modules.entries (src/client/index.ts:52-53)。页面注册进 settings.plugins.tab 的 'all' 标签（order 10）(src/client/index.ts:56-63)；组件以本地 ViewState 三态渲染加载/错误/就绪，并把 fiber 相位映射为字典键 (src/client/PluginInventorySettingsTab.tsx:48-59)。Host 半是空 apply，只为让 Loader 能寻址本包 (src/index.ts:4)。

## Provides

## Depends On (上游依赖)
- `dsh-agent-preset-registry` [编译依赖] - 预置显示名解析复用 registry 的 display 折叠，避免在本包另建一份映射
  - 证据: `src/client/index.ts:12 import { presetDisplayText } from '@deepseek-ai/dsh-agent-preset-registry/display' + package.json:63 devDependencies`
- `dsh-api-remotes` [E1+E2] - Host 清单快照只经 Remote 的 pluginInventory 命名空间读取
  - 证据: `src/client/PluginInventorySettingsTab.tsx:4 import PluginInventorySnapshot + src/client/index.ts:38 ctx.remote.pluginInventory.list()`
- `dsh-client-locale` [E1+E2] - 注册清单页字典并绑定翻译；另借 locale 逐次解析预设名
  - 证据: `src/client/index.ts:3 import type {} from '@deepseek-ai/dsh-client-locale/client' + src/client/index.ts:34-36 ctx.locale.register(NS, { zh, en }) / ctx.locale.bind(NS)`
- `dsh-client-modules` [E1+E2] - 清单页需读客户端模块图条目状态并可触发重试
  - 证据: `src/client/PluginInventorySettingsTab.tsx:2 import ClientEntryState + src/client/index.ts:52-53 ctx.modules.entries.state / ctx.modules.entries.retry()`
- `dsh-client-ui-agent-preset` [编译依赖] - 拉入 settings.agentPreset 字典命名空间合并，使预置名可经该字典解析
  - 证据: `src/client/index.ts:10 import type {} from '@deepseek-ai/dsh-client-ui-agent-preset/client'`
- `dsh-client-ui-primitives` [编译依赖] - 清单表复用共享的菜单、状态点与标签控件
  - 证据: `src/client/PluginInventorySettingsTab.tsx:13 import Menu/StateDot/Tag/IconChevronDownOutlineRegular + package.json:53 devDependencies`
- `dsh-client-ui-renderer` [编译依赖] - 拉入 SlotRegistry 服务合并，使槽注册在此编译单元可用
  - 证据: `src/client/index.ts:7 import type {} from '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-settings` [编译依赖] - 拉入 settings.plugins.tab 槽声明的类型合并（本包不注入 configForms）
  - 证据: `src/client/index.ts:6 import type {} from '@deepseek-ai/dsh-client-ui-settings/client' + package.json:54 devDependencies`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
