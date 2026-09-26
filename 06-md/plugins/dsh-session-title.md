# dsh-session-title

- 包名: `@deepseek-ai/dsh-session-title`
- 分组: G33 会话核心
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/session/session-title`

## 实现逻辑
SessionTitleService（ctx.sessionTitle）以会话日志为真相源维护标题：get/foldSessionTitle 从 session/title 事件折叠最新标题（src/index.ts:282-388），rename() 追加 user 来源标题从而钉住并抑制自动生成（src/index.ts:401-421）。它注册 title/titleInput 两个投影单元（src/index.ts:263-354），监听 user/message、request/header、llm/stream、session/disposed，按 provider 的 first-prompt/all-prompts 节奏在校验主请求路由后调度生成，并提供同步确定性 fallback（src/index.ts:356-378,498-523,787-832）。

## Provides
- ctx.sessionTitle (日志驱动的会话标题服务、provider 契约与确定性 fallback)

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 合并 agent 相关事件/上下文类型
  - 证据: `src/index.ts:21 type import`
- `dsh-invariants` [E1+E2] - 注册 session/title 事件来源与 messageSeqs 关系的运行时不变式
  - 证据: `src/invariant.ts:8 import + src/invariant.ts:81 ctx.invariants.register`
- `dsh-llm` [编译依赖] - 判定 agent 循环请求并读取 model 路由以驱动生成
  - 证据: `src/index.ts:11-12 import`
- `dsh-session` [E1+E2] - 以会话日志为标题真相源并声明 session/title 事件类型
  - 证据: `src/index.ts:18 import + src/types.ts:14 import + src/index.ts:403 ctx.sessions.get`
- `dsh-session-projection` [E1+E2] - 注册 title/titleInput 单元并读取 titleInput 与 turnBoundary 状态
  - 证据: `src/index.ts:19-20 import + src/index.ts:296 static inject + src/index.ts:338,545 ctx.sessionProjections`

## Dependents (下游被依赖)
- `dsh-api-session-controller` - 会话标题命令与客户端投影
- `dsh-session-reference` - 引入 title 投影键的类型合并以读取会话标题作为提及标签
- `dsh-session-title-all-prompts-llm` - 向标题服务注册 all-prompts provider
- `dsh-session-title-first-prompt-llm` - 向标题服务注册 first-prompt provider
