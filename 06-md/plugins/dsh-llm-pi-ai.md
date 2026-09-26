# dsh-llm-pi-ai

- 包名: `@deepseek-ai/dsh-llm-pi-ai`
- 分组: G23 LLM 适配
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/llm/llm-pi-ai`

## 实现逻辑
以 @earendil-works/pi-ai 为后端实现通用多 provider LLM 适配器：PiAiAdapter 每次操作捕获一个不可变 snapshot（profiles 与其 Models 集合），保证一次调用的 provider/模型/凭据在 await 期间冻结 (src/adapter.ts:232-241, 330-348)。config.ts 按 provider 路由解析 profile、物化模型目录与注册时捕获的 retryPolicy (src/config.ts:410-509)，context.ts 把 harness 消息历史（含持久图像解析与 offload 占位）转成 pi-ai 的 Context (src/context.ts:262-338)。index.ts 以设置驱动注册/原子替换适配器路由与可配置目录，并注册按命名空间的模型发现 (src/index.ts:285-316, 275-278)；auth.ts 与 login.ts 把 harness 的 credentials/authorization seam 桥接到 pi-ai 的凭据存储与登录流 (src/auth.ts:141-231, src/login.ts:120-160)。

## Provides
- pi-ai 多 provider LLM 适配器 (向 ctx.llm 注册一组 provider 路由，实现 LlmAdapter 并声明各路由 retry policy)
- pi-ai 凭据/登录桥接 (把 credentials 记录与 authorization 流程映射为 pi-ai 的 CredentialStore/AuthContext 与登录事件)

## Depends On (上游依赖)
- `dsh-authorization` [E1+E2] - 把 pi-ai 的登录会话翻译成 harness 中立的通知/提问流程
  - 证据: `src/login.ts:12 import type AuthorizationMethod + src/login.ts:138 ctx.authorization.registerFlow`
- `dsh-llm` [E1+E2] - 实现并注册 llm seam 适配器，复用其错误类型、图像投影与目录 API
  - 证据: `src/adapter.ts:41 import LlmAdapter/attributionHeaders + src/index.ts:94 inject llm + src/index.ts:302 ctx.llm.registerAdapter`
- `dsh-settings` [编译依赖] - 激活 settings 服务声明，使插件可按设置命名空间配置 provider 路由
  - 证据: `src/index.ts:57 import type {} from '@deepseek-ai/dsh-settings'`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
