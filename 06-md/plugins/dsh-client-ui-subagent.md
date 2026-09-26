# dsh-client-ui-subagent

- 包名: `@deepseek-ai/dsh-client-ui-subagent`
- 分组: G06 客户端 UI 包
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-subagent`

## 实现逻辑
子代理目录、导航与只读 composer 宿主：selectReadOnlySubagent 依据会话 subagent.address.mode 与 parentAvailable 判定是否接管 composer（src/client/index.ts:37-49），apply 经 ctx.slots.inject 向 conversation.session.header.lineage、conversation.session.header.actions、conversation.composer 三处注册组件并注入打开子会话/侧栏动作（src/client/index.ts:74-103）。sidebar-chat 子模块注册 'subagentchat' 资源协议、右侧栏标签类型、sidebar.chat.conversation 槽，并用 SessionProvider 绑定子会话渲染内嵌对话（src/client/sidebar-chat/index.tsx:176-201）。

## Provides
- slot conversation.session.header.lineage / conversation.session.header.actions 的子代理谱系与目录动作
- slot conversation.composer 的只读子代理 composer 接管
- 资源协议 'subagentchat'（ResourceProvider）与 sidebarRightTabs kind 'subagentchat' 标签类型
- slot sidebar.right.pane.tab key '@deepseek-ai/dsh-client-ui-subagent' 与子槽 sidebar.chat.conversation

## Depends On (上游依赖)
- `dsh-client-locale` [E1+E2] - 注册 subagent 字典
  - 证据: `src/client/index.ts:11 + src/client/index.ts:56 ctx.locale.register`
- `dsh-client-resources` [E1+E2] - 注册 subagentchat 资源提供者
  - 证据: `src/client/sidebar-chat/index.tsx:6 import type + src/client/sidebar-chat/index.tsx:178 ctx.resources.register`
- `dsh-client-ui-chat` [编译依赖] - 引入 ChatConversationViewNode 等聊天节点类型
  - 证据: `src/client/index.ts:12 import type`
- `dsh-client-ui-conversation` [E1+E2] - 复用 ComposerChainProps/ConversationViewsProps 与内嵌 conversation slot
  - 证据: `src/client/index.ts:5 import + src/client/sidebar-chat/index.tsx:7 ConversationViewsProps`
- `dsh-client-ui-primitives` [编译依赖] - 复用图标、Tooltip、StateDot 等原语
  - 证据: `src/client/SubagentHeaderLineage.tsx:12`
- `dsh-client-ui-renderer` [编译依赖] - 拉入渲染/槽服务类型合并
  - 证据: `src/client/index.ts:13 import type`
- `dsh-client-ui-session` [编译依赖] - 拉入会话 UI 服务类型合并
  - 证据: `src/client/index.ts:14 import type`
- `dsh-client-ui-sidebar-right` [E1+E2] - 打开子代理侧栏资源并注册 subagentchat 标签类型
  - 证据: `src/client/index.ts:15 + src/client/sidebar-chat/index.tsx:181 sidebarRightTabs.register`
- `dsh-client-ui-workspace` [E1+E2] - 把子代理会话打开为主视图导航
  - 证据: `src/client/index.ts:16 import type + src/client/index.ts:62 ctx.uiWorkspace.openSession`
- `dsh-session` [编译依赖] - 会话标识类型
  - 证据: `src/client/index.ts:4 SessionId`
- `dsh-subagent` [编译依赖] - 子代理地址/模式类型
  - 证据: `src/client/index.ts:3 SubagentAddress`
- `dsh-token-meter` [编译依赖] - 引入 token-meter 客户端类型合并（谱系行展示计量）
  - 证据: `src/client/SubagentHeaderLineage.tsx:15 import type`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
