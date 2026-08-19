# dsh-fs-observation-policy

- 包名: `@deepseek-ai/dsh-fs-observation-policy`
- 分组: G13 文件系统
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/fs/fs-observation-policy`

## 为什么需要它（设计初衷）
文件系统策略层第三块：在 ctx.fs provider 契约之上通过 fs/* 事件门（而非方法服务）增加'observed-state（先观察）→ read-before-edit（先读后改）→ version-guarded（版本守卫的写/改）'策略。它让模型必须先读文件才能改，杜绝盲写导致的版本丢失，是'以 fs/* 事件门替代强制方法服务'设计的示范实现。

发展史：源自 2026-06-26 fsspec-style fs-seam 简化决策，把策略从 FileSystem provider 基类拆出，形成 tool-fs/fs-observation-policy/fs/fs-local 四层栈。无服务 API，仅注册三个 fs/* 监听器，可优雅地加减装。观察状态不跨会话持久化为已知限制。版本 0.1.0-rc.8。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/fs/fs-observation-policy/README.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/fs/fs-observation-policy/package.json

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
