# dsh-experimental-tool-agent-team

- 包名: `@deepseek-ai/dsh-experimental-tool-agent-team`
- 分组: G13 实验特性
- 拓扑层: Layer 5
- 来源层: L3 其余
- 源码路径: `packages/experimental/tool-agent-team`

## 实现逻辑
函数式插件，在 Team 成员的 Agent 作用域内一次性注册完整工具集：spawn_teammate、send_message、list_agents、wait_agent、interrupt_agent 与 team_task_create/list/get/update（含 CAS 语义），每个工具都声明规范化输出 schema 并只允许对应角色调用 (src/index.ts:163-391)。同时向该作用域注入 team:policy 系统提示段，说明写作用域重叠只是建议而非锁、任务就绪不会唤醒 owner 等协作规则 (src/index.ts:168-172, src/index.ts:31-37)。wait_agent 先同步读取是否存在活跃 peer，无活跃 peer 时立即返回 noProgress，避免空等 (src/index.ts:252-275)。安装按 agent/created 与 agent/disposed 增量维护，卸载时逆序释放所有注册 (src/index.ts:401-422)。

## Provides
- Agent 作用域的 Team 工具集 (spawn_teammate/send_message/list_agents/wait_agent/interrupt_agent 与 team_task_*)
- team:policy 系统提示段

## Depends On (上游依赖)
- `dsh-agent` [E1+E2] - 工具按 Agent 作用域安装，并随 Agent 生命周期增删
  - 证据: `src/index.ts:5 import type { Agent } from '@deepseek-ai/dsh-agent' + src/index.ts:412 ctx.agents.list() + src/index.ts:413 ctx.on('agent/created') + src/index.ts:14 inject 'agents' + package.json:35 peerDep`
- `dsh-session` [编译依赖] - Team 成员与会话一一对应，声明依赖保证组合中存在同一份会话实现
  - 证据: `package.json:36 peerDep`
- `dsh-system-prompt` [运行时依赖] - 协作策略以系统提示段形式随工具一起注入该作用域
  - 证据: `src/index.ts:14 inject 'systemPrompt' + src/index.ts:168 scoped.systemPrompt.section({ name: 'team:policy', order: scoped.systemPrompt.getSectionOrder('TEAM_POLICY'), text: POLICY }) + package.json:37 peerDep`
- `dsh-tools` [E1+E2] - 工具定义、输出 schema 校验与作用域注册由 tools seam 提供
  - 证据: `src/index.ts:8-9 import { defineTool } + import type { InferValue, ValueSchemaSpec } + src/index.ts:174 scoped.tools.register(defineTool({...})) + src/index.ts:14 inject 'tools' + package.json:39 peerDep`

## Dependents (下游被依赖)
- 无下游（叶子/被消费端）
