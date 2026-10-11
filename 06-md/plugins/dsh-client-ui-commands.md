# dsh-client-ui-commands

- 包名: `@deepseek-ai/dsh-client-ui-commands`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-commands`

## 实现逻辑
浏览器半以 CommandUiRuntime（ctx.commandUi）持有按能力键的斜杠命令目录缓存、客户端贡献注册表与每会话 popupSelect 控制器（src/client/service.ts:93、src/client/index.ts:60-62）。它把 popupSelect 外壳注册进 conversation.input.overlay，并按会话作用域解析出对应 popup（src/client/index.ts:61-75）；Remote 命令目录在 connection/reset 时失效重取（src/client/service.ts:129）。

## Provides
- ctx.commandUi (斜杠命令目录缓存、客户端贡献注册表与 popupSelect 控制器)

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 拉取命令目录并执行命令
  - 证据: `src/client/service.ts:19 import + src/client/service.ts:108 ctx.remote`
- `dsh-api-session-controller` [E1+E2] - 按会话作用域解析 popup 控制器
  - 证据: `src/client/index.ts:9 import type + src/client/index.ts:70 sessions.scope(sessionId)`
- `dsh-client-locale` [E1+E2] - 注册 command 字典
  - 证据: `src/client/index.ts:15 import type + src/client/index.ts:59 ctx.locale.register(NS)`
- `dsh-client-ui-conversation` [E1+E2] - 占用输入覆盖层槽位渲染 popup
  - 证据: `src/client/index.ts:13 import type + src/client/index.ts:64 slots.inject('conversation.input.overlay')`
- `dsh-client-ui-input-trigger` [编译依赖] - 与输入触发器的会话上下文类型对接
  - 证据: `src/client/contract.ts:8 import + src/client/popup.ts:14 import`
- `dsh-client-ui-primitives` [编译依赖] - 复用弹出层与列表基础控件
  - 证据: `src/client/PopupSelectView.tsx:13 import + src/client/contract.ts:9 import`
- `dsh-client-ui-renderer` [编译依赖] - 渲染器槽位服务类型
  - 证据: `src/client/index.ts:16 import type`
- `dsh-client-ui-session` [编译依赖] - 会话标准 seat 类型
  - 证据: `src/client/index.ts:17 import type`
- `dsh-commands` [编译依赖] - 命令描述与执行结果类型
  - 证据: `src/client/directory.ts:8 import + src/client/service.ts:20 import`
- `dsh-session` [编译依赖] - 会话标识与事件类型
  - 证据: `src/client/directory.ts:9 import + src/client/service.ts:23 import`

## Dependents (下游被依赖)
- `dsh-client-ui-message-feedback` - 挂 /feedback 命令装饰
- `dsh-client-ui-model-selection` - 注册 /model 的 popupSelect 贡献
- `dsh-client-ui-permission-presets` - 装饰 /permission 的 popupSelect 界面
- `dsh-session-log-export` - 订阅 /export 命令执行成功事件以启动浏览器下载
