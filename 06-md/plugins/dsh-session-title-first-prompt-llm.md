# dsh-session-title-first-prompt-llm

- 包名: `@deepseek-ai/dsh-session-title-first-prompt-llm`
- 分组: G33 会话核心
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/session/session-title-first-prompt-llm`

## 实现逻辑
函数插件向 ctx.sessionTitle 注册 automatic='first-prompt' 的 LLM 标题 provider，复用共享的 registerSessionTitleLlmProvider 与 Config 字段（src/index.ts:34-40），仅取第一条人类消息（缺失即抛错）交给给定 provider/model 路由生成标题。inject 声明 sessionTitle/llm/sessions 三项服务（src/index.ts:12）。

## Provides
- session-title first-prompt LLM provider（注册于 ctx.sessionTitle）

## Depends On (上游依赖)
- `dsh-llm` [运行时依赖] - 经 llm 服务调用模型生成标题
  - 证据: `src/index.ts:12 static inject (llm)`
- `dsh-session` [运行时依赖] - 读取会话上下文以生成标题
  - 证据: `src/index.ts:12 static inject (sessions)`
- `dsh-session-title` [运行时依赖] - 向标题服务注册 first-prompt provider
  - 证据: `src/index.ts:12 static inject (sessionTitle)`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
