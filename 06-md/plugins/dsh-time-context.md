# dsh-time-context

- 包名: `@deepseek-ai/dsh-time-context`
- 分组: G08 上下文注入
- 拓扑层: Layer 4
- 来源层: L3 其余
- 源码路径: `packages/context/time-context`

## 实现逻辑
以 pre-step 监听器实现每步时间上下文注入。apply() 先注册 timeContext 会话投影，跟踪最近模型可见消息时间、最近一次耐久注入时间与本轮注入时间（src/index.ts:157-183）；随后以 prepend 方式挂 agent/pre-step 瀑布，先 await next() 取回决策，再按 refreshIntervalMs（默认 600000）节流，命中时追加一条 source.kind='time-context' 的 user 消息（src/index.ts:185-225）。时区来源是本轮 user-rpc 消息的 clientTimeZone：唯一时区直接采用，混合或缺失则渲染要求模型澄清的策略行（src/request-zone.ts:48-80）；时间戳按 ISO 形 + 长偏移 + IANA 名格式化（src/timestamp.ts:31-37）。

## Provides
- sessionProjections 'timeContext' 投影状态（最近消息时间/最近注入时间，src/index.ts:157-183）
- 每步耐久时间读数注入：turn/step 时间戳与距上次可见消息的耗时（src/index.ts:100-115）
- 浏览器时区推导与策略文本（deriveBrowserTimeZoneContext/renderBrowserTimeZoneContext，src/request-zone.ts:48、src/request-zone.ts:66）

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 通过 agents 服务在 pre-step 瀑布上注入时间上下文，并复用其 PreStepDecision 契约
  - 证据: `src/index.ts:11 import type { Agent, PreStepDecision } + src/index.ts:53 export const inject = ['agents', 'sessionProjections'] + src/index.ts:185 ctx.on('agent/pre-step', ...)`
- `dsh-llm` [编译依赖] - 构造时间快照 user 消息，并声明 time-context 消息源参与上下文形成
  - 证据: `src/index.ts:12 import { createUserMessage } + src/index.ts:20 import type { UserMessage } + src/index.ts:14-18 declare module '@deepseek-ai/dsh-llm' MessageSourceMap 'time-context'`
- `dsh-session` [编译依赖] - 按序号回溯会话事件，定位本轮 turn/start 以收集本轮已进入的 user 消息
  - 证据: `src/index.ts:21 import { SessionSeq } from '@deepseek-ai/dsh-session' + src/index.ts:91 agent.session.eventAt(SessionSeq(seq))`
- `dsh-session-projection` [E1+E2] - 注册并读取可重放的时间读数投影，使节流与耗时基准在恢复会话后仍然成立
  - 证据: `src/index.ts:22 import type {} from '@deepseek-ai/dsh-session-projection' + src/index.ts:157 ctx.sessionProjections.register({ key: 'timeContext', stateVersion: 2, ... })`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
