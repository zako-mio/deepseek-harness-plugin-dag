# dsh-session-title

- 包名: `@deepseek-ai/dsh-session-title`
- 分组: G31 会话核心
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/session/session-title`

## 实现逻辑
提供 ctx.sessionTitle：以日志中的 session/title 事件为唯一真相源，get 直接折叠最新标题，rename 接受显式用户标题（归一化后为空则抛 SessionTitleInvalidError）并使其钉住、阻止后续自动生成 (src/index.ts:288-298, src/index.ts:391-427)。服务注册 title 与 titleInput 两个投影单元，前者取最新标题文本，后者折叠首条/计数/末条合格人类消息 (src/index.ts:269-281, src/index.ts:344-360)。自动生成按 provider 的 automatic 模式（first-prompt / all-prompts）在 user/message 上排队，等 request/header 或带主循环标记的 llm/stream 记录到确切路由后才启动，并用每会话 revision + AbortController 实现最新者胜、旧调用被取消 (src/index.ts:506-581, src/index.ts:700-720)。确定性回退标题在无 provider 或 provider 失败时补位，服务注销、provider 注销与会话销毁都会中止在途工作并等待静默 (src/index.ts:798-843, src/index.ts:332-383, src/index.ts:478-503)。

## Provides
- ctx.sessionTitle (日志支撑的会话标题服务：折叠读取、显式重命名、自动生成调度与确定性回退)
- SessionProjectionMap/StateMap 的 title 与 titleInput 单元，以及 SessionTitleProvider 提供方契约

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 合并 agent 侧投影类型声明
  - 证据: `package.json:40 peerDep + src/index.ts:21 import type {}（合并 SessionProjectionMap 的 turnBoundary 声明）`
- `dsh-agent-loop` [运行时依赖] - 读 turnBoundary 判断主请求是否已开始本回合
  - 证据: `src/index.ts:552 ctx.sessionProjections.stateOf(session, 'turnBoundary')；packages/core/agent-loop/src/index.ts:378 注册该投影`
- `dsh-llm` [E1+E2] - 识别主循环请求并读取其 provider/model 路由
  - 证据: `package.json:42 peerDep + src/index.ts:11-12 import isAgentLoopRequest/GenerateOptions；src/index.ts:374 ctx.on('llm/stream')`
- `dsh-session` [E1+E2] - 把标题写入会话日志并从日志折叠
  - 证据: `package.json:43 peerDep + src/index.ts:18 import SessionSeq；src/index.ts:362 ctx.on('session/event')、src/index.ts:409 ctx.sessions.get`
- `dsh-session-projection` [E1+E2] - 注册 title/titleInput 投影单元并读取其状态
  - 证据: `package.json:44 peerDep + src/index.ts:19-20 import type ProjectionDefinition；src/index.ts:344 与 src/index.ts:346 ctx.sessionProjections.register`

## Dependents (下游被依赖)
- `dsh-api-session-controller` - 重命名会话时生成/校验标题
- `dsh-session-reference` - 引入 title 投影键的类型合并以读取会话标题作为提及标签
- `dsh-session-title-all-prompts-llm` - 向会话标题服务注册一个自动标题提供者，并复用其 id 构造与标题规范化
- `dsh-session-title-first-prompt-llm` - 把本 provider 注册进标题服务并复用标题归一化
