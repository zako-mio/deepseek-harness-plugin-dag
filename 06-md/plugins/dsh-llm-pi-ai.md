# dsh-llm-pi-ai

- 包名: `@deepseek-ai/dsh-llm-pi-ai`
- 分组: G22 LLM 适配
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/llm/llm-pi-ai`

## 实现逻辑
基于 @earendil-works/pi-ai 的通用 LLM 适配器：apply() 把 providers 配置解析为按路由的 profile（端点、协议、模型目录、重试策略），把已安装目录路由与自定义路由一并登记为可配置 provider 目录，并把非空路由集注册为同一个 PiAiAdapter 实例，路由集或重试策略变化时原子 re-register (src/index.ts:149-308, src/index.ts:285-308)。PiAiAdapter 每次解析产出不可变快照（profiles + Models 集合），一次操作在首个 await 之前捕获整份快照，使设置变更只影响下一次调用而不改变在途请求 (src/adapter.ts:230-256, src/adapter.ts:80-90)。请求转换由 context.ts 完成（文本历史同步转换、图片附件异步解析，超出图片字节预算时以 IMAGE_OFFLOAD_REQUIRED 明确拒绝），流式事件经 stream.ts 映射为 StreamChunk 并归一化用量与结束原因 (src/context.ts:293-320, src/stream.ts:24-141, src/stream.ts:142-175)。认证侧经 credentials 与 authorization seam 解析引用并注册登录/刷新流程，凭据存储跨快照稳定 (src/auth.ts:141-215, src/login.ts:131)。

## Provides
- ctx.llm 上的 pi-ai 后端 provider 路由集合（展示名、重试策略、模型目录）
- ctx.llm 可配置 provider 目录与模型发现（registerModelDiscovery）
- authorization 登录流程（pi-ai 提供方登录与凭据刷新记录）
- PiAiAdapter 与 pi-ai 配置类型出口（Config / Options / PiAiProviderProfile 等）

## Depends On (上游依赖)
- `cordis-plugin-loader` [E1+E2] - 配置热更新事件由 loader 发出，据此重建路由与目录
  - 证据: `src/index.ts:59 import type {} from '@deepseek-ai/cordis-plugin-loader' + src/index.ts:310 ctx.on('loader/volatile-update')`
- `dsh-authorization` [E1+E2] - 为 pi-ai 提供方注册交互式登录流程
  - 证据: `src/login.ts:12 import type { AuthorizationMethod } + src/index.ts:234 ctx.inject(['authorization'])`
- `dsh-llm` [E1+E2] - 实现 LlmAdapter 并注册进 LLM seam 才能服务请求
  - 证据: `src/index.ts:63-64 import { assertUsableApiKey, LlmError } / type { AdapterRegistrationHandle } + src/index.ts:302 ctx.llm.registerAdapter`
- `dsh-settings` [E1+E2] - 把 provider profile 暴露为 llm-pi-ai 设置段供界面编辑
  - 证据: `src/index.ts:57 import type {} from '@deepseek-ai/dsh-settings' + src/index.ts:150 ctx.inject(['settings'])`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
