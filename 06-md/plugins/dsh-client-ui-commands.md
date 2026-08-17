# dsh-client-ui-commands

- 包名: `@deepseek-ai/dsh-client-ui-commands`
- 分组: G28 设置输入UI
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-commands`

## 为什么需要它（设计初衷）
Web 端斜杠命令体系：会话级命令目录缓存、/ 命令 source、execute/popupSelect/leadingInput 三类派发，让业务包可注册自定义命令。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/client/ui-commands/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness

## 实现逻辑
命令表面：CommandUiRuntime（ctx.commandUi）——capability 键控的全局目录缓存（CommandDirectory，commands.list RPC，service.ts:132-137）、'/' 命令 source（:140-148）、client 贡献注册表与 /host 命令装饰（register/decorate，:164-192）、每会话 popupSelect controller（popupFor，:202-224）。PopupSelectView 注册进 conversation.input.overlay（command-popup，order=1）。dispatch 决策表:菜单/空格/回车三列（:265-329）。

## Provides
- ctx.commandUi (CommandUiRuntime)
- '/' source 'command' (目录缓存 + 模糊匹配 + 三列决策)
- popupSelect 注册表 (contribution/decorate) 与 PopupSelectView
- conversation.input.overlay 'command-popup' 槽
- command 字典

## Depends On (上游依赖)
- `dsh-client-ui-conversation` [编译依赖] - overlay 槽声明 typecheck
  - 证据: `packages/client/ui-commands/src/client/index.ts:12 (type-only import conversation.input.overlay 声明)`
- `dsh-client-ui-input-trigger` [运行时依赖] - 作为 '/' 子类 source 注册并消费 claim/consume-token 契约
  - 证据: `packages/client/ui-commands/src/client/index.ts:48 (inject inputTriggers), service.ts:138-148 (ctx.get('inputTriggers') + registerSource + matchSpace/matchEnter)`
- `dsh-commands` [运行时依赖] - Host 命令目录与执行 wire
  - 证据: `packages/client/ui-commands/src/client/service.ts:134-136 (ctx.remote.commands.list), :149 (commands/change 失效), package.json:60 (peerDep)`
- `dsh-session` [运行时依赖] - 每会话 popup controller 与目录键
  - 证据: `packages/client/ui-commands/src/client/service.ts:121,203 (static inject sessions + sessions.scopeOf)`

## Dependents (下游被依赖)
- `dsh-client-ui-model-selection` - popupSelect 贡献注册
- `dsh-client-ui-permission-presets` - popupSelect 装饰注册
