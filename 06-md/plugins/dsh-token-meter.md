# dsh-token-meter

- 包名: `@deepseek-ai/dsh-token-meter`
- 分组: G23 LLM 适配
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/llm/token-meter`

## 实现逻辑
提供 ctx.tokenMeter 服务，以 replay-aware 方式从持久 session log 计算请求压力与 surface (src/index.ts:101-123, 146-191, 219-240)。注册三个 session projection：tokenUsage 累计 provider usage、contextPressure 以 provider 采样叠加 O(1) shadow-price surface fold 推算占用、contextBreakdown 启发式分解 system/tools/message (src/usage-projection.ts:117-150, 173-217, src/breakdown-projection.ts:48-81)。estimate.ts 以固定密度启发式统一给消息/工具定价 (src/estimate.ts:88-102)，route-pricing.ts 按路由的图片/文件表示重定价 surface 并校验定价对齐 (src/route-pricing.ts:32-75)，turn-usage.ts 折叠一个完整 Turn 的各次尝试得出精确 token 账目 (src/turn-usage.ts:178-273)。

## Provides
- ctx.tokenMeter (从持久 session log 回放测量的 token 计量服务，供 compaction 与上下文压力消费)
- tokenUsage / contextPressure / contextBreakdown 三个 session projection 供 UI 与压缩读取

## Depends On (上游依赖)
- `dsh-compaction-image-offload` [编译依赖] - 激活 image/offload 事件投影声明以在折价时标记已卸载图像
  - 证据: `src/index.ts:8 import from '@deepseek-ai/dsh-compaction-image-offload/projection'`
- `dsh-llm` [E1+E2] - 读取路由图像定价与文件请求文本，并重组 assistant 流以估算 provider 输出
  - 证据: `src/index.ts:10 import assembleAssistantStream + src/index.ts:11 import type TokenUsage + src/index.ts:197 ctx.get('llm')`
- `dsh-llm-retry` [编译依赖] - 识别 llm/retry-started 以正确区分一次 Turn 内的多次尝试
  - 证据: `src/turn-usage.ts:3 import from '@deepseek-ai/dsh-llm-retry/types' + src/usage-projection.ts:7 import type {}`
- `dsh-session` [编译依赖] - 读取持久会话事件序列并做 surface 判定与表头规范化
  - 证据: `src/types.ts:8 import type SessionEvent + src/index.ts:19 import canonicalHeader/isSurfaceEvent/SessionSeq`
- `dsh-session-projection` [E1+E2] - 注册三个投影单元并读取其在会话上的状态
  - 证据: `src/index.ts:27 import type {} + src/index.ts:106 static inject sessionProjections + src/index.ts:114 ctx.sessionProjections.register`

## Dependents (下游被依赖)
- `dsh-acp` - 向客户端上报上下文占用（usage_update）
- `dsh-client-ui-chat` - token 计量显示
- `dsh-client-ui-conversation` - 上下文占用计量显示
- `dsh-client-ui-subagent` - 引入 token-meter 客户端类型合并（谱系行展示计量）
- `dsh-compaction-basic` - 用统一 token 计量器测量表面压力、估算摘要替换体积，并驱动所有保留与收缩定价决策
- `dsh-compaction-tool-result-pruner` - 为每个被遮蔽节点计价以写入影子价格事件，使纯消费者无需保留逐节点状态即可扣减
- `dsh-spill-policy` - 用 estimateContent 估算文本/内容 token 以决定溢出并计算头尾保留预算
