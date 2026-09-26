# dsh-client-ui-tool

- 包名: `@deepseek-ai/dsh-client-ui-tool`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 10
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-tool`

## 实现逻辑
注册整棵工具调用树与内建原子 toolview：apply 向 'conversation.chat.node' 注册 key='tool-call' 的 ToolCallTree，并声明子槽 'tool.call.toolview' 与参数前缀 hook（src/client/apply.ts:35-46）；随后用 ctx.plugin 挂载 bash/read/read-image/file-mutation/search/web/todo/details/ask-question 九个 toolview 模块（src/client/apply.ts:48-56）。各 toolview 模块各自通过 slots.inject/register 注册按工具名分发的 keyed 视图，模型层从原始 call/result 事件派生卡片。

## Provides
- slot conversation.chat.node key='tool-call' 的工具调用树渲染
- slot tool.call.toolview 的按工具名 keyed 视图（bash/read/read-image/file-mutation/search/web/todo/details/ask-question 等）
- 子槽 tool.call.images 声明与 hooks.toolCallArgumentsPartial（准备阶段参数前缀订阅）

## Depends On (上游依赖)
- `dsh-api-remotes` [E1+E2] - 提供 Host home 事实用于 POSIX ~ 显示
  - 证据: `src/client/apply.ts:3 import + src/client/apply.ts:31 ctx.remote.$host`
- `dsh-client-locale` [编译依赖] - 引入本地化命名空间类型
  - 证据: `src/client/contract/slots.ts:11 import type`
- `dsh-client-ui-chat` [编译依赖] - 复用 AssistantChatData/ToolResultNode 等工具视图数据契约
  - 证据: `src/client/contract/slots.ts:9 import type`
- `dsh-client-ui-conversation` [编译依赖] - 引入 MessageImageLoader/OpenFileOptions 与 conversation 节点类型
  - 证据: `src/client/apply.ts:6 import + src/client/apply.ts:10`
- `dsh-client-ui-primitives` [编译依赖] - 复用对话卡片原语与标签
  - 证据: `src/client/tool/models/tool-call-model.ts:12 + src/client/tool/toolviews/todo-row.tsx:2`
- `dsh-client-ui-renderer` [编译依赖] - 拉入槽/渲染服务类型合并
  - 证据: `src/client/apply.ts:7 import type`
- `dsh-client-ui-session` [编译依赖] - 拉入会话 UI 服务类型合并
  - 证据: `src/client/apply.ts:8 import type`
- `dsh-spill-policy` [编译依赖] - 渲染输出溢出/截断提示 notice
  - 证据: `src/client/tool/models/inspection-details-model.ts:3 + terminal-card-model.ts:5`
- `dsh-tools` [编译依赖] - 复用工具类型（todo 历史）
  - 证据: `src/client/tool/models/todo-history.ts:2 import type`

## Dependents (下游被依赖)
- `dsh-client-ui-attachment` - 占据工具调用图片槽
- `dsh-client-ui-cordis` - 为 cordis_* 工具调用提供 tool view 卡片渲染
- `dsh-client-ui-deliverables` - present 工具行视图
- `dsh-client-ui-schedule` - 复用工具视图类型/卡片
- `dsh-client-ui-skill` - 复用 tool.call.toolview 的 props 类型契约
