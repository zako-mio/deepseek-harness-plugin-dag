# dsh-compaction-basic

- 包名: `@deepseek-ai/dsh-compaction-basic`
- 分组: G07 上下文压缩
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/compaction/compaction-basic`

## 实现逻辑
压缩 seam 的基础后端实现 BasicCompactionEngine，继承 CompactionEngine 并实现 summarize/compactIfNeeded/compactRegion/compactNow 四个钩子（src/index.ts:113、src/index.ts:247、src/index.ts:269、src/index.ts:358、src/index.ts:383）。summarize 通过一次 ctx.llm.stream() 复用会话原有 system/tools/消息前缀做 KV-cache 友好的摘要调用（src/summarizer.ts:120-181）；region.ts 负责可压缩区间的选择、工具配对边界校验与 compaction/start→summary→end 的持久化事务（src/region.ts:117-155、src/region.ts:173-276）。apply 阶段注册 agent/pre-step 压力检测、agent/request-error 上下文溢出恢复（按 maxOverflowRetries 重试）等自动监听器（src/index.ts:148-235）。配置在加载期做严格校验并按路由模型解析阈值/保留/摘要预算（src/config.ts:68-110、src/config.ts:153-217）。

## Provides
- ctx.compaction (压缩 seam 的基础后端实现，提供基于 tokenMeter 压力测量的自动/手动压缩)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 在 agent 的步边界与请求错误扩展点上挂自动压缩与溢出恢复，并借 agent.runMaintenance 预约空闲会话的手动压缩
  - 证据: `src/index.ts:15 import type Agent/PreStepDecision + src/index.ts:158 ctx.on('agent/pre-step') + src/index.ts:178 ctx.on('agent/status') + src/index.ts:190 ctx.on('agent/request-error') + src/index.ts:390 agent.runMaintenance`
- `dsh-commands` [编译依赖] - 手动命令发起的压缩需把发起命令身份写进压缩生命周期事件用于呈现关联
  - 证据: `src/index.ts:16 import type CommandId + src/region.ts:18 import type CommandId + src/region.ts:392 sourceCommandId`
- `dsh-compaction-tool-result-pruner` [E1+E2] - 可选地先执行无模型工具结果裁剪降低压力，再决定是否摘要；缺少该插件时保持可独立组合
  - 证据: `src/index.ts:18 type-only import (makes sibling service available to ctx.get) + src/index.ts:292 this.ctx.get('toolResultPruner') + src/index.ts:295 prune.pruneSession`
- `dsh-llm` [E1+E2] - 解析路由模型上下文容量以计算压力阈值，并通过 llm 流式调用执行摘要、构造备份检查点消息
  - 证据: `src/index.ts:12 import CONTEXT_WINDOW_EXCEEDED_CODE + src/index.ts:114 inject 'llm' + src/index.ts:304 ctx.llm.resolveModelInfo + src/summarizer.ts:163 ctx.llm.stream + src/region.ts:19 createUserMessage/errorChain`
- `dsh-session` [E1+E2] - 直接读写会话表面的追加/替换事务与事件流，并在手动压缩后通过 sessions.flush 做持久化检查点
  - 证据: `src/index.ts:11 import type Session/SessionSeq + src/index.ts:114 inject 'sessions' + src/index.ts:184 ctx.on('session/event') + src/index.ts:411 ctx.sessions.flush + src/region.ts:22 import SessionSeq/Session/SessionEvent`
- `dsh-token-meter` [E1+E2] - 用统一 token 计量器测量表面压力、估算摘要替换体积，并驱动所有保留与收缩定价决策
  - 证据: `src/index.ts:114 inject 'tokenMeter' + src/index.ts:277 ctx.tokenMeter.measure + src/region.ts:21 import type TokenMeasurement/TokenMeter + src/region.ts:417 meter.estimateMessage`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
