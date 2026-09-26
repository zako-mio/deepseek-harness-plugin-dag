# dsh-time-context

- 包名: `@deepseek-ai/dsh-time-context`
- 分组: G08 上下文注入
- 拓扑层: Layer 5
- 来源层: L2 web-app
- 源码路径: `packages/context/time-context`

## 实现逻辑
可选的请求时钟上下文：在 agent/pre-step 前置监听中按刷新间隔节流，向请求历史追加一条持久、来源归属的时间读数（turn/step、浏览器时区、格式化的时间戳与距上次的耗时）（src/index.ts:185-225、src/index.ts:100-115）。浏览器时区从本回合用户消息的 clientTimeZone 派生，唯一时区时用于渲染时间戳，混合/缺失时渲染澄清策略行（src/request-zone.ts:48-80、src/index.ts:203-214）。注册 sessionProjections 的 timeContext 投影折叠最近消息时刻与注入时刻，用于节流判定（src/index.ts:157-183）。另附 invariant companion 校验时间读数与回合位置/时间戳一致（src/invariant.ts:77-159）。

## Provides
- session projection 'timeContext' (持久化最近消息时刻与注入时刻，供刷新节流复用)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 在 agent 步前注入时间上下文读数，并读取 turn/step 位置
  - 证据: `src/index.ts:11 import type Agent/PreStepDecision + src/index.ts:185 ctx.on('agent/pre-step', {prepend:true})`
- `dsh-invariants` [E1+E2] - 注册包级不变量，校验时间读数格式、位置与时间戳在加载与派发时可重放一致
  - 证据: `src/invariant.ts:5 import type InvariantFailure/InvariantInstaller + src/invariant.ts:25 inject ['invariants'] + src/invariant.ts:194 ctx.invariants.register`
- `dsh-llm` [编译依赖] - 构造带来源标记的时间快照 user 消息，并复用消息来源合并类型
  - 证据: `src/index.ts:12 import createUserMessage + src/index.ts:13 import type ContextFormed + src/index.ts:20 import type UserMessage + src/request-zone.ts:3 import type UserMessage`
- `dsh-session` [E1+E2] - 倒序读取会话历史以收集本回合已进入的用户消息并定位回合起点
  - 证据: `src/index.ts:21 import SessionSeq + src/invariant.ts:4 import type Session/SessionEvent + src/index.ts:89 agent.session.eventAt(SessionSeq(seq))`
- `dsh-session-projection` [E1+E2] - 注册并读取 timeContext 投影以驱动注入节流，且向 SessionProjectionStateMap 做类型合并
  - 证据: `src/index.ts:22 type-only import + src/index.ts:53 inject ['agents','sessionProjections'] + src/index.ts:157 ctx.sessionProjections.register + src/index.ts:192 ctx.sessionProjections.stateOf`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
