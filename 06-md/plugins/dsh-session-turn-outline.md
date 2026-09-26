# dsh-session-turn-outline

- 包名: `@deepseek-ai/dsh-session-turn-outline`
- 分组: G33 会话核心
- 拓扑层: Layer 4
- 来源层: L2 web-app
- 源码路径: `packages/session/session-turn-outline`

## 实现逻辑
以函数插件向 ctx.sessionProjections 注册 turnOutline 单元（src/index.ts:27-29）。该单元纯同步折叠 turn/start、user/message、assistant/message、turn/end，产出整日志轮次大纲（turn 号、turn/start seq、有界 prompt/response 预览），使客户端可枚举所有轮次并按精确 seq 定位历史分页（src/projection.ts:85-137）。stateVersion=2，仅边界/提示/回复三处改变 turns 引用以压低 change feed（src/projection.ts:90-132）。

## Provides
- turnOutline 投影单元（经 ctx.sessionProjections 交付整会话轮次大纲）

## Depends On (上游依赖)
- `dsh-session` [编译依赖] - 复用 SessionSeq 与 SessionEvent 类型锚定轮次边界
  - 证据: `src/projection.ts:24 import + src/types.ts:10 import`
- `dsh-session-projection` [E1+E2] - 把 turnOutline 单元注册到投影注册表并交付客户端视图
  - 证据: `src/projection.ts:25 import + src/index.ts:20 static inject + src/index.ts:28 ctx.sessionProjections.register`

## Dependents (下游被依赖)
- `dsh-client-ui-chat` - 轮次导航轨条目
