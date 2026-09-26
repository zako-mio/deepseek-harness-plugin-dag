# dsh-message-feedback

- 包名: `@deepseek-ai/dsh-message-feedback`
- 分组: G15 反馈通道
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/feedback/message-feedback`

## 实现逻辑
把「已定稿助手消息」的评分/备注写入会话日志：MessageFeedbackService 暴露 Remote list/put/delete (src/index.ts:154-218)，以 per-session 串行队列在冷写路径上打开 sessionPersistence 句柄、读-比-写并广播 feedback/committed (src/index.ts:261-280)；put 前先校验目标消息确为 assistant/message 且版本匹配，未变则保留版本且不追加事件 (src/index.ts:170-185)。活会话路径直接追加并 flush 后再校验持久化前缀一致 (src/index.ts:231-259)。

## Provides
- ctx.messageFeedback (Host Remote：消息级评分与备注的 list/put/delete)
- feedback/committed 事件（冷路径持久化提交后广播）

## Depends On (上游依赖)
- `dsh-command-feedback` [编译依赖] - 复用同一反馈类别常量集
  - 证据: `src/index.ts:12 FEEDBACK_CATEGORIES import + src/types.ts:11 import`
- `dsh-llm` [编译依赖] - 关联消息反馈与 LLM 消息标识契约
  - 证据: `src/types.ts:9 import`
- `dsh-session` [E1+E2] - 读取/追加会话事件并定位活会话
  - 证据: `src/index.ts:119 inject ['sessionPersistence','sessions'] + src/index.ts:13 import`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配消息反馈命名空间
- `dsh-client-ui-message-feedback` - 消息反馈评分/视图协议类型
- `dsh-session-telemetry-otel` - 声明 feedback/message-put/delete 事件类型以判定本会话反馈
