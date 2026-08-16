# dsh-session-title

- 包名: `@deepseek-ai/dsh-session-title`
- 分组: G08 会话展示
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/session/session-title`

## 实现逻辑
Log-backed 会话标题服务。SessionTitleService(ctx.sessionTitle，static inject=['sessions']) 以 session log 中 'session/title' 事件为唯一事实源。监听 'session/event'(user/message 触发自动调度)、'llm/stream'(主请求路由)、'session/disposed'(中止在途)；自动生成走 provider 注册 + 确定性 fallback 双轨；user rename() 钉住标题。注册 'title' 投影单元。

## Provides
- ctx.sessionTitle(get/rename/refresh/register)
- session/title 会话事件
- title projection key
- SessionTitleProvider 契约
- fallbackSessionTitle/foldSessionTitle

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - isAgentLoopRequest
  - 证据: `packages/session/session-title/src/index.ts:10-11,331-334`
- `dsh-session` [运行时依赖] - 事件源读取/追加
  - 证据: `packages/session/session-title/src/index.ts:262,319,374`
- `dsh-session-projection` [运行时依赖] - 注册 title 纯折单元
  - 证据: `packages/session/session-title/src/index.ts:308-317`

## Dependents (下游被依赖)
- `dsh-agent-spine-demo` - ctx.plugin(SessionTitleService) 会话标题服务
- `dsh-host-apiproxy` - SessionTitleInvalidError
- `dsh-session-title-all-prompts-llm` - 标题服务：provider 注册契约（SessionTitleProviderId/automatic/generate）
- `dsh-session-title-first-prompt-llm` - 注册进标题服务
