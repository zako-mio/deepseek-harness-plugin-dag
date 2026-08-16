# dsh-llm-deepseek

- 包名: `@deepseek-ai/dsh-llm-deepseek`
- 分组: G05 LLM适配
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/llm/llm-deepseek`

## 实现逻辑
DeepSeek chat-completions 适配器插件(inject ['llm'])。apply() 创建 DeepSeekAdapter(fetch+SSE，eventsource-parser 解析)，向 ctx.llm.registerAdapter(['deepseek-official'], adapter) 与 registerConfigurableProviders 注册路由；连接事实(apiKeyEnv/baseURL/models/retryPolicy)每次请求经 options() thunk 重新解析，API key 经 ctx.get('credentials') 或 launchEnvironment 按请求解析；错误码归一化(AUTH/RATE_LIMIT/QUOTA/CONTEXT_WINDOW_EXCEEDED)。

## Provides
- llm 适配器: provider 路由 'deepseek-official'
- 可配置 provider 目录(llm-deepseek 设置段)
- 模型目录 deepseek-v4-flash/deepseek-v4-pro
- llm-deepseek 设置段 schema
- DeepSeekAdapter 类导出

## Depends On (上游依赖)
- `dsh-llm` [运行时依赖] - inject ['llm']：registerAdapter
  - 证据: `packages/llm/llm-deepseek/src/index.ts:42, 251-256`

## Dependents (下游被依赖)
- `dsh-sdk-jsonrpc-server` - 默认 provider 初始化
