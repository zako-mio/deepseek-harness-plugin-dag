# dsh-command-feedback

- 包名: `@deepseek-ai/dsh-command-feedback`
- 分组: G15 反馈通道
- 拓扑层: Layer 4
- 来源层: L1 核心集
- 源码路径: `packages/feedback/command-feedback`

## 实现逻辑
提供与 UI 触发解耦的会话反馈记录链路：recordFeedback() 以 session.append('feedback/record', …) 写入单条权威的 log-only 事件（去除首尾空白、空文本记为缺省）(src/index.ts:58-64)。SessionFeedbackService 作为 Host Remote 暴露 ctx.sessionFeedback.record，按 sessionId 取活会话或返回 session-not-found (src/index.ts:85-110)；apply() 同时注册全局 /feedback 斜杠命令并在无文本时返回用法错误 (src/index.ts:73-82, 117-126)。

## Provides
- ctx.sessionFeedback (Host Remote，供产品面写入会话级反馈)
- feedback/record 会话事件与 /feedback 斜杠命令
- FEEDBACK_CATEGORIES 反馈类别常量

## Depends On (上游依赖)
- `dsh-commands` [E1+E2] - 注册 /feedback 命令定义并与命令适配器对接
  - 证据: `src/index.ts:41 inject ['commands'] + src/index.ts:12 import`
- `dsh-session` [E1+E2] - 向活会话追加 feedback/record 日志事件
  - 证据: `src/index.ts:86 static inject ['sessions'] + src/index.ts:14 import`

## Dependents (下游被依赖)
- `dsh-api-remotes` - 装配命令反馈命名空间
- `dsh-client-ui-message-feedback` - 反馈记录与分类的协议类型
- `dsh-message-feedback` - 复用同一反馈类别常量集
- `dsh-session-telemetry-otel` - 声明 feedback/record 等事件类型以判定授权事件
