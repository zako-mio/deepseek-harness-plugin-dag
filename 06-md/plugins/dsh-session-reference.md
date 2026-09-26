# dsh-session-reference

- 包名: `@deepseek-ai/dsh-session-reference`
- 分组: G08 上下文注入
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/context/session-reference`

## 实现逻辑
跨会话引用解析服务 SessionReferenceResolver（ctx.sessionReferenceResolver）：把宿主解析出的结构化会话引用读取为当前表面快照，经订阅 system-prompt/assemble 记录的最近路由计算模型相对字节预算，再把投影出的对话按字节上限保留/截断并渲染为不可信只读上下文（src/index.ts:127-142、src/index.ts:299-358、src/projection.ts:73-146）。在 agent/pre-step 前置监听中把直接用户消息里的规范 @[label](dsh-session:…) 提及替换为可读 @label，并在其后插入聚合的引用快照消息（src/index.ts:135-177、src/uri.ts:48-87）。被截断的预览会把完整转录喂给可选 spillStore，并附一条省略说明（src/spill.ts:23-50）。

## Provides
- ctx.sessionReferenceResolver (跨会话引用解析服务：读取他会话快照并按字节预算渲染为可信度受限的持久上下文)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 在 agent 步前把会话引用上下文拼入直接用户消息之后
  - 证据: `src/index.ts:10 import type Agent/PreStepDecision + src/index.ts:135 ctx.on('agent/pre-step')`
- `dsh-llm` [编译依赖] - 构造引用上下文 user 消息、冻结直接消息，并识别 NO_ADAPTER 以回退默认字节预算
  - 证据: `src/index.ts:12 import createUserMessage/freezeMessage/LlmError + src/index.ts:13 import type ContentBlock/LlmResolvedModelInfo/UserMessage + src/types.ts:8-9 子路径类型 import`
- `dsh-session` [编译依赖] - 使用会话 id / 序列号等不透明标识类型区分源会话与捕获位置
  - 证据: `src/index.ts:14 import type SessionId + src/projection.ts:7-8 import SessionSeq/类型 + src/spill.ts:3 import type SessionId + src/types.ts:10 + src/uri.ts:4`
- `dsh-session-projection` [E1+E2] - 从 title/subagent 投影快照派生候选的提及标签与显示标题，避免折叠整个日志
  - 证据: `src/index.ts:17 import type ProjectionSnapshot + src/index.ts:248 this.ctx.get('sessionProjections') + src/index.ts:250 projections.snapshot(attached, ['title','subagent'])`
- `dsh-session-projection-cache` [E1+E2] - 对冷会话从持久投影缓存回答标题，无需打开其日志
  - 证据: `src/index.ts:18 type-only import + src/index.ts:251 this.ctx.get('sessionProjectionCache')?.cachedSnapshot`
- `dsh-session-title` [编译依赖] - 引入 title 投影键的类型合并以读取会话标题作为提及标签
  - 证据: `src/index.ts:19 type-only import (title projection key merge)`
- `dsh-subagent` [编译依赖] - 引入 subagent 投影值的类型以优先使用子代理创建标签作为显示标题
  - 证据: `src/index.ts:20 type-only import (subagent label projection)`
- `dsh-system-prompt` [E1+E2] - 在系统提示装配完成后捕获 provider/model 变量作为引用字节预算的模型来源
  - 证据: `src/index.ts:21 type-only import + src/index.ts:127 ctx.on('system-prompt/assemble', {prepend:true})`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配会话引用命名空间
- `dsh-client-ui-reference` - 会话引用候选类型
