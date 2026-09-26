# dsh-client-ui-commands

- 包名: `@deepseek-ai/dsh-client-ui-commands`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-commands`

## 实现逻辑
以 CommandUiRuntime(Service，注册为 ctx.commandUi) 提供 '/' 命令面：构造时经 ctx.get('inputTriggers').registerSource 注册 trigger '/' 的 source，并建 CommandDirectory 做 capability-keyed 目录缓存、PopupSelectController 做每会话弹层 (src/client/service.ts:76-130)。候选合成把 Host 目录与客户端 contribution 按可用性合并、按 rankByName 排序，host 与 contribution 重名时 fail loud (src/client/service.ts:1-14, 97-128)。apply 注册 command 字典、ctx.plugin(CommandUiRuntime)，再把 PopupSelectView 以 order 1 放进 'conversation.input.overlay'，注入面按 sessionId 经 sessions.scope 解出该会话 popup (src/client/index.ts:58-75)。

## Provides
- ctx.commandUi (CommandUiRuntime：'/' 命令 source、客户端命令贡献注册表、每会话 popupSelect 控制器)
- slot: conversation.input.overlay#command-popup (order 1 的命令弹层 PopupSelectView)
- Locale 命名空间 command
- 本地事件 command/executed(sessionId, name, result) 发射
- 上抛 CommandUiRuntime/CommandDirectory/PopupSelectController/filterOptions 与 CommandUiContract/CommandContribution 等类型

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 拉取 Host 命令目录并订阅变更
  - 证据: `src/client/service.ts:19 + src/client/service.ts:108 ctx.remote.commands.list + src/client/service.ts:129 connection/reset`
- `dsh-api-session-controller` [E1+E2] - 按会话解析 scope 与 using
  - 证据: `src/client/index.ts:9 ISessions + src/client/service.ts:98 this.sessions()`
- `dsh-client-locale` [E1+E2] - 注册命令字典
  - 证据: `src/client/index.ts:15 + src/client/index.ts:59 ctx.locale.register('command')`
- `dsh-client-ui-conversation` [运行时依赖] - 占据输入浮层槽位
  - 证据: `src/client/index.ts:13 SlotMap merge + src/client/index.ts:64 slots.inject('conversation.input.overlay')`
- `dsh-client-ui-input-trigger` [E1+E2] - 把 '/' 命令面注册成触发源
  - 证据: `src/client/contract.ts:8 + src/client/service.ts:113-115 ctx.get('inputTriggers').registerSource`
- `dsh-client-ui-primitives` [编译依赖] - 命令弹层组件与候选排序函数
  - 证据: `src/client/PopupSelectView.tsx:13 import + src/client/service.ts:26 rankByName`
- `dsh-client-ui-renderer` [编译依赖] - 引入 slots 服务声明
  - 证据: `src/client/index.ts:16 merge`
- `dsh-client-ui-session` [编译依赖] - 会话 UI 声明合并
  - 证据: `src/client/index.ts:17 merge`
- `dsh-commands` [编译依赖] - 命令目录与结果类型
  - 证据: `src/client/directory.ts:8-12 + src/client/service.ts:20 CommandResult`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/directory.ts:9 import SessionId`

## Dependents (下游被依赖)
- `dsh-client-ui-message-feedback` - 挂 /feedback 命令装饰
- `dsh-client-ui-model-selection` - 注册 /model 命令的 popupSelect 交互
- `dsh-client-ui-permission-presets` - 装饰 /permission 命令为 popup 选择器
- `dsh-session-log-export` - 订阅 /export 命令执行成功事件以启动浏览器下载
