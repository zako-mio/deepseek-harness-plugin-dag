# dsh-plugin-package-inventory-deepseek

- 包名: `@deepseek-ai/dsh-plugin-package-inventory-deepseek`
- 分组: G23 LLM 适配
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/llm/plugin-package-inventory-deepseek`

## 实现逻辑
在官方 DeepSeek 请求上贡献 dsh_plugin_packages 字段：收集 Loader 活跃且非结构化的条目，并按请求 agent 的 standing preset 追加其预设树条目 (src/index.ts:157-185, 138-149)。PackageIdentityResolver 为每个条目解析其 owning package 的 name/version 身份——bare 包按锚点定位 manifest，相对/绝对模块则向上查找最近 manifest，并对非包松散模块返回匿名 (src/index.ts:101-135, 54-98)。去重、按确定性文本序排序后经 ctx.deepseekLlmApiExtensions.register 注册字段的 prepare 逻辑 (src/index.ts:176-204)。

## Provides
- dsh_plugin_packages 请求字段贡献 (向 ctx.deepseekLlmApiExtensions 注册，携带当前活跃插件包的 name/version 清单)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 按请求会话定位 agent，以追加其 standing preset 的活跃条目
  - 证据: `src/index.ts:16 import type {} + src/index.ts:29 inject agents + src/index.ts:165 ctx.agents.get`
- `dsh-agent-preset-registry` [E1+E2] - 查询 agent 的 standing preset 挂载树以纳入预设内活跃插件包
  - 证据: `src/index.ts:19 import type {} + src/index.ts:169 dynamic import standingMountFor + src/index.ts:164 ctx.get('agentPresets')`
- `dsh-deepseek-llm-api-extensions` [E1+E2] - 把插件包清单作为独立顶层字段注册进 DeepSeek 请求扩展注册表
  - 证据: `src/index.ts:17 import type {} + src/index.ts:29 inject deepseekLlmApiExtensions + src/index.ts:196 ctx.deepseekLlmApiExtensions.register`
- `dsh-session` [编译依赖] - 以 SessionId 类型标识请求所属会话
  - 证据: `src/index.ts:18 import type SessionId`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
