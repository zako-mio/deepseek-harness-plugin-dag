# dsh-message-feedback

- 包名: `@deepseek-ai/dsh-message-feedback`
- 分组: G25 宿主服务
- 拓扑层: Layer 3
- 来源层: L2 web-app
- 源码路径: `packages/feedback/message-feedback`

## 为什么需要它（设计初衷）
生命周期绑定的逐消息评分与备注旁路数据（feedback 能力族）。

来源：
- https://registry.npmjs.org/@deepseek-ai/dsh-message-feedback
- https://github.com/deepseek-ai/deepseek-harness/tree/master/packages/feedback/message-feedback

## 实现逻辑
消息级 Like/Dislike+可选笔记 sidecar：MessageFeedbackService（TypertRemoteService）提供 @Remote list/put/delete；基于 storageDomain 打开 message-feedback 域表（sessions 表），经 sessionPersistence/sessions 校验会话生命周期与助手消息目标，version 乐观并发，note 字节上限（maxNoteBytes）配置。

## Provides
- ctx.messageFeedback 服务
- messageFeedback Typert Remote（list/put/delete）

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - peerDependencies（生成 typert 产物引用）
  - 证据: `packages/feedback/message-feedback/package.json:54`
- `dsh-session` [编译依赖] - deriveEventMessage/isAppendSurfaceEvent 定位目标助手消息
  - 证据: `packages/feedback/message-feedback/package.json:55; src/index.ts:10-11`
- `dsh-storage-domain` [编译依赖] - KvTable 类型与域表读写
  - 证据: `packages/feedback/message-feedback/package.json:57; src/index.ts:13`

## Dependents (下游被依赖)
- `dsh-client-ui-message-feedback` - feedback 域 wire 类型（item/rating/结果）
