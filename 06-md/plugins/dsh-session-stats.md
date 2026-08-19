# dsh-session-stats

- 包名: `@deepseek-ai/dsh-session-stats`
- 分组: G25 宿主服务
- 拓扑层: Layer 3
- 来源层: L2 web-app
- 源码路径: `packages/session/session-stats`

## 为什么需要它（设计初衷）
注册 sessionStats 投影单元，从日志折算 turn/step 数与各阶段耗时的会话统计。

来源：
- https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/session/session-stats/README.md

## 实现逻辑
函数插件：在 ctx.sessionProjections.register 注册 'sessionStats' 投影单元（projection.ts 纯 fold：turn/step 计数、llm/tool/ttft/decode 墙钟与输出 token，zod schema 校验状态），apply 按事件流 step/start、assistant/chunk、assistant/message、tool/call、tool/result 折叠；交付由投影 seam 负责。

## Provides
- sessionStats 投影单元（key 'sessionStats'）

## Depends On (上游依赖)
- `dsh-llm` [编译依赖] - isTokenDelta 判定首 token
  - 证据: `packages/session/session-stats/package.json:45; src/projection.ts:27`
- `dsh-session` [编译依赖] - peerDependencies（事件类型）
  - 证据: `packages/session/session-stats/package.json:46`
- `dsh-session-projection` [编译依赖] - ProjectionDefinition 类型
  - 证据: `packages/session/session-stats/package.json:47; src/projection.ts:28`

## Dependents (下游被依赖)
- `dsh-client-ui-conversation` - sessionStats 投影 key 类型合并
