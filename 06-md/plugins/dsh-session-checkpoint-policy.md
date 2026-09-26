# dsh-session-checkpoint-policy

- 包名: `@deepseek-ai/dsh-session-checkpoint-policy`
- 分组: G33 会话核心
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/session/session-checkpoint-policy`

## 实现逻辑
在三个副作用边界插入语义持久化检查点：llm/stream 在适配器派发首个 chunk 前先 ctx.sessions.flush 完整已记录请求前缀（src/index.ts:64-68,29-38）；tools/execute 对顶层工具调用在工具体执行前 flush，若已中止则返回规范的 TOOL_ABORTED_BEFORE_DISPATCH 错误结果（src/index.ts:70-75,41-50）；agent/pre-step 在下一步请求前持久化前一步提交（src/index.ts:79-82）。检查点失败在模型与工具副作用边界 fail-closed，不调用下游适配器/工具体。

## Provides
- 语义持久化检查点策略（llm/tools/agent 边界强制 flush；无自有 ctx 服务）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 在每步请求前持久化前一步结果
  - 证据: `src/index.ts:11 import + src/index.ts:79 agent/pre-step`
- `dsh-llm` [E1+E2] - 在模型流请求边界做检查点
  - 证据: `src/index.ts:9 import + src/index.ts:18 static inject + src/index.ts:64 llm/stream`
- `dsh-session` [编译依赖] - 引用 Session 类型并对其调用 flush
  - 证据: `src/index.ts:8 import`
- `dsh-tools` [E1+E2] - 在工具执行边界做检查点并复用中止错误码
  - 证据: `src/index.ts:10 import + src/index.ts:18 static inject + src/index.ts:70 tools/execute`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
