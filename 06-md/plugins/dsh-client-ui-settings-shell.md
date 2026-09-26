# dsh-client-ui-settings-shell

- 包名: `@deepseek-ai/dsh-client-ui-settings-shell`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-settings-shell`

## 实现逻辑
浏览器半在 Host 服务 bash 或 pwsh 命名空间时，把 shell 设置卡片注册进 Plugins 页的 `plugins.item`（id='shell' order 10，src/client/index.ts:50-52）。它按实际服务的命名空间选择控制器（`served.has(PWSH_NS) ? pwsh : bash`，src/client/index.ts:51），两个 ShellCardController 各自绑定 `bash`/`pwsh` 命名空间的 staged form 并在 effect 中 dispose（src/client/index.ts:47-49）。node half 为空 apply（src/index.ts:10）。

## Provides
- settings.shell locale 命名空间字典
- plugins.item 槽位条目 id='shell' (order 10)：shell 执行器命令超时与单流输出上限设置卡片（按平台绑定 bash 或 pwsh 命名空间）

## Depends On (上游依赖)
- `dsh-client-locale` [E1+E2] - 注册并绑定本页文案
  - 证据: `src/client/index.ts:10 type-only import + src/client/index.ts:44 ctx.locale.bind(NS)`
- `dsh-client-ui-plugin-manager` [E1+E2] - Plugins 页拥有 plugins.item 槽位
  - 证据: `src/client/index.ts:15 type-only import + src/client/index.ts:50-51 向 plugins.item 注册`
- `dsh-client-ui-primitives` [编译依赖] - 复用共享设置表单原语
  - 证据: `src/client/ShellCard.tsx:4 import + src/client/locales.ts:3 import`
- `dsh-client-ui-renderer` [编译依赖] - 引入 ctx.slots 合并
  - 证据: `src/client/index.ts:16 type-only import`
- `dsh-client-ui-settings` [E1+E2] - 经 configForms 取得 shell 命名空间的表单 scope
  - 证据: `src/client/index.ts:13 type-only import + src/client/index.ts:47 ctx.configForms.get(BASH_NS)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
