# dsh-client-ui-model-selection

- 包名: `@deepseek-ai/dsh-client-ui-model-selection`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 16
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-model-selection`

## 实现逻辑
先 ctx.plugin(ModelDirectoryResolver) 挂上 ctx.modelDirectories（src/client/index.ts:138），该服务用 WeakMap-with-values 为每个 Session 惰性建一个 ModelDirectory，并订阅 connection/reset 与 llm/adapters-updated 等事件刷新进程级目录（src/client/service.ts:46-73）。apply 再用同一目录注册两个入口：/model 的 commandUi popupSelect 装饰（src/client/index.ts:145）与 composer 的 conversation.input.model 座位（src/client/index.ts:182）。popup 选项由 optionsOf 拍平目录（失败组列出但不可选，src/client/index.ts:75-101），选择经 selectionOf 反解并按 session/selectModel 提交（src/client/index.ts:116-131）。

## Provides
- ctx.modelDirectories (ModelDirectoryResolver：每 Session 共享的模型目录解析服务)
- commandUi 的 /model popupSelect 装饰（列出 provider/model 行、当前项高亮、失败组只读）
- conversation.input.model 座位（composer 侧栏同名模型选择菜单，与 popup 共用同一 Session 目录状态）

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 读模型目录 Remote 与转发事件
  - 证据: `src/client/catalog.ts:4 import + src/client/service.ts:53 ctx.remote.$on`
- `dsh-api-session-controller` [E1+E2] - Session 绑定/投影与 session Remote 控制器面
  - 证据: `src/client/index.ts:14-15 import + src/client/service.ts:17-18 import`
- `dsh-client-locale` [运行时依赖] - 注册 model 文案命名空间
  - 证据: `src/client/index.ts:21 import type + src/client/index.ts:132 ctx.locale.register(NS)`
- `dsh-client-ui-commands` [运行时依赖] - 注册 /model 命令的 popupSelect 交互
  - 证据: `src/client/index.ts:17 import type + src/client/index.ts:145 command.register`
- `dsh-client-ui-conversation` [运行时依赖] - 使用 ui-conversation 声明的 input.model 座位
  - 证据: `src/client/index.ts:19 import type + src/client/index.ts:182 scope.slots.inject('conversation.input.model')`
- `dsh-client-ui-primitives` [编译依赖] - 复用图标与 MenuSurface 控件
  - 证据: `src/client/index.ts:25 import { IconDataOutlineRegular } + src/client/ModelSelect.tsx:22`
- `dsh-client-ui-renderer` [E1+E2] - ctx.slots 槽注册表
  - 证据: `src/client/index.ts:22 import type + src/client/index.ts:123 inject 'slots'`
- `dsh-client-ui-session` [编译依赖] - Session 标准来源类型面
  - 证据: `src/client/index.ts:23 import type {}`
- `dsh-session` [编译依赖] - 会话身份类型
  - 证据: `src/client/service.ts:18 import type { SessionId }`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
