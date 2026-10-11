# dsh-session-title-all-prompts-llm

- 包名: `@deepseek-ai/dsh-session-title-all-prompts-llm`
- 分组: G13 实验特性
- 拓扑层: Layer 7
- 来源层: L3 其余
- 源码路径: `packages/experimental/session-title-all-prompts-llm`

## 实现逻辑
以「sessionTitle provider 注册」实现：Config 在共享 SessionTitleLlmConfig 之上追加 targetWords/targetCjkCharacters 两个必填长度目标，resolveConfig 对二者做正整数校验并复用 resolveSessionTitleLlmConfig 校验共享执行控制 (src/index.ts:28-72)。apply 用 SessionTitleProviderId(name) 生成 id，向 ctx.sessionTitle 注册 automatic:'all-prompts' 的提供者，generate 把全部人类消息（及 provider 来源的 currentTitle 锚点）框成 JSON 交给 executeSessionTitleLlm，并按目标语言与是否锚定生成系统指令 (src/index.ts:154-176, src/index.ts:81-103)。模型输出经 titleFromOutput 取首个非空行、剥离整行星号强调，并拒绝 tool-call/max-tokens 结束态后由 normalizeSessionTitle 规范化 (src/index.ts:116-146)。

## Provides
- ctx.sessionTitle (注册 id 为 session-title-all-prompts-llm、automatic:'all-prompts' 的会话标题提供者：以全部人类消息经 LLM 生成/更新标题)

## Depends On (上游依赖)
- `dsh-llm` [E1+E2] - 声明 llm 服务依赖，并按路由支持的最低 reasoning effort 为标题调用选择推理档
  - 证据: `package.json:26 peerDep + src/index.ts:6 import LlmResolvedModelInfo/ReasoningEffortId + src/index.ts:24 inject 'llm'`
- `dsh-session` [E1+E2] - 声明 sessions 服务依赖，标题生成需在会话上下文中执行
  - 证据: `package.json:27 peerDep + src/index.ts:24 inject 'sessions'`
- `dsh-session-title` [E1+E2] - 向会话标题服务注册一个自动标题提供者，并复用其 id 构造与标题规范化
  - 证据: `package.json:28 peerDep + src/index.ts:8-12 import normalizeSessionTitle/SessionTitleProviderId + src/index.ts:157 ctx.sessionTitle.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
