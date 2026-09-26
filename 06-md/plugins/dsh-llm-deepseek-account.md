# dsh-llm-deepseek-account

- 包名: `@deepseek-ai/dsh-llm-deepseek-account`
- 分组: G23 LLM 适配
- 拓扑层: Layer 2
- 来源层: L1 核心集
- 源码路径: `packages/llm/llm-deepseek-account`

## 实现逻辑
以 DeepSeek 账号令牌为鉴权实现官方 provider 路由 'deepseek-account'：resolveAuth 经 ctx.get('deepseekAccount').resolveToken 取令牌并注入 x-dsh-auth-token 头 (src/index.ts:20-38)，在 onRequestError 中把配额超限映射为 ACCOUNT_QUOTA_EXCEEDED、401 映射为 ACCOUNT_TOKEN_INVALID 并拒绝失效令牌 (src/index.ts:26-36)。向 ctx.llm 注册可配置 provider 目录项并注册适配器 (src/index.ts:39-53)，配置直接复用 llm-deepseek 的协议字段（无 API-key 引用）(src/config.ts:2-6)。

## Provides
- DeepSeek Account provider 路由注册 (以账号令牌鉴权，向 ctx.llm 注册 'deepseek-account' 适配器与可配置目录项)

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - 复用 provider 无关的错误码与错误类型表达鉴权/配额失败
  - 证据: `src/index.ts:4 import ACCOUNT_QUOTA_EXCEEDED_CODE/LlmError/QUOTA_EXCEEDED_CODE`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
