# dsh-compaction-image-offload

- 包名: `@deepseek-ai/dsh-compaction-image-offload`
- 分组: G07 上下文压缩
- 拓扑层: Layer 5
- 来源层: L1 核心集
- 源码路径: `packages/compaction/compaction-image-offload`

## 实现逻辑
图像卸载执行器：当具备图像能力的路由以 IMAGE_OFFLOAD_REQUIRED 拒绝请求时，插件通过 offloadOldestImages 选取最旧的保留输入图像并追加一条 image/offload 决策事件（src/index.ts:27-32、src/image-offload.ts:16-45）。注册的 imageOffloadProjection 在重放时把被选中的图像块标记为 offloaded，形成持久化的表面修复而不是花费重试预算（src/projection.ts:40-73、src/project-message.ts:13-35）。同时对压缩摘要失败（compaction/summary-error）走同一卸载恢复路径（src/index.ts:33-40）。

## Provides

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 在 agent 请求错误扩展点上拦截图像卸载失败并返回 retry 动作，发起一次表面修复后的重试
  - 证据: `src/index.ts:13 import type RequestErrorAction + src/index.ts:19 inject 'agents' + src/index.ts:27 ctx.on('agent/request-error')`
- `dsh-llm` [编译依赖] - 识别适配器上报的 IMAGE_OFFLOAD_REQUIRED 失败码，并按 dsh-llm 的内容块/消息类型改写图像块
  - 证据: `src/index.ts:14 import IMAGE_OFFLOAD_REQUIRED_CODE/LlmError + src/image-offload.ts:3 import type ContentBlock + src/project-message.ts:3 import type ContentBlock/Message + src/projection.ts:3 import type Message`
- `dsh-session` [E1+E2] - 在会话表面上追加 image/offload 事件并注册纯函数消息投影，使卸载决策可重放且不改动节点身份
  - 证据: `src/index.ts:19 inject 'sessions' + src/index.ts:26 ctx.sessions.registerMessageProjection + src/image-offload.ts:4 import type Session/SessionSeq + src/projection.ts:4-5 subpath 类型 import`

## Dependents (下游被依赖)
- `dsh-token-meter` - 激活 image/offload 事件投影声明以在折价时标记已卸载图像
