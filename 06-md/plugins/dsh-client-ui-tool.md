# dsh-client-ui-tool

- 包名: `@deepseek-ai/dsh-client-ui-tool`
- 分组: G27 会话交互UI
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-tool`

## 实现逻辑
工具调用树 + 业务 Tool 视图。apply() 注册：conversation.chat.node keyed 'tool-call'（ToolCallTree，含 child slot tool.call.toolview keyed dispatch）、conversation.details.tool（ToolDetails 渲染选中调用输出）；再以 7 个独立 registrant plugin（bash/read/file-mutation/search/web/todo/ask-question toolviews）注册 keyed 'tool.call.toolview' 原子视图，未覆盖的 toolName 由 GenericToolCard fallback。declares slot 'tool.call.toolview'（keyed，open key 域，toolName 即 key）。

## Provides
- slot 声明: tool.call.toolview(keyed)
- conversation.chat.node keyed 'tool-call' 渲染器(ToolCallTree)
- conversation.details.tool 渲染器(ToolDetails)
- 7 个内置原子 toolview: read/search/web/todo/file-mutation/bash-sample/ask-question

## Depends On (上游依赖)
- `dsh-api-remotes` [编译依赖] - remote 类型底座
  - 证据: `package.json:52 peerDependencies`
- `dsh-client-locale` [编译依赖] - locale 命名空间（复用 conversation 命名空间文案）
  - 证据: `package.json:53 peerDependencies + locale.ts`
- `dsh-client-runtime` [编译依赖] - 会话快照/ToolCallBlock 类型与运行时
  - 证据: `apply.ts:2 ClientContext + ToolCallTree.tsx:3 ToolCallBlock`
- `dsh-client-ui-conversation` [编译依赖] - 消费 conversation.chat.node/details.tool 座位声明与 ChatNodeDataMap 'tool-call' 数据契约
  - 证据: `apply.ts:3 type-only import + package.json:55 peerDependencies + package.json:37 dsh.client.inject`
- `dsh-client-ui-primitives` [编译依赖] - 图标/组件 atoms
  - 证据: `toolviews/read-row.tsx:11 IconBrowseOutline16 等`
- `dsh-client-ui-slots` [编译依赖] - slot 注册 API 与四份 props 类型
  - 证据: `contract/slots.ts:2 PropsLocale/PropsRenderSlots/PropsRuntime + 各 toolview 注册用 ctx.slots.inject`

## Dependents (下游被依赖)
- `dsh-client-ui-cordis` - 消费 tool.call.toolview 座位注册业务 Tool 卡片
- `dsh-client-ui-skill` - keyed 工具行槽声明
