# dsh-client-ui-input-trigger

- 包名: `@deepseek-ai/dsh-client-ui-input-trigger`
- 分组: G28 设置输入UI
- 拓扑层: Layer 12
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-input-trigger`

## 为什么需要它（设计初衷）
输入触发流水线：光标处 / 与 @ 检测、分组候选菜单、路由到已注册 source（如命令、引用插入），纯内核+React 壳分离。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/client/ui-input-trigger/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness

## 实现逻辑
'/' | '@' 输入管线核心：browser 半注册 InputTriggerService（ctx.inputTriggers）——source 注册表 + 每会话 controller 解析（service.ts:28-100，registerSource/sessionOf）。MenuView 自注册进 conversation.input.overlay 槽（slash-menu，order=0，按 sessionId 解析 controller）。inject ['sessions','locale']。契约在 contract.ts，source 仅经 ctx.inputTriggers.registerSource 接入。

## Provides
- ctx.inputTriggers (InputTriggerService)
- conversation.input.overlay 'slash-menu' 槽注册 (MenuView)
- InputTriggerSource / TriggerChar 类型契约 (types.ts / contract.ts)
- slash.menu 字典

## Depends On (上游依赖)
- `dsh-client-locale` [编译依赖] - 候选菜单本地化
  - 证据: `packages/client/ui-input-trigger/src/client/index.ts:57 (locale.register MENU_NS)`
- `dsh-client-runtime` [编译依赖] - client 运行时上下文与会话面
  - 证据: `packages/client/ui-input-trigger/src/client/index.ts:48 (inject sessions/locale), service.ts:10 (ClientContext/ISessions 类型)`
- `dsh-session` [运行时依赖] - 按会话 scope 解析 controller
  - 证据: `packages/client/ui-input-trigger/src/client/service.ts:29,80-82 (static inject ['sessions'] + sessions.scopeOf)`

## Dependents (下游被依赖)
- `dsh-client-ui-commands` - 作为 '/' 子类 source 注册并消费 claim/consume-token 契约
- `dsh-client-ui-conversation` - '/'|'@' 输入触发控制器与 slash 事件契约（bail 监听）
- `dsh-client-ui-cordis` - 注册 '@' cordis 引用源（@pluginId）
- `dsh-client-ui-skill` - 注册 '/' 引用源并消费 lexicon/subscribeLexicon 契约
- `dsh-client-ui-subagent` - 注册 '@' 引用源
