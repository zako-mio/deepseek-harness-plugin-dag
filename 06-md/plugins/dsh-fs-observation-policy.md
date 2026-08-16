# dsh-fs-observation-policy

- 包名: `@deepseek-ai/dsh-fs-observation-policy`
- 分组: G13 文件系统
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/fs/fs-observation-policy`

## 实现逻辑
纯事件型文件观察策略(不注册任何服务):apply() 建立 ObservedStateGate,以 WeakMap<owner(session), Map<targetKey, FsObservation>> 记录观察;通过 ctx.on 订阅三个 fs/* 事件——fs/write-intent 决策、fs/edit-intent 决策、fs/observed 记录。无此插件时工具退化为无条件变更。

## Provides
- fs/write-intent、fs/edit-intent 瀑布单槽决策监听
- fs/observed 监听(会话级观察状态)
- FS_NOT_OBSERVED/FS_NOT_FOUND 守卫语义

## Depends On (上游依赖)
- `dsh-session` [运行时依赖] - owner 从 actor.agent.session 派生
  - 证据: `packages/fs/fs-observation-policy/src/index.ts:40`

## Dependents (下游被依赖)
- `dsh-tool-fs` - fs/* 事件槽的监听方
- `dsh-tool-str-replace-editor` - 写/编辑前守卫与观察记录
