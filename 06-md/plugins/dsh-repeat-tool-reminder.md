# dsh-repeat-tool-reminder

- 包名: `@deepseek-ai/dsh-repeat-tool-reminder`
- 分组: G18 工具守卫
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/guard/repeat-tool-reminder`

## 实现逻辑
以 agent 为键维护「同一工具 + 规范化参数」的连续重复链，在 tools/post-execute 瀑布点观察并追加提醒，而从不否决或改写调用（src/index.ts:196-231）。参数先做深键排序再序列化以形成链键（src/index.ts:96-112），命中 thresholds 时首档发柔性提醒、后续档位带截断的参数预览（src/index.ts:206-213, 125-128）。agent/pre-step 检测到真实用户消息即重置该 agent 的链（src/index.ts:236-239）。

## Provides

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 以 agent 为键维护重复链并在用户插话时重置
  - 证据: `src/index.ts:11 import (Agent, PreStepDecision) + src/index.ts:236-237 ctx.on('agent/pre-step') + chains.delete(agent)`
- `dsh-llm` [编译依赖] - 构造模型可见的提醒消息及其生产者来源标签
  - 证据: `src/index.ts:12-13 import createUserMessage + src/index.ts:20 import MessageSource`
- `dsh-session` [编译依赖] - 提醒消息所使用的会话消息类型
  - 证据: `src/index.ts:21 import UserMessage`
- `dsh-tools` [E1+E2] - 订阅工具执行后瀑布点以观察重复调用并附加提醒
  - 证据: `src/index.ts:22 import (PostToolDecision, ToolExecution) + src/index.ts:220 ctx.on('tools/post-execute')`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
