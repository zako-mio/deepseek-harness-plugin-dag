# dsh-llm-deepseek-api-key

- 包名: `@deepseek-ai/dsh-llm-deepseek-api-key`
- 分组: G23 LLM 适配
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/llm/llm-deepseek-api-key`

## 实现逻辑
以 API key 鉴权实现官方 DeepSeek 路由 'deepseek-official'：resolveApiKey 先经 ctx.get('credentials').resolve 解析凭据引用，无 seam 时退化到启动环境变量，对空或含非法字符的 key 抛 INVALID_CREDENTIAL (src/index.ts:20-35)。注册可配置 provider 目录项并以 x-api-key 头鉴权、以 catalogModelInfo 列出模型 (src/index.ts:36-46)。config.ts 在协议配置上追加默认 DEEPSEEK_API_KEY 的 credential-ref 字段，并与端点一起解析出 ResolvedDeepSeekOptions (src/config.ts:14-38)。

## Provides
- DeepSeek 官方 provider 路由注册 (以 API key 鉴权，向 ctx.llm 注册 'deepseek-official' 适配器与可配置目录项)

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 复用共享的 API key 可用性校验与错误类型
  - 证据: `src/index.ts:3 import assertUsableApiKey/LlmError`

## Dependents (下游被依赖)
- `dsh-sdk-jsonrpc-server` - 接入 DeepSeek API key 凭据 seam
