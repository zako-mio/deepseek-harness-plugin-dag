# dsh-workspace-changes

- 包名: `@deepseek-ai/dsh-workspace-changes`
- 分组: G11 交付物
- 拓扑层: Layer 0
- 来源层: L2 web-app
- 源码路径: `packages/deliverables/workspace-changes`

## 实现逻辑
汇总每个顶层 turn 改动的文件：以 git 工作树快照（turn 起止）为主，叠加文件工具编辑的整文件捕获，非 git 环境退化为仅文件工具编辑（src/index.ts:1-10、120-129）。`apply()` 通过 `session/event`、`agent/turn-stopping`、`tools/pre-execute` 驱动每 Session 的 `TurnRecorder`（src/index.ts:143-164），并把 `workspaceChanges` 服务 provide 到 ctx，按 SessionId+seq 提供 `summary()` 与按需计算的 `diff()`（src/index.ts:114-118、src/types.ts:78-97）。变更摘要由 `workspace/changes` Session 事件宣告，摘要本体留在 Host 侧（src/types.ts:99-108）。

## Provides
- ctx.workspaceChanges (按 Session/seq 提供每 turn 变更摘要与文件前后对比)
- Session 事件 workspace/changes

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 在 turn 停止时收口快照
  - 证据: `src/index.ts:14 import type {} from '@deepseek-ai/dsh-agent' + src/index.ts:153 agent/turn-stopping`
- `dsh-session` [编译依赖] - 按 Session 生命周期观察事件与释放记录器
  - 证据: `src/index.ts:15 import type { Session, SessionId } + src/recorder.ts:5 import + src/index.ts:143 session/event`
- `dsh-tools` [编译依赖] - 在工具执行前捕获文件编辑以覆盖 git 未跟踪路径
  - 证据: `src/index.ts:17 import type {} from '@deepseek-ai/dsh-tools' + src/index.ts:156 tools/pre-execute`

## Dependents (下游被依赖)
- `dsh-client-ui-deliverables` - 工作区变更记录/差异类型
