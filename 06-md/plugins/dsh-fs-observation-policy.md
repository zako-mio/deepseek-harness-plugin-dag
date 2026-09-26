# dsh-fs-observation-policy

- 包名: `@deepseek-ai/dsh-fs-observation-policy`
- 分组: G16 文件系统
- 拓扑层: Layer 0
- 来源层: L1 核心集
- 源码路径: `packages/fs/fs-observation-policy`

## 实现逻辑
事件专属的文件观察策略，不注册任何服务：ObservedStateGate 用 WeakMap(owner→targetKey→FsObservation) 记录每次权威的 present/absent 观察，区分「确认不存在」与「未见」 (src/index.ts:28-54, 91-94)。在 fs/write-intent 与 fs/edit-intent 两个单槽 waterfall 上据该状态派生 createIfAbsent/replaceIfVersion，或对未读/不存在抛 FS_NOT_OBSERVED/FS_NOT_FOUND (src/index.ts:65-88, 119-122)；fs/observed 上同步记录且保持同步非抛 (src/index.ts:127-129)。无此插件时工具退回 provider 的无条件变更行为。

## Provides

## Depends On (上游依赖)
- 无依赖（基础插件）

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
