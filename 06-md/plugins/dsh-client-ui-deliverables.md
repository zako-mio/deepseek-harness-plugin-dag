# dsh-client-ui-deliverables

- 包名: `@deepseek-ai/dsh-client-ui-deliverables`
- 分组: G27 会话交互UI
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-deliverables`

## 实现逻辑
turn tail 产物行。deliverablesDefinition（kind 'deliverables'，match tool/result 且 callView 为 diff/edit 的 mutation locations，累积 Turn 内 produced 路径）注册进 ConversationEventRegistry；ProducedFiles 以 selector selectProducedFiles（关闭 turn 有产物才认领）注册进 conversation.chat.turnTail 链，inject 经 connection 提供 isLoopback/hostDescription；另 provide('chatFileMentions') 服务，让 ChatView 的闭合散文渲染 produced 文件内联提及（MarkdownFileMentions）。

## Provides
- conversation.chat.turnTail 链条目(ProducedFiles)
- ConversationNodeDefinition 'deliverables'（Turn 内产物累积，无 view node）
- ctx 服务 chatFileMentions（forClosing）
- ConversationTurnDataMap 'deliverables' 合并

## Depends On (上游依赖)
- `dsh-client-connection` [运行时依赖] - 连接回环/主机描述（产物链接是本地路径则 open）
  - 证据: `index.ts:10 ConnectionHandle + index.ts:38 ctx.get('connection') + index.ts:48-49 isLoopback/hostDescription`
- `dsh-client-locale` [编译依赖] - deliverables 命名空间字典
  - 证据: `index.ts:13 type-only + index.ts:40 locale.register`
- `dsh-client-runtime` [编译依赖] - EventDefinition 注册表与事件匹配
  - 证据: `turn-deliverables.ts:6-9 ConversationNodeDefinition,isAppendSurfaceEvent`
- `dsh-client-ui-conversation` [编译依赖] - 消费 turnTail 链座位与 TurnTailOwnerProps 载体（turn.data 读 deliverables）
  - 证据: `index.ts:12 ChatFileMentions 类型 + turn-deliverables.ts:11 TurnTailOwnerProps + package.json:12 dsh.client.inject`
- `dsh-client-ui-primitives` [编译依赖] - 产物内联提及类型
  - 证据: `turn-deliverables.ts:10 MarkdownFileMentions 类型`
- `dsh-client-ui-slots` [编译依赖] - slot 注册与 props 类型
  - 证据: `ProducedFiles.tsx:9 InjectFace/PropsLocale + index.ts:20-25 LocaleNamespaceMap merge`
- `dsh-tools` [编译依赖] - 产物来源为 mutation tools 的 callView.locations（运行时契约）
  - 证据: `cordis.patch.yml:213-216 ui-deliverables 行（装配）`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
