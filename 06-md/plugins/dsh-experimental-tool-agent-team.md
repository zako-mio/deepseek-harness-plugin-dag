# dsh-experimental-tool-agent-team

- 包名: `@deepseek-ai/dsh-experimental-tool-agent-team`
- 分组: G38 多智能体协作
- 拓扑层: Layer 7
- 来源层: L3 其余
- 源码路径: `packages/experimental/tool-agent-team`

## 为什么需要它（设计初衷）
把agent-team的底层服务封装成模型可直接调用的协作工具，屏蔽服务细节，使Lead与teammate通过工具协议协作并遵守写作用域纪律。

发展史：RC8 新增

## 实现逻辑
面向模型的Agent Teams工具集(私有包)。src/index.ts:14 inject=['agents','agentTeams','tools','systemPrompt']。install 在每个exact Agent作用域注册：POLICY系统提示section、spawn_teammate(仅Lead可调)、send_message/followup_task(quiet/wakeup两种投递)、list_agents、wait_agent(含no-progress快速路径)、interrupt_agent、team_task_create/list/get/update等。所有工具经 ctx.agentTeams 服务转发，callingAgent 从exec.agent恢复调用者身份。Config含freshProvider/forkProvider指定teammate子代理提供者。

## Provides
- 模型面向工具: spawn_teammate/send_message/followup_task/list_agents/wait_agent/interrupt_agent/team_task_*
- Team协作POLICY系统提示注入
- Agent-scoped工具注册

## Depends On (上游依赖)
- `dsh-agent` [运行时依赖] - 恢复exact调用者agent身份
  - 证据: `src/index.ts:152-156 callingAgent`
- `dsh-experimental-agent-team` [运行时依赖] - 转发所有Team协作操作
  - 证据: `src/index.ts:14 inject ['agentTeams']`
- `dsh-system-prompt` [运行时依赖] - 注入Team协作策略提示
  - 证据: `src/index.ts:164 scoped.systemPrompt.section`
- `dsh-tools` [运行时依赖] - 工具定义与注册
  - 证据: `src/index.ts:8 defineTool`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
