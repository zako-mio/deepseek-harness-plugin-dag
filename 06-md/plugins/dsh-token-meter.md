# dsh-token-meter

- 包名: `@deepseek-ai/dsh-token-meter`
- 分组: G06 LLM治理
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/llm/token-meter`

## 为什么需要它（设计初衷）
通过单例 ctx.tokenMeter 提供回放感知的 token 测量：从持久日志为每会话推进隔离 fold，压缩(compaction)等压力敏感插件共享计量，无需依赖 CompactionEngine。用固定启发式（4字符≈1token+结构开销）估算，保证测量与模型路由/压缩解耦。

发展史：位于 packages/llm/token-meter，2026-08-10 首批发布，0.1.0-rc.6 转公开。dsh-compaction-basic 的默认计量依赖；提供 tokenUsage/contextPressure/contextBreakdown 三个会话投影单元。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/llm/token-meter/README.zh.md
- https://registry.npmjs.org/@deepseek-ai/dsh-token-meter

## 实现逻辑
Replay-aware token 计量服务(ctx.tokenMeter)。TokenMeter 服务按 session 维护 ReplayState，惰性折叠事件日志得出请求压力与 surface token 估算；measure() 输出基线+surface 增量；estimateMessage/estimateHeader 启发式计价；可选注入 sessionProjections 注册 usage/contextPressure/breakdown 三个投影定义。

## Provides
- ctx.tokenMeter(TokenMeter)
- measure(): TokenMeasurement
- estimateMessage()
- tokenUsage/contextPressure/contextBreakdown 投影定义
- TokenMeterConfig

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - BlockAssembler/deepFreeze；TokenUsage 类型
  - 证据: `packages/llm/token-meter/src/index.ts:9-10`
- `dsh-session` [运行时依赖] - 订阅 session/event；折叠 header/surface
  - 证据: `packages/llm/token-meter/src/index.ts:11-12, 95-97`
- `dsh-session-projection` [运行时依赖] - ctx.inject(['sessionProjections']) 注册投影
  - 证据: `packages/llm/token-meter/src/index.ts:14, 87-91`

## Dependents (下游被依赖)
- `dsh-client-ui-conversation` - tokenUsage/contextPressure/contextBreakdown 投影类型
- `dsh-compaction-basic` - measure 定价压力/收敛
- `dsh-compaction-tool-result-pruner` - estimateMessage 计算 shadowedTokenCount
