# dsh-time-context

- 包名: `@deepseek-ai/dsh-time-context`
- 分组: G34 Web上下文扩展
- 拓扑层: Layer 3
- 来源层: L3 其余
- 源码路径: `packages/context/time-context`

## 实现逻辑
opt-in 请求时钟上下文插件：apply() 注册 prepend 的 'agent/pre-step' 监听器（inject ['agents']）。每个符合条件 step 在决定消息中附加持久、来源归属（source.kind='plugin', form='snapshot'）的 UserMessage：当前时间（Intl.DateTimeFormat 按选定时区格式化）+ 距上一条模型可见消息（step=1）或上一次 step 上下文（step>1）的 elapsed 时长。浏览器时区感知：deriveBrowserTimeZoneContext 从请求消息中解析浏览器时区，无唯一浏览器 zone 时回退进程时区（config.timeZone 可覆盖）；refreshIntervalMs 提供会话内最小注入间隔（读 raw durable 事件找上次注入，避免进程本地缓存）。验证：非法 refreshIntervalMs/无法解析时区即插件加载失败。precedingMessageTime 只统计 user/message|assistant/message|tool/result 模型可见事件。

## Provides
- agent/pre-step prepend 监听器（每次请求注入时间快照 UserMessage）
- 持久时间上下文（turn/step + 时区 + elapsed 时长 + 浏览器时区检测）
- source.kind='plugin' form='snapshot' 的会话事件写入

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - agent/pre-step 事件词表与 PreStepDecision 注入契约
  - 证据: `packages/context/time-context/src/index.ts:10 Agent/PreStepDecision 类型；170 ctx.on('agent/pre-step')；package.json:38`
- `dsh-llm` [编译依赖] - 构造注入的 UserMessage 载荷
  - 证据: `packages/context/time-context/src/index.ts:11 createUserMessage + UserMessage 类型`
- `dsh-session` [编译依赖] - 扫描会话事件定位前序消息/上次注入/requestMessages
  - 证据: `packages/context/time-context/src/index.ts:59 agent.session.events 事件重放（user/message/tool/result/turn/start）+ package.json:40`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
