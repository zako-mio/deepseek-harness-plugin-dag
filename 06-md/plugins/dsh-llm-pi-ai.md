# dsh-llm-pi-ai

- 包名: `@deepseek-ai/dsh-llm-pi-ai`
- 分组: G05 LLM适配
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/llm/llm-pi-ai`

## 为什么需要它（设计初衷）
pi-ai 支持的 DeepSeek 适配器，作为 dsh-llm-deepseek 的设计验证孪生实现，挂在 LLM seam 上。

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-llm-pi-ai
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/llm/llm-pi-ai

## 实现逻辑
pi-ai 库驱动的通用 LLM 适配器插件(inject ['llm'])。apply() 按 provider 配置 dict 生成 PiAiAdapter(继承 LlmAdapter)，routes 来自 pi-ai catalog 或手声明；每次请求解析 profile，key 经 credentials/launchEnvironment 解析；ctx.llm.registerConfigurableProviders 维护目录、registerModelDiscovery 提供端点问询、registerAdapter 注册路由；含模型回放与图片附件解析(resolveAttachments→ctx.get('attachments'))。

## Provides
- llm 适配器: 多 provider 路由(openai/anthropic/自定义)
- 可配置 provider 目录(llm-pi-ai 设置段)
- 模型发现(registerModelDiscovery)
- llm-pi-ai 设置段 schema
- PiAiAdapter 类导出

## Depends On (上游依赖)
- `dsh-llm` [运行时依赖] - inject ['llm']：registerAdapter 等
  - 证据: `packages/llm/llm-pi-ai/src/index.ts:85, 220, 246, 270`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
