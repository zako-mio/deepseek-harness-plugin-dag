# dsh-llm-deepseek

- 包名: `@deepseek-ai/dsh-llm-deepseek`
- 分组: G05 LLM适配
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/llm/llm-deepseek`

## 为什么需要它（设计初衷）
Harness LLM 接缝的 DeepSeek chat-completions 官方适配器：用原生 fetch + SSE（eventsource-parser）把官方 wire 格式翻译成 StreamChunk 协议，注册 deepseek-official provider 路由，支持 thinking/reasoning_effort、KV-cache 记账、动态配置（settings+credentials 分离）、稳定错误码。解决'DeepSeek API 如何以流式、可重试、可审计方式接入 harness'的问题。RC7 新增 low 推理强度档位。

发展史：RC8 新增原生多模态图片请求(DeepSeek适配器可配置)

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/llm/llm-deepseek/README.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/llm/llm-deepseek/package.json

## 实现逻辑
新增原生多模态图片请求: index.ts:95 模型可声明 inputModalities(['image'])，:107 新增 maxRequestImageBytes 配置(默认20MiB); index.ts:276-281 通过 ctx.get('attachments') 解析attachment服务。serialize.ts:99-157 新增 imagePart/contentParts/userContent，将durable图片附件读为 data:base64 的 image_url part(仅限user角色)。adapter.ts:235-252 请求含图时校验模型模态并解析attachments; serialize.ts:185+ 推理CoT 改为每个带reasoning的turn均回传 reasoning_content。新增依赖 dsh-attachment。

## Provides
- llm 适配器: provider 路由 'deepseek-official'
- 可配置 provider 目录(llm-deepseek 设置段)
- 模型目录 deepseek-v4-flash/deepseek-v4-pro
- 推理强度档位 off/low/high/max(新增 low)
- llm-deepseek 设置段 schema
- DeepSeekAdapter 类导出

## Depends On (上游依赖)
- `dsh-llm` [运行时依赖] - inject ['llm']：registerAdapter
  - 证据: `packages/llm/llm-deepseek/src/index.ts:42, 251-256`

## Dependents (下游被依赖)
- `dsh-sdk-jsonrpc-server` - 默认 provider 初始化
