# dsh-session-title-all-prompts-llm

- 包名: `@deepseek-ai/dsh-session-title-all-prompts-llm`
- 分组: G35 会话存储变体
- 拓扑层: Layer 4
- 来源层: L3 其余
- 源码路径: `packages/session/session-title-all-prompts-llm`

## 为什么需要它（设计初衷）
会话标题的 LLM 提供方插件：用全部用户消息生成标题。

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-session-title-all-prompts-llm
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/session/session-title-all-prompts-llm

## 实现逻辑
全人类消息 LLM 标题 provider：apply() 调 dsh-session-title-llm 的 registerSessionTitleLlmProvider(ctx, config, name='session-title-all-prompts-llm', automatic='all-prompts', selectMessages=messages=>messages)，即选择全部人类消息作为标题生成输入（与 first-prompt 变体仅选择首个 prompt 对照）。inject ['sessionTitle','llm','sessions']。Config 复用 SessionTitleLlmConfigFields（targetWords/targetCjkCharacters/maxInputBytes/maxOutputTokens/timeoutMs/provider/model，required LLM 策略，无默认）。registerSessionTitleLlmProvider 内部：resolveSessionTitleLlmConfig 校验并 deepFreeze 配置 → ctx.sessionTitle.register({id: SessionTitleProviderId, automatic, generate})；generate 经 llm 发辅助请求（systemPrompt 语言感知 + frameMessages JSON 围栏防 prompt 注入），route 回退 request/header 捕获的 provider/model。

## Provides
- ctx.sessionTitle 注册的 'all-prompts' 自动标题 provider（automatic='all-prompts'）
- 全部人类消息选择器（selectMessages=identity）
- LLM 生成标题（语言感知 system prompt + JSON 围栏）

## Depends On (上游依赖)
- `dsh-llm` [运行时依赖] - llm 服务：辅助模型调用生成标题
  - 证据: `packages/session/session-title-all-prompts-llm/src/index.ts:12 inject ['llm']；session-title-llm/src/index.ts generateSessionTitleWithLlm 发辅助请求`
- `dsh-session` [运行时依赖] - 会话事件流：标题生成时机（事件驱动）
  - 证据: `packages/session/session-title-all-prompts-llm/src/index.ts:12 inject ['sessions']；session-title/src/index.ts:262 static inject ['sessions']`
- `dsh-session-title` [运行时依赖] - 标题服务：provider 注册契约（SessionTitleProviderId/automatic/generate）
  - 证据: `packages/session/session-title-all-prompts-llm/src/index.ts:12 inject ['sessionTitle']；registerSessionTitleLlmProvider 内部 ctx.sessionTitle.register（session-title-llm/src/index.ts:162）；package.json:33`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
