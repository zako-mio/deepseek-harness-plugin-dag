# dsh-tool-goal

- 包名: `@deepseek-ai/dsh-tool-goal`
- 分组: G17 目标与计划
- 拓扑层: Layer 6
- 来源层: L1 核心集
- 源码路径: `packages/goal/tool-goal`

## 实现逻辑
注册 get_goal/create_goal/update_goal 三个模型可调用工具，并向 systemPrompt 写入 tool:goal 策略节（src/index.ts:187-342）。authority.ts 在每次执行时要求精确 live 的调用 agent，并区分「直接人类输入」与「当前目标轮」两种权威（src/authority.ts:48-117）。update_goal 的 blocked 需满足配置的连续轮数阈值，且在目标轮内 complete/blocked 会 deferContext 注入收尾指令（src/index.ts:305-330）。

## Provides
- get_goal/create_goal/update_goal 模型工具 (定义并注册到 tools 注册表)
- tool:goal 系统提示词节 (目标工具策略与 blocked 阈值指引)

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 校验调用 agent 的 live 身份与 root 归属以判定人类权威
  - 证据: `src/authority.ts:4 import Agent + src/authority.ts:53 ctx.agents.get + src/authority.ts:81 ctx.agents.roots`
- `dsh-goal` [E1+E2] - 通过目标域服务执行工具操作并读取 CAS 引用
  - 证据: `src/index.ts:9-10 import (GoalId, GoalRef, GoalView) + src/authority.ts:113 ctx.goals.get + src/index.ts:225 ctx.goals.create`
- `dsh-llm` [编译依赖] - 构造收尾上下文消息与结构化工具错误
  - 证据: `src/index.ts:11 import (boundContextSummary, createUserMessage, HarnessError) + src/wrapup.ts:3 import ContentBlock`
- `dsh-session` [编译依赖] - 权威判定所需的会话事件与序列号类型
  - 证据: `src/authority.ts:7 import (SessionEvent, SessionSeq)`
- `dsh-session-projection` [E1+E2] - 读取 turnBoundary 投影确定开放轮的起始序列号
  - 证据: `src/authority.ts:9 import type {} + src/authority.ts:35 ctx.sessionProjections.stateOf(agent.session,'turnBoundary')`
- `dsh-system-prompt` [运行时依赖] - 注册目标工具策略段并按序插入系统提示词
  - 证据: `src/index.ts:29 inject [...'systemPrompt'] + src/index.ts:189-191 ctx.systemPrompt.section/getSectionOrder`
- `dsh-tools` [E1+E2] - 以 defineTool 定义并注册三个目标工具
  - 证据: `src/index.ts:19-20 import (defineTool, GenericCallView) + src/index.ts:29 inject ['agents','goals','tools','systemPrompt','sessionProjections'] + src/index.ts:195 ctx.tools.register`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
