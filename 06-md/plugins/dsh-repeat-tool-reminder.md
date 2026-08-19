# dsh-repeat-tool-reminder

- 包名: `@deepseek-ai/dsh-repeat-tool-reminder`
- 分组: G23 工具守卫
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/guard/repeat-tool-reminder`

## 为什么需要它（设计初衷）
仅建议的循环中断器：监控相同规范化参数连续调用同一工具的次数，达阈值注入逐级提醒，绝不否决调用。

来源：
- https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/master/packages/guard/repeat-tool-reminder/README.zh.md
- https://github.com/deepseek-ai/deepseek-harness/blob/master/.agents/notes/archived/feature/2026-07-08-repeat-tool-guard.md

## 实现逻辑
重复工具调用提醒 guard：apply 维护 WeakMap<Agent, Chain> 连续重复链。在 'tools/post-execute' 上 observe，参数深排序 canonicalize 后按 [name, canonical] 计数，命中 thresholds 则注入提醒 UserMessage 到 additionalContexts(只 enrich 不 veto)；'agent/pre-step' 在用户消息出现时重置链。

## Provides
- tools/post-execute 观察者(重复提醒注入)
- agent/pre-step 重置钩子
- 配置 thresholds/include/exclude

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - 监听 agent/pre-step
  - 证据: `packages/guard/repeat-tool-reminder/src/index.ts:11,229`
- `dsh-llm` [编译依赖] - createUserMessage
  - 证据: `packages/guard/repeat-tool-reminder/src/index.ts:12,203`
- `dsh-session` [编译依赖] - UserMessage 类型
  - 证据: `packages/guard/repeat-tool-reminder/src/index.ts:14,203`
- `dsh-tools` [运行时依赖] - 监听 tools/post-execute
  - 证据: `packages/guard/repeat-tool-reminder/src/index.ts:15,213`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
