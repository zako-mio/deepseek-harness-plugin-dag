# dsh-experimental-client-ui-agent-team

- 包名: `@deepseek-ai/dsh-experimental-client-ui-agent-team`
- 分组: G13 实验特性
- 拓扑层: Layer 15
- 来源层: L3 其余
- 源码路径: `packages/experimental/client-ui-agent-team`

## 实现逻辑
Host 半边为空 `apply()`，行为完全在浏览器侧（src/index.ts:4）。Client 侧 `registerAgentTeamUi()` 注册 agent-team locale 字典，并把 Team 动作注入 conversation header 的 `conversation.session.header.actions` 槽（src/client/mount.ts:29-62）。打开成员时先用会话的 subagent address 归一到 Lead Session，再经 `uiWorkspace.openSession` 打开父会话或 continuable 子会话（src/client/mount.ts:32-51）。

## Provides

## Depends On (上游依赖)
- `dsh-api-session-controller` [E1+E2] - 读取会话绑定与保留信息定位 Lead/子会话
  - 证据: `src/client/TeamAction.tsx:8 import '@deepseek-ai/dsh-api-session-controller/client' + src/client/mount.ts:4 import + src/client/mount.ts:21 inject 'sessions'`
- `dsh-client-locale` [E1+E2] - 注册中英文 Team 文案字典
  - 证据: `src/client/mount.ts:7 import '@deepseek-ai/dsh-client-locale/client' + src/client/mount.ts:21 inject 'locale' + src/client/mount.ts:30 locale.register`
- `dsh-client-ui-conversation` [编译依赖] - 在会话头部动作区渲染 Team 入口
  - 证据: `src/client/TeamAction.tsx:16 import '@deepseek-ai/dsh-client-ui-conversation/client' + src/client/mount.ts:6 import`
- `dsh-client-ui-renderer` [编译依赖] - 让注册的组件被渲染管线识别
  - 证据: `src/client/mount.ts:8 import '@deepseek-ai/dsh-client-ui-renderer/client'`
- `dsh-client-ui-workspace` [E1+E2] - 切换/打开成员会话视图
  - 证据: `src/client/mount.ts:9 import '@deepseek-ai/dsh-client-ui-workspace/client' + src/client/mount.ts:21 inject 'uiWorkspace' + src/client/mount.ts:42 openSession`
- `dsh-session` [编译依赖] - 使用会话 id 类型与快照字段
  - 证据: `src/client/TeamAction.tsx:3 import SessionId + src/client/mount.ts:5 import '@deepseek-ai/dsh-session/types'`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
