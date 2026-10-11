# dsh-workspace-changes

- 包名: `@deepseek-ai/dsh-workspace-changes`
- 分组: G11 交付物
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/deliverables/workspace-changes`

## 实现逻辑
观察每个顶层 turn 的 git 工作树快照（turn/start 与 turn/end），并对 git 不覆盖的路径在文件工具编辑前后做整文件捕获，汇总成 workspace/changes 会话事件与 workspaceChanges 服务 (src/index.ts:1-10, src/index.ts:95-183)。git 可执行文件在插件生命周期内只解析一次，macOS 上把 /usr/bin/git 的 Xcode stub 视为不可用；子代理会话被排除 (src/index.ts:72-86, src/index.ts:59-62)。服务经 ctx.provide('workspaceChanges', ...) 暴露 summary/diff，按 sessionId+seq 提供摘要与按需逐文件前后对比，会话销毁即遗忘 (src/index.ts:106-120, src/types.ts:78-97)。变更目标在 fs/write-intent、fs/edit-intent、tools/pre-execute 上以 prepend 监听捕获 (src/index.ts:158-182)。

## Provides
- ctx.workspaceChanges (按 turn 的变更摘要与逐文件前后对比服务)
- SessionEventMap 扩展: workspace/changes

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - turn 收尾钩子用于在 turn 结束前把捕获结果落定
  - 证据: `src/index.ts:14 import type {} from '@deepseek-ai/dsh-agent' + src/index.ts:155 ctx.on('agent/turn-stopping', async ({ agent, turn }) => ...) + package.json:40 peerDep`
- `dsh-session` [E1+E2] - turn/tool 事件流、会话销毁与 SessionEventMap 扩展都在 session seam 上
  - 证据: `src/index.ts:15 import type { Session, SessionId } from '@deepseek-ai/dsh-session' + src/index.ts:145 ctx.on('session/event', ...) + src/index.ts:154 ctx.on('session/disposed', ...) + src/recorder.ts:5 import from '@deepseek-ai/dsh-session' + src/types.ts:2 import type { SessionId } + package.json:41 peerDep`
- `dsh-tools` [E1+E2] - 以工具预执行为界把执行信封与会话 recorder 绑定，捕获工具产生的文件改动
  - 证据: `src/index.ts:17 import type {} from '@deepseek-ai/dsh-tools' + src/index.ts:174 ctx.on('tools/pre-execute', ...) + package.json:43 peerDep`

## Dependents (下游被依赖)
- `dsh-client-ui-deliverables` - 读取工作区变更与差异
