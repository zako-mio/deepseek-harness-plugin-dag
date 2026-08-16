# dsh-session-reference

- 包名: `@deepseek-ai/dsh-session-reference`
- 分组: G34 Web上下文扩展
- 拓扑层: Layer 3
- 来源层: L3 其余
- 源码路径: `packages/context/session-reference`

## 实现逻辑
跨会话快照服务 ctx.sessionReferenceResolver（SessionReferenceResolver extends Service，static inject ['sessionQuery']）。主机把会话 mention 适配为结构化引用，本服务拥有精确读取/投影/预算/持久上下文。listCandidates()：按工作目录亲和度（candidateRank）排序引用候选，排除自身，支持 session-id/cwd/title 子串过滤，经 sessionQuery.readTitleSnapshots 补标签。prepare()：引用去重+排除目标自身+maxReferences 上限，并行 readSurface 读每个被引用会话的 surface 快照，renderSources 经 projection.ts 的 retainReferencedSession（TextRetainer 字节预算 maxReferenceBytes + isCompactCheckpointSource 识别压缩检查点）投影用户/助手对话（排除工具/推理/注入），渲染为带 PROMPT_PREFIX 的 '## Referenced sessions' untrusted 只读快照 JSON，封装为 source.kind='session-reference' 的 UserMessage 附加上下文。提供 encode/decodeSessionReferenceUri、formatSessionReferenceMention、parseSessionReferenceText（SESSION_REFERENCE_SCHEME）。

## Provides
- ctx.sessionReferenceResolver（SessionReferenceResolver 服务）
- listCandidates(): SessionReferenceCandidate[]（cwd 亲和排序）
- prepare(): PreparedReferencedMessage（detached content + additionalContext 引用快照）
- 会话引用 URI 编解码（encode/decodeSessionReferenceUri/formatMention/parseText）
- SESSION_REFERENCE_SCHEME/MAX_REFERENCES/DEFAULT_CANDIDATE_LIMIT/DEFAULT_MAX_REFERENCE_BYTES
- untrusted 只读 'Referenced sessions' prompt 前缀

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 目标 agent 身份与工作目录（cwd 亲和排序/排除自身）
  - 证据: `packages/context/session-reference/src/index.ts:10 Agent 类型（agent.session.header.cwd, agent.id）`
- `dsh-llm` [编译依赖] - 构造附加 UserMessage 载荷与事件类型穷尽
  - 证据: `packages/context/session-reference/src/index.ts:11 createUserMessage + ContentBlock/UserMessage 类型；projection.ts:5 assertNever`
- `dsh-session` [编译依赖] - SessionId branded 类型与 SessionHeader（cwd/createdAt）契约
  - 证据: `packages/context/session-reference/src/index.ts:13 SessionId 类型 + package.json:43 peerDependencies`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
