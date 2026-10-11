# dsh-session-title-first-prompt-llm

- 包名: `@deepseek-ai/dsh-session-title-first-prompt-llm`
- 分组: G31 会话核心
- 拓扑层: Layer 7
- 来源层: L1 核心集
- 源码路径: `packages/session/session-title-first-prompt-llm`

## 实现逻辑
注册 id 为 session-title-first-prompt-llm、automatic 为 first-prompt 的标题 provider：apply 先用 resolveConfig 校验 targetWords/targetCjkCharacters 与共享执行控制，再调用 ctx.sessionTitle.register (src/index.ts:65-72, src/index.ts:145-166)。generate 只取请求中第一条人类消息，用语言感知的系统指令与 JSON 数组包装的输入调用 executeSessionTitleLlm，并按模型支持列表选择最小 reasoning effort (src/index.ts:81-94, src/index.ts:151-159, src/index.ts:74-76)。输出解析拒绝 tool-call 与 max-tokens 结束原因，取首个非空行并剥离整行星号强调，再归一化为非空标题 (src/index.ts:107-137)。

## Provides
- sessionTitle provider `session-title-first-prompt-llm` (由首条人类消息驱动 LLM 生成会话标题)

## Depends On (上游依赖)
- `dsh-llm` [E1+E2] - 解析模型信息并选择 reasoning effort
  - 证据: `package.json:26 peerDep + src/index.ts:6 import type LlmResolvedModelInfo/ReasoningEffortId；src/index.ts:24 inject 含 'llm'`
- `dsh-session` [运行时依赖] - 共享标题执行模块按会话取请求头与投影
  - 证据: `package.json:27 peerDep + src/index.ts:24 export const inject = ['sessionTitle','llm','sessions']`
- `dsh-session-title` [E1+E2+E3] - 把本 provider 注册进标题服务并复用标题归一化
  - 证据: `package.json:28 peerDep + src/index.ts:8-12 import normalizeSessionTitle/SessionTitleProviderId；src/index.ts:148 ctx.sessionTitle.register；packages/bundle/base/cordis.patch.yml:55-56 先装服务、:62-63 后装 provider`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
