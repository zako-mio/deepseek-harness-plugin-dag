# dsh-client-ui-input-trigger

- 包名: `@deepseek-ai/dsh-client-ui-input-trigger`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 14
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-input-trigger`

## 实现逻辑
以 InputTriggerService(注册为 ctx.inputTriggers) 拥有 '/' 与 '@' 的触发检测、候选菜单与 pick 流水线 (src/client/index.ts:1-6, 59-61)。apply 用 ctx.inject(['slots','inputTriggers','sessions']) 后把 MenuView 以 order 0 注册进 'conversation.input.overlay'，注入面按 sessionId 经 sessions.scope 解出该会话 controller 的 menu/headers，并桥接 onPick/onCrumb/onHover/onDismiss 回调 (src/client/index.ts:62-86)。检测与菜单归约的纯函数契约在 src/core/contract.ts 与 src/types.ts，source 只能经 ctx.inputTriggers 注册 (src/client/index.ts:24-32)。宿主半为空 apply (src/index.ts:9)。

## Provides
- ctx.inputTriggers (InputTriggerService：触发检测、候选菜单、pick 流水线；source 注册唯一入口)
- slot: conversation.input.overlay#slash-menu (order 0 的候选菜单 MenuView)
- Locale 命名空间 slash.menu
- 上抛 InputTriggerService/InputTriggerController 与 InputTriggerSource/TriggerChar/MenuState/PickOutcome 等大量公开类型与契约

## Depends On (上游依赖)
- `dsh-api-session-controller` [运行时依赖] - 把槽 frame 的 sessionId 解析成会话作用域
  - 证据: `src/client/index.ts:10 merge + src/client/index.ts:73 sessions.scope(sessionId)`
- `dsh-client-locale` [运行时依赖] - 注册并观察菜单字典
  - 证据: `src/client/index.ts:8 merge + src/client/index.ts:61 ctx.locale.register('slash.menu')`
- `dsh-client-ui-conversation` [运行时依赖] - 依赖 Conversation 声明的输入浮层槽
  - 证据: `src/client/slots.ts:2 + src/core/contract.ts:7 (conversation.input.overlay 槽)`
- `dsh-client-ui-primitives` [编译依赖] - 候选菜单列表基础组件
  - 证据: `src/client/MenuView.tsx:15 import @deepseek-ai/dsh-client-ui-primitives`
- `dsh-client-ui-renderer` [编译依赖] - 引入 slots 服务声明
  - 证据: `src/client/index.ts:11 merge`
- `dsh-client-ui-session` [编译依赖] - 会话 UI 声明合并
  - 证据: `src/client/index.ts:12 merge`
- `dsh-session` [编译依赖] - 会话标识/上下文类型
  - 证据: `src/client/controller.ts:15 + src/types.ts:15`

## Dependents (下游被依赖)
- `dsh-client-ui-chat` - 技能引用经触发管线打开
- `dsh-client-ui-commands` - 把 '/' 命令面注册成触发源
- `dsh-client-ui-permission-presets` - 命令/座位回调的会话上下文类型
- `dsh-client-ui-reference` - 注册 '@' 触发源并消费其 Source/Crumb 契约
- `dsh-client-ui-skill` - 注册斜杠菜单的 skill 候选源
