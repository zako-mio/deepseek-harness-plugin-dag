# dsh-llm-deepseek

- 包名: `@deepseek-ai/dsh-llm-deepseek`
- 分组: G05 LLM适配
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/llm/llm-deepseek`

## 为什么需要它（设计初衷）
Harness LLM 接缝的 DeepSeek chat-completions 官方适配器：用原生 fetch + SSE（eventsource-parser）把官方 wire 格式翻译成 StreamChunk 协议，注册 deepseek-official provider 路由，支持 thinking/reasoning_effort、KV-cache 记账、动态配置（settings+credentials 分离）、稳定错误码。解决'DeepSeek API 如何以流式、可重试、可审计方式接入 harness'的问题。RC7 新增 low 推理强度档位。

发展史：与 pi-ai 库级实现 dsh-llm-pi-ai 并列为同一接缝的双实现，刻意用 deepseek-official 路由名与 pi-ai 的 deepseek 区分以便同仓共存。在 0.1.0-rc.x 迭代中增加思考模式序列化、reasoning passback、app attribution 头、compaction 标记等。版本 0.1.0-rc.7。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/llm/llm-deepseek/README.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/llm/llm-deepseek/package.json

## 实现逻辑
DeepSeek chat-completions 适配器插件(inject ['llm'])。apply() 创建 DeepSeekAdapter(fetch+SSE，eventsource-parser 解析)，向 ctx.llm.registerAdapter(['deepseek-official'], adapter) 与 registerConfigurableProviders 注册路由；连接事实(apiKeyEnv/baseURL/models/retryPolicy)每次请求经 options() thunk 重新解析，API key 经 ctx.get('credentials') 或 launchEnvironment 按请求解析；错误码归一化(AUTH/RATE_LIMIT/QUOTA/CONTEXT_WINDOW_EXCEEDED)。RC7：推理强度新增 low 档，reasoningEffort 支持 off/low/high/max 四级(thinking 关闭时仅允许 off)。

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
