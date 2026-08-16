# dsh-commands

- 包名: `@deepseek-ai/dsh-commands`
- 分组: G10 命令交互
- 拓扑层: Layer 3
- 来源层: L1 核心集
- 源码路径: `packages/interaction/commands`

## 实现逻辑
定义 ctx.commands CommandRuntime(TypertRemoteService 默认导出)，用 ScopedLayers 做全局+per-agent scope 命令注册。register() 校验名称/描述/handler；execute() 解析斜杠行，mint commandId、append 'command/run' 日志事件、调用 handler、settle 后 append 'command/done'。list()/find() 是 @Remote 导出，notifyChange 发 'commands/change'。

## Provides
- ctx.commands(CommandRuntime)
- session 事件 command/run|command/done
- commands/change emit 事件
- @Remote list/find/execute
- parseCommand/CommandId

## Depends On (上游依赖)
- `dsh-agent` [编译依赖] - 命令执行目标 agent
  - 证据: `packages/interaction/commands/src/index.ts:7,260`
- `dsh-session` [运行时依赖] - 命令生命周期事件持久化
  - 证据: `packages/interaction/commands/src/index.ts:308,330,360`

## Dependents (下游被依赖)
- `dsh-client-ui-commands` - Host 命令目录与执行 wire
- `dsh-client-ui-conversation` - command/run 事件与命令 surface 契约
- `dsh-client-ui-goal` - command/run 事件与 CommandId 契约
- `dsh-client-ui-plan` - 执行 /plan off 命令通道
- `dsh-command-compact` - /命令注册
- `dsh-command-feedback` - /命令注册
- `dsh-command-goal` - /命令注册
- `dsh-permission-presets` - /permission 命令注册
- `dsh-plan-mode` - /plan 命令
- `dsh-session-log-export` - CommandResult 类型
