# dsh-llm-pi-ai

- 包名: `@deepseek-ai/dsh-llm-pi-ai`
- 分组: G05 LLM适配
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/llm/llm-pi-ai`

## 为什么需要它（设计初衷）
pi-ai 支持的 DeepSeek 适配器，作为 dsh-llm-deepseek 的设计验证孪生实现，挂在 LLM seam 上。RC7 以 ReplayEnvelope 双层回放(完整/图片)与 onReplayDegrade 降级增强回放保真。

发展史：RC8 修复图片载荷过高 + 自定义OpenAI兼容网关请求格式/推理回传

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-llm-pi-ai
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/llm/llm-pi-ai

## 实现逻辑
config.ts:45-55 新增 DEFAULT_MAX_REQUEST_IMAGE_BYTES(20MiB); context.ts:151-175 toPiContext 增加 maxRequestImageBytes 参数并调用 offloadRequestImages 脱载最旧图片。catalog.ts:221-352 + config.ts:217-253 大幅扩展 OpenAI 兼容网关 compat 面(chat-template/qwen-chat-template thinking格式、maxTokensField、cacheControlFormat、supportsReasoningEffort、requiresReasoningContentOnAssistantMessages等)，修复自定义网关请求格式差异与推理回传缺失。stream.ts:43-45 将413/请求体超限判定为 INVALID_REQUEST。

## Provides
- llm 适配器: 多 provider 路由(openai/anthropic/自定义)
- 可配置 provider 目录(llm-pi-ai 设置段)
- 模型发现(registerModelDiscovery)
- llm-pi-ai 设置段 schema
- PiAiAdapter 类导出
- ReplayEnvelope 双层回放 + onReplayDegrade 降级回调

## Depends On (上游依赖)
- `dsh-llm` [运行时依赖] - inject ['llm']：registerAdapter 等
  - 证据: `packages/llm/llm-pi-ai/src/index.ts:85, 220, 246, 270`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
