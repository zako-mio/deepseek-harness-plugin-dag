# dsh-llm-deepseek-api-key

- 包名: `@deepseek-ai/dsh-llm-deepseek-api-key`
- 分组: G22 LLM 适配
- 拓扑层: Layer 1
- 来源层: L1 核心集
- 源码路径: `packages/llm/llm-deepseek-api-key`

## 实现逻辑
为官方 DeepSeek 路由提供 API-key 认证与凭据门控的模型发现：apply() 先解析一次配置（含端点与 DEEPSEEK_API_KEY 凭据引用）使错误在加载期暴露，再向 ctx.llm 声明可配置 provider (src/index.ts:17-38)。resolveApiKey 优先经 credentials seam 解析引用，无 seam 时退回启动环境，缺失即以 MISSING_CREDENTIAL 明确报错并指明修复位置（不回显密钥）(src/index.ts:20-35)。随后 registerDeepSeekProvider 注册 'deepseek-official'：认证头为 x-api-key，模型发现先做凭据门控、无凭据时返回空目录而非抛错 (src/index.ts:39-51)。配置解析把端点事实与凭据引用固定在同一代，避免两代配置混用 (src/config.ts:37-38)。

## Provides
- ctx.llm 的 deepseek-official provider 路由（API-key 认证头 + 凭据门控的模型发现）
- Config / plainOptions / resolveAdapterOptions 配置出口

## Depends On (上游依赖)
- `cordis-plugin-loader` [编译依赖] - 读取 loader 注入的 fiber 条目 id 作为 settings 命名空间
  - 证据: `src/index.ts:4 import type {} from '@deepseek-ai/cordis-plugin-loader' + package.json:35 可选 peerDep`
- `dsh-llm` [E1+E2] - 适配器必须注册进 LLM seam 才能被路由与发现
  - 证据: `src/index.ts:3 import { assertUsableApiKey, LlmError } + src/index.ts:13 inject ['llm'] + src/index.ts:36 ctx.llm.registerConfigurableProviders`

## Dependents (下游被依赖)
- `dsh-sdk-jsonrpc-server` - provider 无适配器且为 deepseek-official 时按需挂载回退适配器
