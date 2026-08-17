# dsh-client-ui-subagent

- 包名: `@deepseek-ai/dsh-client-ui-subagent`
- 分组: G28 设置输入UI
- 拓扑层: Layer 15
- 来源层: L2 web-app
- 源码路径: `packages/client/ui-subagent`

## 为什么需要它（设计初衷）
子 Agent 会话目录、续跑路由 UI 与 '@' 引用来源，管理多 Agent 会话的浏览与接线。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/client/ui-subagent/package.json

## 实现逻辑
子代理引用源：注册 '@' source name=subagent（index.ts:70-95,97），候选从 sessions.list 快照过滤 running 子会话（零 RPC，:61-69），pick 落字面 @label。另注册 conversation.session.header.actions 的 subagent-catalog 按钮（:110-119）与 conversation.composer 的 SubagentReadOnlyComposer（priority=-10，one-shot/parent-offline 接管，:120-128,44-53）。

## Provides
- '@' source 'subagent' (InputTriggerSource + codec)
- conversation.session.header.actions 'subagent-catalog' 槽
- conversation.composer 'SubagentReadOnlyComposer' (select 接管)
- subagent 字典

## Depends On (上游依赖)
- `dsh-client-ui-conversation` [编译依赖] - 会话头与 composer 槽声明
  - 证据: `packages/client/ui-subagent/src/client/index.ts:17,110-127 (ComposerChainProps 类型 + header.actions/composer 槽)`
- `dsh-client-ui-input-trigger` [编译依赖] - 注册 '@' 引用源
  - 证据: `packages/client/ui-subagent/src/client/index.ts:18,41,97 (类型 import + inject + registerSource)`
- `dsh-session` [运行时依赖] - 子会话候选源与导航动作
  - 证据: `packages/client/ui-subagent/src/client/index.ts:61-69,100-108 (sessions.list / openSubagent / refreshSubagents / setSubagentCatalogOpen)`
- `dsh-subagent` [编译依赖] - SubagentAddress 与子代理语义类型
  - 证据: `packages/client/ui-subagent/package.json:60 (peerDep dsh-subagent)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
