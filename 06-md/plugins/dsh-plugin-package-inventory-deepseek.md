# dsh-plugin-package-inventory-deepseek

- 包名: `@deepseek-ai/dsh-plugin-package-inventory-deepseek`
- 分组: G22 LLM 适配
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/llm/plugin-package-inventory-deepseek`

## 实现逻辑
为官方 DeepSeek 请求贡献 dsh_plugin_packages 字段：apply() 在启用时把该字段的 provider 注册进 ctx.deepseekLlmApiExtensions，prepare 时现场收集活跃插件包 (src/index.ts:199-213)。collectActivePluginPackages 从 loader 条目树取处于 ACTIVE 且非 group、非 disabled 的条目，并在给出 sessionId 时并入该 agent 的 preset 组合模块 (src/index.ts:137-146, src/index.ts:154-192)。PackageIdentityResolver 以裸包名经 pluginPackages 或 require 解析路径、否则向上寻找最近的 package.json，读取 name/version 并按进程缓存，无法解析的条目只告警一次且不进入清单 (src/index.ts:55-133, src/index.ts:176-188)。最终按 name/version 做确定性文本排序并去重，得到与宿主 ICU/locale 无关的线上值 (src/index.ts:148-151, src/index.ts:174-191)。

## Provides
- DeepSeek 请求扩展字段 dsh_plugin_packages（当前活跃插件包清单，version: 1）

## Depends On (上游依赖)
- `cordis-plugin-loader` [E1+E2] - 活跃插件包身份只能从 loader 条目树与 fiber 状态取得
  - 证据: `src/index.ts:15 import type { EntryTree } + src/index.ts:29 inject ['loader'] + src/index.ts:161 ctx.loader`
- `dsh-agent` [E1+E2] - 按请求 session 定位所属 agent，进而读取其 preset 组合
  - 证据: `src/index.ts:16 import type {} from '@deepseek-ai/dsh-agent' + src/index.ts:164 ctx.agents.get(...)`
- `dsh-agent-preset-registry` [E1+E2] - 可选地把请求 agent 的 preset 组合模块并入插件包清单
  - 证据: `src/index.ts:19 import type {} + src/index.ts:162 ctx.get('agentPresets')`
- `dsh-deepseek-llm-api-extensions` [E1+E2] - 字段必须注册进扩展注册表才会并入官方 DeepSeek 请求
  - 证据: `src/index.ts:17 import type {} + src/index.ts:205 ctx.deepseekLlmApiExtensions.register('dsh_plugin_packages')`
- `dsh-session` [编译依赖] - 请求携带的 sessionId 类型由会话 seam 定义
  - 证据: `src/index.ts:18 import type { SessionId } + package.json:44 peerDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
